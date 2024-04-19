/*
 * infxmc_uart.c
 *
 *  Created on: Jun 29, 2022
 *      Author: Ben deVries
 */


#include "xmc_uart.h"
#include "xmc_usic.h"
#include "xmc_gpio.h"
#include "infxmc_uart.h"
#include "ring_buffer.h"

#define SERVICE_REQEST_0  0U


//See Header
void xmc_uart_init(infxmc_uart_device_t *dev)
{
	XMC_GPIO_CONFIG_t uart_tx;
	XMC_GPIO_CONFIG_t uart_rx;

	const struct infxmc_uart_config *config = dev->config;
	struct infxmc_uart_data	  *data	= dev->data;

	XMC_UART_CH_Init(config->channel, &data->uart_config);

	//XMC_GPIO_SetMode(config->rx.port,config->rx.pin, XMC_GPIO_MODE_INPUT_PULL_UP);
	#if UC_FAMILY == XMC1
	if(config->rx.rxd_input != XMC_UART_CH_INPUT_RXD)
	{
		XMC_UART_CH_SetInputSource(config->channel, XMC_UART_CH_INPUT_RXD, 6);
		if(config->rx.rxd_input != XMC_UART_CH_INPUT_RXD1)
		{
			XMC_UART_CH_SetInputSource(config->channel, XMC_UART_CH_INPUT_RXD1, 5);
		}
	}
	#endif


	XMC_UART_CH_SetInputSource(config->channel, config->rx.rxd_input, config->rx.input);


	/* Set service request for receive interrupt */
	XMC_USIC_CH_SetInterruptNodePointer(config->channel, XMC_USIC_CH_INTERRUPT_NODE_POINTER_RECEIVE, config->usic_node_rx);
	XMC_USIC_CH_SetInterruptNodePointer(config->channel, XMC_USIC_CH_INTERRUPT_NODE_POINTER_ALTERNATE_RECEIVE, config->usic_node_rx);
	XMC_USIC_CH_SetInterruptNodePointer(config->channel, XMC_USIC_CH_INTERRUPT_NODE_POINTER_TRANSMIT_SHIFT, config->usic_node);
	XMC_USIC_CH_SetInterruptNodePointer(config->channel, XMC_USIC_CH_INTERRUPT_NODE_POINTER_TRANSMIT_BUFFER, config->usic_node);
	XMC_USIC_CH_SetInterruptNodePointer(config->channel, XMC_USIC_CH_INTERRUPT_NODE_POINTER_PROTOCOL, config->usic_node);

	/*Set priority and enable NVIC node for receive interrupt*/
	#if UC_FAMILY == XMC4
	NVIC_SetPriority(config->dev_irq, NVIC_EncodePriority(NVIC_GetPriorityGrouping(), config->isr_prempt_pri, config->isr_sub_pri));
	NVIC_SetPriority(config->dev_irq_rx, NVIC_EncodePriority(NVIC_GetPriorityGrouping(), config->isr_prempt_pri_rx, config->isr_sub_pri_rx));
	#else
	NVIC_SetPriority(config->dev_irq,  NVIC_EncodePriority(NVIC_GetPriorityGrouping(),config->isr_prempt_pri,0));
	NVIC_SetPriority(config->dev_irq_rx, NVIC_EncodePriority(NVIC_GetPriorityGrouping(),config->isr_prempt_pri_rx,0));
	#endif
	NVIC_EnableIRQ(config->dev_irq);
	NVIC_EnableIRQ(config->dev_irq_rx);

	XMC_UART_CH_EnableEvent(config->channel, XMC_UART_CH_EVENT_STANDARD_RECEIVE |
			XMC_UART_CH_EVENT_ALTERNATIVE_RECEIVE | XMC_UART_CH_EVENT_TRANSMIT_BUFFER | XMC_UART_CH_EVENT_FRAME_FINISHED);

	XMC_UART_CH_Start(config->channel);

	uart_tx.mode = (XMC_GPIO_MODE_OUTPUT_PUSH_PULL | config->tx.af);
	uart_rx.mode = XMC_GPIO_MODE_INPUT_PULL_UP;
	XMC_GPIO_Init(config->rx.port,config->rx.pin,&uart_rx);

	XMC_GPIO_Init(config->tx.port,config->tx.pin,&uart_tx);
	//XMC_GPIO_SetMode(config->tx.port,config->tx.pin, (XMC_GPIO_MODE_t)(XMC_GPIO_MODE_OUTPUT_PUSH_PULL | config->tx.af));

	data->dev_initialized = true;
	data->is_transmitting = false;

}

