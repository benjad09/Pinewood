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

#include "ledSeq.h"

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
DEF_GPIO(greenLight,XMC_GPIO_PORT0,5)
CCU4_MODULE_DEV_DEF(Mot_CCU, MOTOR_CC4_MODULE);
CCU4_PWM_DEF(TailLights,ENA_CC4_SLICE,&Mot_CCU,ENA_CC4_PRESCALLER,ENA_CC4_SLICE_N,ENA_CC4_SHADOW,ENA_PORT,ENA_PIN,ENA_AF);
CCU4_PWM_DEF(HeadLights,ENB_CC4_SLICE,&Mot_CCU,ENB_CC4_PRESCALLER,ENB_CC4_SLICE_N,ENB_CC4_SHADOW,ENB_PORT,ENB_PIN,ENB_AF);



void sendDebugString(const char*const str)
{
	for(const char *c = str;*c!='\0';c++)
	{
		xmc_uart_send_byte(&debug_uart,*c);
	}
}

void set_bar(uint8_t mask)
{
	set_gpio(&led2,(mask>>3)&0x1);
	set_gpio(&led0,(mask>>2)&0x1);
	set_gpio(&led1,(mask>>1)&0x1);
	set_gpio(&led3,(mask>>0)&0x1);

}

const LedCommand_t leftright[] = {COMMAND_DEF(0b1100,500),COMMAND_DEF(0b0011,500)};
SEQUENCE_DEF(lrseq,leftright,10);

const LedCommand_t outin[] = {COMMAND_DEF(0b0110,500),COMMAND_DEF(0b1001,500)};
SEQUENCE_DEF(outinseq,outin,10);

const LedCommand_t squig[] = {COMMAND_DEF(0b0101,200),COMMAND_DEF(0b1010,200)};
SEQUENCE_DEF(squiginseq,squig,10);

const LedCommand_t flasyLR[] = {COMMAND_DEF(0b1000,100),COMMAND_DEF(0b0100,50),COMMAND_DEF(0b1000,100),COMMAND_DEF(0b0100,50),COMMAND_DEF(0b1000,100),COMMAND_DEF(0b0100,50),COMMAND_DEF(0b1000,100),COMMAND_DEF(0b0100,50),
								COMMAND_DEF(0b0001,100),COMMAND_DEF(0b0010,50),COMMAND_DEF(0b0001,100),COMMAND_DEF(0b0010,50),COMMAND_DEF(0b0001,100),COMMAND_DEF(0b0010,50),COMMAND_DEF(0b0001,100),COMMAND_DEF(0b0010,50)};
SEQUENCE_DEF(flashLRseq,flasyLR,3);


const LedCommand_t indecateRight[] = {COMMAND_DEF(0b1000,100),COMMAND_DEF(0b1100,100),COMMAND_DEF(0b1110,100),COMMAND_DEF(0b1111,100),COMMAND_DEF(0b0111,100),COMMAND_DEF(0b0011,100),COMMAND_DEF(0b0001,100),COMMAND_DEF(0b0000,100)};
SEQUENCE_DEF(goRight,indecateRight,10);

const LedCommand_t indecateLeft[] = {COMMAND_DEF(0b0001,100),COMMAND_DEF(0b0011,100),COMMAND_DEF(0b0111,100),COMMAND_DEF(0b1111,100),COMMAND_DEF(0b1110,100),COMMAND_DEF(0b1100,100),COMMAND_DEF(0b1000,100),COMMAND_DEF(0b0000,100)};
SEQUENCE_DEF(goLeft,indecateLeft,10);

const LedCommand_t indecateCenter[] = {COMMAND_DEF(0b1001,200),COMMAND_DEF(0b1111,200),COMMAND_DEF(0b0110,200),COMMAND_DEF(0b0000,200)};
SEQUENCE_DEF(goCenter,indecateCenter,10);

LedRunner_t barRunner = {0};
LedRunner_t greenRunner = {0};
LedRunner_t headlightrunner = {0};
LedRunner_t taillightrunner = {0};

const LedCommand_t flashBrights[] = {COMMAND_DEF(1000,250),COMMAND_DEF(100,250)};
SEQUENCE_DEF(flashB,flashBrights,2);

