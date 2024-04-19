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

#define MAX_DEPTH 16

typedef struct LedCommand {
	uint16_t value;
	uint16_t holdtime;
}LedCommand_t;

typedef struct LedSequence {
	LedCommand_t *const commands;
	const size_t len;
	const size_t repeats;
	size_t index;
	size_t loop;
	uint32_t timeout;
	uint16_t valueout;
	struct LedSequence *next;
}LedSequence_t;

void start_Lsequence_OneShot(LedSequence_t *seq);

void start_Lsequence(LedSequence_t *seq);

void start_Lsequence_forever(LedSequence_t *seq);

bool update_Lsequence(LedSequence_t *seq);

uint16_t get_Lsequence(LedSequence_t *seq);

void link_Lsequence(LedSequence_t *seq,LedSequence_t *seq2);

#define COMMAND_DEF(setVal,holdMs)	{.value = setVal,.holdtime = holdMs}

#define SEQUENCE_DEF(name,commandArray,seqrepeats)						\
		LedSequence_t name = {											\
				.commands = &commandArray,								\
				.len = sizeof(commandArray)/sizeof(LedCommand_t),		\
				.repeats = seqrepeats,									\
				}



#endif /* LEDSEQ_H_ */
