/******************************************************************************
 * @file     EasyMain.c
 * @brief    Uses a system timer to toggle the  ports P0.0 to P0.2 and P0.5 to P0.9 with 200ms frequency.
 *			 LEDs that are connected to these ports will toggle respectively.
 * 			 In addition it uses the UART of USIC Channel 1 to send a message every 2s to a terminal
 *			 emulator. The communication settings are 57.6kbps/8N1
 *			 P1.3 is configured as input (RXD) and P1.2 is configured as output(TXD)
 *			 This project runs without modifications on the XMC1100 kit for ARDUINO
 * @version  V1.0
 * @date     20. February 2015
 * @note
 * Copyright (C) 2015 Infineon Technologies AG. All rights reserved.
 ******************************************************************************
 * @par
 * Infineon Technologies AG (Infineon) is supplying this software for use with
 * Infineon�s microcontrollers.
 * This file can be freely distributed within development tools that are
 * supporting such microcontrollers.
 * @par
 * THIS SOFTWARE IS PROVIDED "AS IS".  NO WARRANTIES, WHETHER EXPRESS, IMPLIED
 * OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE.
 * INFINEON SHALL NOT, IN ANY CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL,
 * OR CONSEQUENTIAL DAMAGES, FOR ANY REASON WHATSOEVER.
 *****************************************************************************/

#include <string.h>

#include "XMC1100.h"
#include "GPIO.h"
#include "Uptime.h"
#include "infxmc_uart.h"
#include "debug.h"
#include "gpio_helper.h"
#include "CCU4_Handler.h"
#include <stdbool.h>

#define DEBUG_UART_XMC 					XMC_UART0_CH0

#define DEBUG_BAUD_RATE					115200

#define DEBUG_UART_IRQ					USIC0_0_IRQn
#define DEBUG_UART_IRQ_HANDLER			USIC0_0_IRQHandler
#define DEBUG_UART_USIC_NODE			0

#define DEBUG_UART_RX_IRQ				USIC0_1_IRQn
#define DEBUG_UART_RX_IRQ_HANDLER		USIC0_1_IRQHandler
#define DEBUG_UART_RX_USIC_NODE			1

#define DEBUG_TX_PORT					XMC_GPIO_PORT2
#define DEBUG_TX_PIN					1
#define DEBUG_TX_AF						P2_1_AF_U0C0_DOUT0

#define DEBUG_RX_PORT					XMC_GPIO_PORT2
#define DEBUG_RX_PIN					2
#define DEBUG_RX_INPUT 					USIC0_C0_DX3_P2_2
#define DEBUG_RXD_INPUT					XMC_UART_CH_INPUT_RXD1




#define ENA_CC4_PRESCALLER				XMC_CCU4_SLICE_PRESCALER_128


#define ENA_CC4_SLICE					CCU40_CC42
#define ENA_CC4_SLICE_N					2
#define ENA_CC4_SHADOW					XMC_CCU4_SHADOW_TRANSFER_SLICE_2

#define ENA_CC4_IRQ						CCU40_2_IRQHandler
#define ENA_CC4_IRQN					CCU40_2_IRQn

#define ENA_PORT						XMC_GPIO_PORT2
#define ENA_PIN							10
#define ENA_AF							P2_10_AF_CCU40_OUT2


#define ENB_CC4_PRESCALLER				XMC_CCU4_SLICE_PRESCALER_128

#define ENB_CC4_SLICE					CCU40_CC43
#define ENB_CC4_SLICE_N					3
#define ENB_CC4_SHADOW					XMC_CCU4_SHADOW_TRANSFER_SLICE_3


#define ENB_CC4_IRQ						CCU40_3_IRQHandler
#define ENB_CC4_IRQN					CCU40_3_IRQn

#define ENB_PORT						XMC_GPIO_PORT2
#define ENB_PIN							11
#define ENB_AF							P2_11_AF_CCU40_OUT3


#define MOTOR_CC4_MODULE				CCU40






