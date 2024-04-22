/*
 * ledSeq.h
 *
 *  Created on: Apr 19, 2024
 *      Author: Ben deVries
 */

#ifndef LEDSEQ_H_
#define LEDSEQ_H_

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#define MAX_DEPTH 16

typedef struct LedCommand {
	uint16_t value;
	uint16_t holdtime;
}LedCommand_t;

typedef struct LedSequence {
	const LedCommand_t *commands;
	const size_t len;
	const size_t repeats;
	struct LedSequence *next;
}LedSequence_t;

typedef struct LedRunner
{
	LedSequence_t *seq;
	size_t index;
	size_t loop;
	uint32_t timeout;
	uint16_t valueout;
	bool is_running;
}LedRunner_t;

void start_Lrunner_OneShot(LedRunner_t *run,LedSequence_t *head);

void start_Lrunner(LedRunner_t *run,LedSequence_t *head);

void start_Lrunner_forever(LedRunner_t *run,LedSequence_t *head);

bool update_Lrunner(LedRunner_t *run,uint32_t uptime);

uint16_t get_LrunnerVal(LedRunner_t *run);

void link_seq(LedSequence_t *head,LedSequence_t *next);

#define COMMAND_DEF(setVal,holdMs)	{.value = setVal,.holdtime = holdMs}

#define SEQUENCE_DEF(name,commandArray,seqrepeats)						\
		LedSequence_t name = {											\
				.commands = commandArray,								\
				.len = sizeof(commandArray)/sizeof(LedCommand_t),		\
				.repeats = seqrepeats,									\
				}



#endif /* LEDSEQ_H_ */
