

#include "Uptime.h"
#include "Stdint.h"


static volatile uint32_t master_uptime = 0;

void busy_wait(uint32_t us)
{
	us /= 2;
	__asm volatile("cmp %[us_r],#0\t\n"
				   "beq busy_wait_3\t\n"
				   "busy_wait_1:\t\n"
				   "mov r2,#16\t\n"
				   "busy_wait_2:\t\n"
			       "sub r2,#1\t\n"
				   "cmp r2,#0\t\n"
				   "bne busy_wait_2\t\n"
				   "sub     %[us_r], #1\t\n"              //1 cycle
				   "cmp     %[us_r], #0\t\n"              //1 cycle
				   "bne     busy_wait_1\t\n"    //2 cycles if branching
				   "busy_wait_3:\t\n"

					: /*empty result*/
					: [us_r] "r" (us));
}


void busy_wait_ms(uint32_t ms)
{

	uint32_t timeout = uptime_get()+ms;
	while(timeout > uptime_get())
	{
		__asm volatile("nop\t\n");
	}
}


uint32_t uptime_get(void)
{
	return master_uptime;
}

void inc_uptime(void)
{
	master_uptime++;
}


void start_timer(uptime_timer_t *timer,uint32_t period)
{
	timer->period = period;
	timer->start = uptime_get();
	timer->timeout = timer->start+timer->period;

}

void reset_timer(uptime_timer_t *timer)
{
	timer->start = uptime_get();
	timer->timeout = timer->start+timer->period;
}

bool timer_timeouted(uptime_timer_t *timer)
{
	return(uptime_get()>=timer->timeout);
}

bool timer_check_and_reset(uptime_timer_t *timer)
{
	if(timer_timeouted(timer))
	{
		reset_timer(timer);
		return true;
	}
	return false;
}

uint32_t timer_get_elapsed(uptime_timer_t *timer)
{
	return (uptime_get()-timer->start);
}
