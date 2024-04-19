/*
 * CCU4_Timer.c
 *
 *  Created on: Aug 26, 2022
 *      Author: Ben deVries
 */


#include "CCU4_Handler.h"
#include <xmc_ccu4.h>
#include <xmc_scu.h>
#include <xmc_gpio.h>
#include "gpio_helper.h"


#define CCU4_MAX(a,b) ((a>b)?a:b)
#define CCU4_MIN(a,b) ((a<b)?a:b)


void init_ccu4_timer(CCU4_Module_t *dev)
{

	XMC_CCU4_SetModuleClock(dev->ccu4_mod_dev,XMC_CCU4_CLOCK_SCU);
	XMC_CCU4_Init(dev->ccu4_mod_dev,XMC_CCU4_SLICE_MCMS_ACTION_TRANSFER_PR_CR);

}


static void init_slice(CCU4_slice_t *slice)
{
	XMC_CCU4_SLICE_COMPARE_CONFIG_t g_timer_object =
	{
	  .timer_mode 		   = XMC_CCU4_SLICE_TIMER_COUNT_MODE_EA,
	  .monoshot   		   = XMC_CCU4_SLICE_TIMER_REPEAT_MODE_REPEAT,
	  .shadow_xfer_clear   = 0U,
	  .dither_timer_period = 0U,
	  .dither_duty_cycle   = 0U,
	  .prescaler_mode	   = XMC_CCU4_SLICE_PRESCALER_MODE_NORMAL,
	  .mcm_enable		   = 0U,
	  .prescaler_initval   = slice->pre_scaler,
	  .float_limit		   = 0U,
	  .dither_limit		   = 0U,
	  .passive_level 	   = XMC_CCU4_SLICE_OUTPUT_PASSIVE_LEVEL_LOW,
	  .timer_concatenation = 0U
	};

	XMC_CCU4_EnableClock(slice->module_dev->ccu4_mod_dev,slice->slice_n);
	XMC_CCU4_StartPrescaler(slice->module_dev->ccu4_mod_dev);

	XMC_CCU4_SLICE_CompareInit(slice->chan_dev, &g_timer_object);

	XMC_CCU4_EnableShadowTransfer(slice->module_dev->ccu4_mod_dev, slice->shadow_mask);

}

uint16_t fast_100_scaller(uint16_t period,uint8_t power)
{
	uint32_t temp = (uint32_t)period;
	temp = temp*power*0x28F; //Floor(2^16/100)
	temp >>= 16;
	return CCU4_MIN(temp,period);
}


void init_pwm(CCU4_PWM_t *dev)
{
	init_slice(&dev->slice);
	init_gpio(&dev->pwm_pin,XMC_GPIO_MODE_OUTPUT_PUSH_PULL);
}

void enable_shadow(CCU4_PWM_t *dev)
{
	CCU4_slice_t *slice = &dev->slice;
	XMC_CCU4_EnableShadowTransfer(slice->module_dev->ccu4_mod_dev, slice->shadow_mask);
}


void start_pwm(CCU4_PWM_t *dev,uint16_t compare,uint16_t period)
{
	CCU4_CC4_TypeDef  *chan_dev = dev->slice.chan_dev;


	dev->current_period = period;
	compare = dev->current_period - compare;
	XMC_CCU4_SLICE_SetTimerPeriodMatch(chan_dev,period);
	//XMC_CCU4_SLICE_SetTimerCompareMatch(chan_dev,compare);

	XMC_CCU4_SLICE_ClearTimer(chan_dev);
	XMC_CCU4_SLICE_StartTimer(chan_dev);

	XMC_CCU4_SLICE_SetTimerCompareMatch(chan_dev,compare);
	enable_shadow(dev);

}

void stop_pwm(CCU4_PWM_t *dev)
{
	CCU4_CC4_TypeDef  *chan_dev = dev->slice.chan_dev;
	XMC_CCU4_SLICE_ClearTimer(chan_dev);
	XMC_CCU4_SLICE_StopTimer(chan_dev);
}


void update_pwm(CCU4_PWM_t *dev,uint16_t compare)
{
	CCU4_CC4_TypeDef  *chan_dev = dev->slice.chan_dev;
	compare = dev->current_period - compare;
	XMC_CCU4_SLICE_SetTimerCompareMatch(chan_dev,CCU4_MIN(compare,dev->current_period));
	enable_shadow(dev);
}

void update_pwm_power(CCU4_PWM_t *dev,uint8_t power)
{
	update_pwm(dev,fast_100_scaller(dev->current_period,power));
}


static void init_comp_slice(CCU4_slice_t *slice)
{
	XMC_CCU4_SLICE_CAPTURE_CONFIG_t g_timer_object =
	{
			.prescaler_initval = slice->pre_scaler,
	};


	XMC_CCU4_EnableClock(slice->module_dev->ccu4_mod_dev,slice->slice_n);
	XMC_CCU4_StartPrescaler(slice->module_dev->ccu4_mod_dev);

	XMC_CCU4_SLICE_CaptureInit(slice->chan_dev, &g_timer_object);

	XMC_CCU4_EnableShadowTransfer(slice->module_dev->ccu4_mod_dev, slice->shadow_mask);
}

void _capture_irq(CCU4_CAPTURE_t *dev)
{
	CCU4_CC4_TypeDef  *chan_dev = dev->slice.chan_dev;
	XMC_CCU4_SLICE_ClearEvent(chan_dev, XMC_CCU4_SLICE_IRQ_ID_EVENT0);
	if(dev->cb)
	{
		dev->cb();
	}
}

void init_capture(CCU4_CAPTURE_t *dev)
{
	CCU4_CC4_TypeDef  *chan_dev = dev->slice.chan_dev;
	init_comp_slice(&dev->slice);

	XMC_CCU4_SLICE_EVENT_CONFIG_t config = {
			.duration = XMC_CCU4_SLICE_EVENT_FILTER_7_CYCLES,
			.edge = XMC_CCU4_SLICE_EVENT_EDGE_SENSITIVITY_RISING_EDGE,
			.level = XMC_CCU4_SLICE_EVENT_LEVEL_SENSITIVITY_ACTIVE_HIGH,
			.mapped_input = dev->input,
	};

	init_gpio(&dev->pwm_pin,XMC_GPIO_MODE_INPUT_TRISTATE);

	XMC_CCU4_SLICE_ConfigureEvent(chan_dev,XMC_CCU4_SLICE_EVENT_0,&config);

	XMC_CCU4_SLICE_EnableEvent(chan_dev, XMC_CCU4_SLICE_IRQ_ID_EVENT0);

	XMC_CCU4_SLICE_SetInterruptNode(chan_dev, XMC_CCU4_SLICE_IRQ_ID_EVENT0, dev->irq_slice);

	NVIC_SetPriority(dev->irq_n,NVIC_EncodePriority(NVIC_GetPriorityGrouping(), dev->priority,0));

	NVIC_EnableIRQ(dev->irq_n);

	XMC_CCU4_SLICE_StartTimer(chan_dev);

}

void register_capture_cb(CCU4_CAPTURE_t *dev,void(*cb)(void))
{
	dev->cb = cb;
}