UART_DEV_DEF(debug_uart,DEBUG_UART_XMC,DEBUG_BAUD_RATE,
		UART_STANDARD_DATA_BITS,1,
		DEBUG_RX_PORT,DEBUG_RX_PIN,DEBUG_RX_INPUT,DEBUG_RXD_INPUT,
		DEBUG_TX_PORT,DEBUG_TX_PIN,DEBUG_TX_AF,
		DEBUG_UART_RX_IRQ,	DEBUG_UART_RX_IRQ_HANDLER,	DEBUG_UART_RX_USIC_NODE,	3,	0,
		DEBUG_UART_IRQ,		DEBUG_UART_IRQ_HANDLER,		DEBUG_UART_USIC_NODE,		3,		0,
		64,1024);

void SysTick_Handler(void)
{
	inc_uptime();


}


DEF_GPIO(led0,XMC_GPIO_PORT0,6);
DEF_GPIO(led1,XMC_GPIO_PORT0,7);
DEF_GPIO(led2,XMC_GPIO_PORT0,8);
DEF_GPIO(led3,XMC_GPIO_PORT0,9);
DEF_GPIO(greenLight,XMC_GPIO_PORT0,14)
CCU4_MODULE_DEV_DEF(Mot_CCU, MOTOR_CC4_MODULE);
CCU4_PWM_DEF(HeadLights,ENA_CC4_SLICE,&Mot_CCU,ENA_CC4_PRESCALLER,ENA_CC4_SLICE_N,ENA_CC4_SHADOW,ENA_PORT,ENA_PIN,ENA_AF);
CCU4_PWM_DEF(TailLights,ENB_CC4_SLICE,&Mot_CCU,ENB_CC4_PRESCALLER,ENB_CC4_SLICE_N,ENB_CC4_SHADOW,ENB_PORT,ENB_PIN,ENB_AF);



void sendDebugString(const char*const str)
{
	for(const char *c = str;*c!='\0';c++)
	{
		xmc_uart_send_byte(&debug_uart,*c);
	}
}

void set_bar(uint8_t mask)
{
	set_gpio(&led0,(mask>>3)&0x1);
	set_gpio(&led1,(mask>>2)&0x1);
	set_gpio(&led2,(mask>>1)&0x1);
	set_gpio(&led3,(mask>>0)&0x1);

}


int main(void)
{
	// Clock configuration
	init_gpio(&led0,XMC_GPIO_MODE_OUTPUT_PUSH_PULL);
	init_gpio(&led1,XMC_GPIO_MODE_OUTPUT_PUSH_PULL);
	init_gpio(&led2,XMC_GPIO_MODE_OUTPUT_PUSH_PULL);
	init_gpio(&led3,XMC_GPIO_MODE_OUTPUT_PUSH_PULL);
	init_gpio(&greenLight,XMC_GPIO_MODE_OUTPUT_PUSH_PULL);

	set_gpio(&greenLight,0);
	init_ccu4_timer(&Mot_CCU);

	init_pwm(&HeadLights);
	init_pwm(&TailLights);
	start_pwm(&HeadLights,125,1000);
	start_pwm(&TailLights,125,1000);
//	start_pwm(&HeadLights,0,1000);
//	start_pwm(&TailLights,0,1000);


	set_bar(0x0);
	SysTick_Config(SystemCoreClock / 1000);
	xmc_uart_init(&debug_uart);
	startdebug(sendDebugString);
	debug_print("Hello Racers!\r\n");
	set_bar(0xf);
	while(1)
	{
		for(size_t i = 0;i<10;i++)
		{
			set_bar(0b1100);
			busy_wait_ms(500);
			set_bar(0b0011);
			busy_wait_ms(500);
		}
		for(size_t i = 0;i<10;i++)
		{
			set_bar(0b1001);
			busy_wait_ms(500);
			set_bar(0b0110);
			busy_wait_ms(500);
		}

	}
}