const LedCommand_t GO_GREENSTART[] = {COMMAND_DEF(1,250),COMMAND_DEF(0,250)};
SEQUENCE_DEF(startGreen,GO_GREENSTART,3);

const LedCommand_t HOLDGREEN[] = {COMMAND_DEF(1,5000),COMMAND_DEF(0,100)};
SEQUENCE_DEF(HoldGreen,HOLDGREEN,1);

const LedCommand_t B_ON[] = {COMMAND_DEF(1000,100)};
SEQUENCE_DEF(brake_on,B_ON,1);

const LedCommand_t B_OFF[] = {COMMAND_DEF(125,100)};
SEQUENCE_DEF(brake_off,B_OFF,1);

void brake(int argc,char **argv)
{
	if(argc == 1)
	{
		switch(argv[0][0])
		{
		case '1':
		case 'I':
		case 'i':
		case 's':
		case 'S':
			start_Lrunner(&taillightrunner,&brake_on);
			return;
			break;
		default:
			break;
		}
	}
	start_Lrunner(&taillightrunner,&brake_off);
}

void flash(int argc,char **argv)
{
	(void) argc;
	(void) argv;
	start_Lrunner(&headlightrunner,&flashB);
	//start_Lrunner(&taillightrunner,&flashB);
}

void green(int argc,char **argv)
{
	//ITSNOT EASY BEING GREEN
	(void) argc;
	(void) argv;
	start_Lrunner(&greenRunner,&startGreen);
}

void goDir(int argc,char **argv)
{
	if (argc>= 1)
	{
		switch(argv[0][0])
		{
		case '0':
		case 'L':
		case 'l':
			start_Lrunner(&barRunner,&goLeft);

			break;
		case '1':
		case 'C':
		case 'c':
			start_Lrunner(&barRunner,&goCenter);

			break;
		case '2':
		case 'R':
		case 'r':
			start_Lrunner(&barRunner,&goRight);

			break;
		default:
			debug_print("bad arg");
		}
	}
}

DEFINE_DEBUG_SUB(goDirsub,goDir,"pick a direction",false,1,1);

DEFINE_DEBUG_SUB(flashSub,flash,"thank You",false,0,0);

DEFINE_DEBUG_SUB(greenSub,green,"for you youngsters",false,0,0);

DEFINE_DEBUG_SUB(brakeSub,brake,"Hold UP",false,0,1);

volatile bool byteIn = false;

void db_in(uint32_t bytes_avalible)
{
	byteIn=true;
}

uart_isr_t debugISR =
{
		.byte_available = db_in,
};

int main(void)
{

	uint8_t charIn;
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
	xmc_uart_reg_isr(&debug_uart,&debugISR);



	startdebug(sendDebugString);
	subFnc(&goDirsub);
	subFnc(&greenSub);
	subFnc(&flashSub);
	subFnc(&brakeSub);
	debug_print("\r\n\n\n\nHello Racers!\r\n");
	set_bar(0xf);

	link_seq(&startGreen,&HoldGreen);

	link_seq(&goRight,&lrseq);
	link_seq(&goLeft,&lrseq);
	link_seq(&goCenter,&lrseq);




	link_seq(&lrseq,&outinseq);
	link_seq(&outinseq,&flashLRseq);
	link_seq(&flashLRseq,&squiginseq);
	link_seq(&squiginseq,&lrseq);
	start_Lrunner(&barRunner,&goRight);

	while(1)
	{
		if(update_Lrunner(&barRunner,uptime_get()))
		{
			set_bar(get_LrunnerVal(&barRunner));
		}
		if(update_Lrunner(&greenRunner,uptime_get()))
		{
			set_gpio(&greenLight,get_LrunnerVal(&greenRunner));
		}
		if(update_Lrunner(&headlightrunner,uptime_get()))
		{
			start_pwm(&HeadLights,get_LrunnerVal(&headlightrunner),1000);
		}
		if(update_Lrunner(&taillightrunner,uptime_get()))
		{
			start_pwm(&TailLights,get_LrunnerVal(&taillightrunner),1000);
		}
		if(byteIn)
		{
			byteIn = false;
			while(xmc_uart_get_byte(&debug_uart,&charIn) == uart_ok)
			{
				debugIn((charIn));
			}
		}
	}
}