uint32_t xmc_uart_set_baud_rate(infxmc_uart_device_t *dev,uint32_t new_baud)
{
	const struct infxmc_uart_config *config = dev->config;
	struct infxmc_uart_data	  		*data	= dev->data;
	uint32_t oversampling = 16UL;

	data->uart_config.baudrate = new_baud;

	if( data->uart_config.oversampling != 0U)
	{
		oversampling = (uint32_t) data->uart_config.oversampling;
	}

	/* Configure baud rate */
	if ( data->uart_config.normal_divider_mode)
	{
		/* Normal divider mode */
		(void)XMC_USIC_CH_SetBaudrateEx(config->channel,  data->uart_config.baudrate, oversampling);
	}
	else
	{
		/* Fractional divider mode */
		(void)XMC_USIC_CH_SetBaudrate(config->channel,  data->uart_config.baudrate, oversampling);
	}
	NVIC_EnableIRQ(config->dev_irq);

	return uart_ok;

}

//See Header
void xmc_uart_reg_isr(infxmc_uart_device_t *dev , uart_isr_t *isrs)
{
	struct infxmc_uart_data	  *data	= dev->data;
	if(isrs->byte_available != NULL)
	{
		data->isr_cb.byte_available = isrs->byte_available;
	}
	if(isrs->tx_buf_empty != NULL)
	{
		data->isr_cb.tx_buf_empty = isrs->tx_buf_empty;
	}
	if(isrs->tx_complete != NULL)
	{
		data->isr_cb.tx_complete = isrs->tx_complete;
	}
}


//See Header
xmc_uart_status_t xmc_uart_send_byte(infxmc_uart_device_t *dev, uint8_t byte)
{
	const struct infxmc_uart_config *config = dev->config;
	struct infxmc_uart_data	  		*data	= dev->data;
	XMC_USIC_CH_t *const channel = config->channel;
	if(!data->dev_initialized)
	{
		return device_not_initialized;
	}



	  if ((channel->TBCTR & USIC_CH_TBCTR_SIZE_Msk) == 0UL)//Ensure that uart has no fifo buffer
	  {
		//
		//Check if uart periferial is activly transmiting

		NVIC_DisableIRQ(config->dev_irq);
		if(ring_buffer_is_full(&data->tx_buffer))
		{
			NVIC_EnableIRQ(config->dev_irq);
			return buffer_full;
		}
		ring_buffer_put(&data->tx_buffer,byte);

		if(data->is_transmitting == false)
		{
			data->is_transmitting = true;
			data->last_frame = false;
			ring_buffer_get(&data->tx_buffer,&byte);
			channel->TBUF[0U] = (uint16_t)byte;
		}
		NVIC_EnableIRQ(config->dev_irq);
	  }
	  else
	  {
		return device_not_initialized;
	  }
	  return uart_ok;
}

//See Header
xmc_uart_status_t xmc_uart_get_byte(infxmc_uart_device_t *dev,uint8_t *byte)
{

	struct infxmc_uart_data	  *data	 = dev->data;
	if(!data->dev_initialized)
	{
		return device_not_initialized;
	}
	if(ring_buffer_get(&data->rx_buffer,(uint8_t *const)byte) == 0)
	{
		return uart_ok;
	}
	else
	{
		return buffer_empty;
	}
}


//See Header
void xmc_uart_dump_tx_buff(infxmc_uart_device_t *dev)
{
	const struct infxmc_uart_config *config = dev->config;
	struct infxmc_uart_data	  		*data	= dev->data;
	XMC_USIC_CH_t *const channel = config->channel;
	uint8_t byte;
	__disable_irq();
	while(!ring_buffer_is_empty(&data->tx_buffer))
	{
		while((XMC_USIC_CH_GetTransmitBufferStatus(channel) == XMC_USIC_CH_TBUF_STATUS_BUSY));
		ring_buffer_get(&data->tx_buffer,(uint8_t *const)&byte);
		channel->TBUF[0U] = (uint16_t)byte;
	}
	while((XMC_USIC_CH_GetTransmitBufferStatus(channel) == XMC_USIC_CH_TBUF_STATUS_BUSY));
	__enable_irq();
}

