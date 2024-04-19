
#include "gpio_helper.h"
#include "xmc_gpio.h"

void init_gpio(xmc_gpio_t *pin,XMC_GPIO_MODE_t add_af)
{
	XMC_GPIO_CONFIG_t config_struct;
	config_struct.mode = (pin->af|add_af);
	XMC_GPIO_Init((XMC_GPIO_PORT_t *)pin->port,pin->pin,&config_struct);
}

void set_gpio(xmc_gpio_t *pin,uint8_t val)
{
	XMC_GPIO_SetOutputLevel((XMC_GPIO_PORT_t *)pin->port,pin->pin,((val)?(XMC_GPIO_OUTPUT_LEVEL_HIGH):(XMC_GPIO_OUTPUT_LEVEL_LOW)));
}
