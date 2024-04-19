

#ifndef CCU_4_HANDLER_H_
#define CCU_4_HANDLER_H_

#include <xmc_ccu4.h>
#include <xmc_scu.h>
#include <xmc_gpio.h>
#include "gpio_helper.h"
#include <stdint.h>
#include <stdbool.h>


typedef struct CCU4_Module_S {
	CCU4_GLOBAL_TypeDef  *ccu4_mod_dev;
}CCU4_Module_t;


typedef struct CCU4_slice {
	CCU4_CC4_TypeDef  			*chan_dev;
	CCU4_Module_t	  			*module_dev;
	XMC_CCU4_SLICE_PRESCALER_t 	pre_scaler;
	uint8_t						slice_n;
	uint32_t					shadow_mask;
}CCU4_slice_t;


typedef struct CCU4_PWM {
	CCU4_slice_t slice;
	xmc_gpio_t pwm_pin;
	bool is_running;
	uint16_t current_period;
}CCU4_PWM_t;

typedef struct CCU4_CAPTURE {
	CCU4_slice_t slice;
	xmc_gpio_t pwm_pin;
	XMC_CCU4_SLICE_INPUT_t input;
	XMC_CCU4_SLICE_SR_ID_t 	irq_slice;
	bool is_running;
	uint16_t current_count;
	IRQn_Type irq_n;
	uint32_t priority;
	void(*cb)(void);
}CCU4_CAPTURE_t;

/**
 * @brief initilizes ccu4 timer
 *
 * @param dev - pointer to Timer struct being used
 */
void init_ccu4_timer(CCU4_Module_t* dev);





uint16_t fast_100_scaller(uint16_t period,uint8_t power);

void init_pwm(CCU4_PWM_t *dev);

void start_pwm(CCU4_PWM_t *dev,uint16_t compare,uint16_t period);

void stop_pwm(CCU4_PWM_t *dev);

void update_pwm(CCU4_PWM_t *dev,uint16_t compare);

void update_pwm_power(CCU4_PWM_t *dev,uint8_t power);


void _capture_irq(CCU4_CAPTURE_t *dev);

void init_capture(CCU4_CAPTURE_t *dev);

void register_capture_cb(CCU4_CAPTURE_t *dev,void(*cb)(void));

#define CCU4_MODULE_DEV_DEF(name,device)  																						\
		CCU4_Module_t name = {			  																						\
				.ccu4_mod_dev = device,	  																						\
};


#define SETUP_SLICE(chan,module,scale,n,shadow)	\
		{										\
		.chan_dev = chan,						\
		.module_dev = module,					\
		.pre_scaler = scale,					\
		.slice_n = n,							\
		.shadow_mask = shadow,					\
		}


#define CCU4_PWM_DEF(name,chan,module,scale,n,shadow,port_n,pin_n,af_n) \
		CCU4_PWM_t name = {												\
				.slice = SETUP_SLICE(chan,module,scale,n,shadow),		\
				.pwm_pin = SETUP_GPIO(port_n,pin_n,af_n),				\
};


#define CCU4_CAPTURE_DEF(name,chan,module,scale,n,shadow,port_n,pin_n,in_n,IRQ,n_IRQ,slicey,pri) 	\
		CCU4_CAPTURE_t name = {																		\
				.slice = SETUP_SLICE(chan,module,scale,n,shadow),									\
				.pwm_pin = SETUP_GPIO(port_n,pin_n,0),												\
				.input = in_n,																		\
				.irq_n = n_IRQ,																		\
				.priority = pri,																	\
				.irq_slice = slicey,																\
};																									\
void IRQ(void){_capture_irq(&name);}

#endif
