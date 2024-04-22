
#include "ledSeq.h"
#include "uptime.h"



void start_Lrunner_OneShot(LedRunner_t *run,LedSequence_t *head)
{


}

void start_Lrunner(LedRunner_t *run,LedSequence_t *head)
{
	run->seq = head;
	run->index = 0;
	run->loop = 0;
	run->timeout = 0;
	run->valueout = run->seq->commands[0].value;
	run->is_running = true;
}

void start_Lrunner_forever(LedRunner_t *run,LedSequence_t *head);

bool update_Lrunner(LedRunner_t *run,uint32_t uptime)
{
	if((uptime > run->timeout)&&run->is_running)
	{
		run->valueout = run->seq->commands[run->index].value;
		run->timeout = uptime+run->seq->commands[run->index].holdtime;
		run->index++;
		if(run->index >= run->seq->len)
		{
			run->index = 0;
			run->loop++;
			if(run->loop >= run->seq->repeats)
			{
				run->loop = 0;
				if(run->seq->next != NULL)
				{
					run->seq = run->seq->next;
				}
				else
				{
					run->is_running = false;
				}
			}
		}
		return true;
	}
	return false;
}

uint16_t get_LrunnerVal(LedRunner_t *run)
{
	return(run->valueout);
}

void link_seq(LedSequence_t *head,LedSequence_t *next)
{
	head->next = next;
}
