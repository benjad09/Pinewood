/*
 * gpio_helper.h
 *
 *  Created on: May 8, 2023
 *      Author: Ben deVries
 */

#ifndef SOURCE_SRC_GPIO_HELPER_H_
#define SOURCE_SRC_GPIO_HELPER_H_

#include "xmc_gpio.h"

typedef struct xmc_gpio {
	const XMC_GPIO_PORT_t *const port;
	const uint8_t pin;
	const XMC_GPIO_MODE_t af;
}xmc_gpio_t;

#define SETUP_GPIO(port_in,pin_in,af_in) \
		{.port = port_in,				 \
		 .pin = pin_in,					 \
		 .af = af_in,}					\

#define DEF_GPIO(name,port_in,pin_in) \
		xmc_gpio_t name = SETUP_GPIO(port_in,pin_in,0);

void init_gpio(xmc_gpio_t *pin,XMC_GPIO_MODE_t add_af);

void set_gpio(xmc_gpio_t *pin,uint8_t val);


#endif /* SOURCE_SRC_GPIO_HELPER_H_ */
