/*
 * hardware.h
 *
 *  Created on: Jun 28, 2022
 *      Author: Ben deVries
 */

#ifndef INFXMC_UART_H_
#define INFXMC_UART_H_



#ifdef __cplusplus
extern "C" {
#endif

#include "xmc_uart.h"
#include "xmc_gpio.h"
#include "ring_buffer.h"


#define UART_STANDARD_BAURDRATE  		115200
#define UART_STANDARD_DATA_BITS			8
#define UART_STANDARD_STOP_BITS			1

typedef enum
{
  uart_ok      					=  0,
  buffer_full  					= -1,
  buffer_empty					= -2,
  device_not_initialized     	= -3,
} xmc_uart_status_t;


//Uart Devices
typedef struct uart_isr
{
	//This will be called everytime a new byte comes in. It returns the length of the rx input
    void (*byte_available)(uint32_t bytes_avalible);

    //called whenever the tx buffer empties meaning room for more data
    void (*tx_buf_empty)(void);

    //called whenever al the tx bytes have been sent.
    void (*tx_complete)(void);



}uart_isr_t;



typedef struct infxmc_uart_config
{
	XMC_USIC_CH_t 					*channel; //Pointer to USIC device
	struct rx_con
	{
		XMC_GPIO_PORT_t *const port;
		uint8_t pin;
		uint8_t input; //Input that gets linked to USIC device
		XMC_UART_CH_INPUT_t rxd_input;
	}rx;
	struct tx_con
	{
		XMC_GPIO_PORT_t *const port;
		uint8_t pin;
		XMC_GPIO_MODE_t af; //Alternate function used to connect bin to USIC device
	}tx;
	IRQn_Type dev_irq; //USIC interupt
	uint32_t isr_prempt_pri; //ISR priority 0 is highest 63 lowest
	uint32_t isr_sub_pri;//ISR sub priority
	uint8_t  usic_node;
	IRQn_Type dev_irq_rx; //USIC interupt
	uint32_t isr_prempt_pri_rx; //ISR priority 0 is highest 63 lowest
	uint32_t isr_sub_pri_rx;//ISR sub priority
	uint8_t  usic_node_rx;
}infxmc_uart_config_t;



typedef struct infxmc_uart_data
{
	XMC_UART_CH_CONFIG_t 			uart_config;//XMC channel config
	bool dev_initialized; //Set to true when xmc_uart_init is started
	bool last_frame;
	volatile bool is_transmitting;
	ring_buffer_t tx_buffer; //Rolling buffer holding TX bytes
	ring_buffer_t rx_buffer; //Rolling buffer holding RX bytes
	struct uart_isr isr_cb;  //Device call back structure
}infxmc_uart_data_t;


typedef struct infxmc_uart_device
{
	const struct infxmc_uart_config *config;
	struct infxmc_uart_data			* const data;
}infxmc_uart_device_t;




/**
 * @brief initilizes hard ware required by uart periferial
 *
 * @param dev - pointer to uart device being used
 */
void xmc_uart_init(infxmc_uart_device_t *dev);

/**
 * @brief must be called every interupt of uart device
 *
 * @param dev - pointer to uart device being used
 */
void _xmc_uart_handle_isr(infxmc_uart_device_t *dev);

/**
 * @brief must be called every interupt of uart device
 *
 * @param dev - pointer to uart device being used
 */
void _xmc_uart_handle_rx_isr(infxmc_uart_device_t *dev);


/**
 * @brief used to hand off call back structure to the device
 *
 * @param dev - pointer to uart device being used
 * @param isrs - pointer to the collection of isr used
 *
 * See uart_isr for functions
 */
void xmc_uart_reg_isr(infxmc_uart_device_t *dev ,uart_isr_t *isrs);


/**
 * @brief this stuffs bytes into the tx buffer and starts it transmiting asncyrosnosly
 *
 * @param dev - pointer to uart device being used
 * @param byte - the byte of data being sent
 *
 * @retval 0 	byte added to the buffer
 * @retval -1 	tx buffer full
 * @retval -2	uart incorrectly configured
 */
xmc_uart_status_t xmc_uart_send_byte(infxmc_uart_device_t *dev, uint8_t byte);


/**
 * @brief pull data out of the rx buffer
 *
 * @param dev - pointer to uart device being used
 * @param byte - pointer to data out. Uses pointer so that codes can be returned
 *
 * @retval 0 	byte pulled from buffer
 * @retval -1 	rx buffer empty
 */
xmc_uart_status_t xmc_uart_get_byte(infxmc_uart_device_t *dev,uint8_t *byte);


/**
 * @brief dumps whatever is in the uart's TX buffer without the use of the interrupt
 * used when something has gone very wrong
 *
 * @param dev - pointer to uart device being used
 */
void xmc_uart_dump_tx_buff(infxmc_uart_device_t *dev);

/**
 * @brief get amount of data in the rx buffer
 *
 * @param dev - pointer to uart device being used
 *
 * @retval rx bytes in buffer
 */
__STATIC_INLINE uint32_t xmc_uart_available_rx_bytes(infxmc_uart_device_t *dev)
{
	struct infxmc_uart_data	  *data	 = dev->data;
	return(ring_buffer_avail(&data->rx_buffer));
}


/**
 * @brief gets the buffer space avalible in TX buffer
 *
 * @param dev - pointer to uart device being used
 *
 * @retval space left in tx buffer in bytes
 */
__STATIC_INLINE uint32_t xmc_uart_tx_buff_space(infxmc_uart_device_t *dev)
{
	struct infxmc_uart_data	  *data	 = dev->data;
	return(data->tx_buffer.len-ring_buffer_avail(&data->tx_buffer));
}


/**
 * @brief get baud rate of the device driver
 *
 * @param dev - pointer to uart device being used
 *
 * @retval baud rate in bits per second
 */
__STATIC_INLINE uint32_t xmc_uart_get_baud_rate(infxmc_uart_device_t *dev)
{
	return(dev->data->uart_config.baudrate);
}

/**
 * @brief set a new baud rate
 *
 * @param dev - pointer to uart device being used
 *
 * @param new_baud - The new baud rate of the device
 *
 * @retval modus ok if operation was succsessful
 */
uint32_t xmc_uart_set_baud_rate(infxmc_uart_device_t *dev,uint32_t new_baud);


/**
 * @def UART_DEV_DEF
 *
 * @brief This is a helper macro for putting together uart devices
 *
 * @param name the name you wish to give you serial device whenever a function
 * interacts with a device this name is given
 *
 * @param xmc_dev type XMC_USIC_CH_t pointer to the xmc register for the usic being used
 *
 * @param baud baud rate of the device
 *
 * @param data_b    	data bits
 *
 * @param stop_b		stop bits
 *
 * @param rx_port 		type XMC_GPIO_PORT_t port of the rx pin
 *
 * @param rx_pin		rx pin number being used
 *
 * @param rx_input		Used to link the rx pin to device sorce
 *
 * @param rxd			The RXD input being used by the current device
 *
 * @param ... other 	parameters as expected by DEVICE_DT_DEFINE.
 *
 * @param tx_port 		type XMC_GPIO_PORT_t port of the tx pin
 *
 * @param tx_pin		tx pin number being used
 *
 * @param tx_af			alternate function of a tx pin used to connect to driver
 *
 * @param irq_num		IRQ number used by the peripheral
 *
 * @param irq_name		Name of the IRQ handler used by the uart device
 * These can be found in the XMCxxxx.h files example USIC1_0_IRQHandler
 *
 * @param usic_node_n   The USIC interupt node used by the uart device 1-3
 *
 * @param irq_prem_pri	Premption priority of devices interrupt
 *
 * @param irq_sub_priority sub priority of interrupt
 *
 * @param rx_buf_size 	size of the rx buffer
 *
 * @param tx_buf_size   size of the tx buffer
 *
 * @param ... other parameters as expected by DEVICE_DT_DEFINE.
 */



#define UART_DEV_DEF(name,xmc_dev,baud,data_b,stop_b,rx_port,rx_pin,rx_input,rxd,tx_port,tx_pin,tx_af,	\
		irq_rx_num,irq_rx_name,usic_rx_node_n,irq_rx_prem_pri,irq_rx_sub_priority,						\
		irq_num,irq_name,usic_node_n,irq_prem_pri,irq_sub_priority,rx_buf_size,tx_buf_size) 			\
		const infxmc_uart_config_t name##config = {													\
			.channel = xmc_dev,																		\
			.usic_node = usic_node_n,																\
			.rx = {																					\
				.port = rx_port,																	\
				.pin = rx_pin,																		\
				.input = rx_input,																	\
				.rxd_input = rxd,																	\
			},																						\
			.tx = {																					\
				.port = tx_port,																	\
				.pin = tx_pin,																		\
				.af = tx_af,																		\
			},																						\
			.dev_irq = irq_num,																		\
			.isr_prempt_pri = irq_prem_pri,															\
			.isr_sub_pri = irq_sub_priority,														\
			.dev_irq_rx = irq_rx_num,																\
			.isr_prempt_pri_rx = irq_rx_prem_pri,													\
			.isr_sub_pri_rx = irq_rx_sub_priority,													\
			.usic_node_rx = usic_rx_node_n,															\
			};																						\
			uint8_t name##rx_buf[rx_buf_size] = {0};												\
			uint8_t name##tx_buf[tx_buf_size] = {0};												\
			infxmc_uart_data_t name##data = {														\
					.uart_config = {																\
					  .baudrate = baud,																\
					  .data_bits = data_b,															\
					  .stop_bits = stop_b,															\
					},																				\
					.last_frame		 = false,														\
					.dev_initialized = false,														\
					.tx_buffer = {																	\
							.buffer = name##tx_buf,													\
							.head = 0,																\
							.tail = 0,																\
							.len = tx_buf_size,														\
					},																				\
					.rx_buffer = {																	\
							.buffer = name##rx_buf,													\
							.head = 0,																\
							.tail = 0,																\
							.len = rx_buf_size,														\
					},																				\
					.isr_cb = {																		\
							.byte_available = NULL,													\
							.tx_buf_empty = NULL,													\
					},																				\
			};																						\
			infxmc_uart_device_t name = {															\
					.config = &name##config,														\
					.data 	= &name##data,															\
			};																						\
			/*This function will exist in the file that defines the driver*/						\
			void irq_name(void)	{ _xmc_uart_handle_isr(&name); }									\
			void irq_rx_name(void) { _xmc_uart_handle_rx_isr(&name); }								\




#ifdef __cplusplus
}
#endif


#endif
