/*
 * uptime.h
 *
 *  Created on: May 2, 2023
 *      Author: Ben deVries
 */

#ifndef SOURCE_BOOT_SHARED_UPTIME_H_
#define SOURCE_BOOT_SHARED_UPTIME_H_
#include <stdint.h>
#include <stdbool.h>

uint32_t uptime_get(void); // Ok so a 32 bit uptime counter rolls over in 49 days. if the IG has been on for more than 49 days we have bigger problems

void inc_uptime(void);

void busy_wait(uint32_t us);

void busy_wait_ms(uint32_t ms);

typedef struct uptime_timer
{
	uint32_t period;
	uint32_t timeout;
	uint32_t start;
}uptime_timer_t;

void start_timer(uptime_timer_t *timer,uint32_t period);

void reset_timer(uptime_timer_t *timer);

bool timer_timeouted(uptime_timer_t *timer);

bool timer_check_and_reset(uptime_timer_t *timer);

uint32_t timer_get_elapsed(uptime_timer_t *timer);





#endif /* SOURCE_BOOT_SHARED_UPTIME_H_ */