void _xmc_uart_handle_rx_isr(infxmc_uart_device_t *dev)
{
	const struct infxmc_uart_config *config = dev->config;
	struct infxmc_uart_data	  *data	 = dev->data;
	XMC_USIC_CH_t *const channel = config->channel;
	uint32_t status;
	uint8_t byte;
	do{
		status = XMC_UART_CH_GetStatusFlag(channel);
		if( status &
				( XMC_UART_CH_STATUS_FLAG_RECEIVE_INDICATION
				| XMC_UART_CH_STATUS_FLAG_ALTERNATIVE_RECEIVE_INDICATION) )
		{
			if((status & XMC_UART_CH_STATUS_FLAG_RECEIVE_INDICATION))
			{
				XMC_UART_CH_ClearStatusFlag(channel, (uint32_t)XMC_UART_CH_STATUS_FLAG_RECEIVE_INDICATION);
			}
			else
			{
				XMC_UART_CH_ClearStatusFlag(channel, (uint32_t)XMC_UART_CH_STATUS_FLAG_ALTERNATIVE_RECEIVE_INDICATION);
			}
			for(uint16_t i = 0; XMC_USIC_CH_GetReceiveBufferStatus(channel); i++)
			{
				byte = (uint8_t)XMC_UART_CH_GetReceivedData(channel);
				ring_buffer_put(&data->rx_buffer,byte);
				if(data->isr_cb.byte_available != NULL)
				{
					data->isr_cb.byte_available(ring_buffer_avail(&data->rx_buffer));
				}
				if(i>0)
				{
					__NOP();
				}
			}
		}
	}while(XMC_UART_CH_GetStatusFlag(channel) & ( XMC_UART_CH_STATUS_FLAG_RECEIVE_INDICATION | XMC_UART_CH_STATUS_FLAG_ALTERNATIVE_RECEIVE_INDICATION));
	//Check that we havent gotten a send interupt while handling current interupt
}

//See Header
void _xmc_uart_handle_isr(infxmc_uart_device_t *dev)
{
	const struct infxmc_uart_config *config = dev->config;
	struct infxmc_uart_data	  *data	 = dev->data;
	XMC_USIC_CH_t *const channel = config->channel;
	uint32_t status;
	uint8_t byte;


	do{
		status = XMC_UART_CH_GetStatusFlag(channel);
		if(status & XMC_UART_CH_STATUS_FLAG_TRANSMIT_BUFFER_INDICATION)
		{
			XMC_UART_CH_ClearStatusFlag(channel,XMC_UART_CH_STATUS_FLAG_TRANSMIT_BUFFER_INDICATION);
			if(!ring_buffer_is_empty(&data->tx_buffer))
			{
				ring_buffer_get(&data->tx_buffer,(uint8_t *const)&byte);
				channel->TBUF[0U] = (uint16_t)byte;
				data->last_frame = false;
			}
			else
			{
				data->last_frame = true;
			}

		}
		if(status & XMC_UART_CH_STATUS_FLAG_TRANSMITTER_FRAME_FINISHED)
		{
			XMC_UART_CH_ClearStatusFlag(channel,XMC_UART_CH_STATUS_FLAG_TRANSMITTER_FRAME_FINISHED);

//			status &= ~XMC_UART_CH_STATUS_FLAG_TRANSMIT_BUFFER_INDICATION;
			if(data->last_frame == true)
			{
				if(!ring_buffer_is_empty(&data->tx_buffer))
				{
					ring_buffer_get(&data->tx_buffer,(uint8_t *const)&byte);
					channel->TBUF[0U] = (uint16_t)byte;
					data->last_frame = false;
				}
				else
				{
					if((XMC_USIC_CH_GetTransmitBufferStatus(channel) != XMC_USIC_CH_TBUF_STATUS_BUSY))
					{
						if(data->isr_cb.tx_buf_empty != NULL)
						{
							data->isr_cb.tx_buf_empty();
						}
						if(data->isr_cb.tx_complete != NULL)
						{
							data->isr_cb.tx_complete();
						}
						data->is_transmitting = false;
					}
				}
			}
		}
		//TX done

	}while(XMC_UART_CH_GetStatusFlag(channel) & (XMC_UART_CH_STATUS_FLAG_TRANSMITTER_FRAME_FINISHED | XMC_UART_CH_STATUS_FLAG_TRANSMIT_BUFFER_INDICATION));
	//Check that we havent gotten a send interupt while handling current interupt
}
