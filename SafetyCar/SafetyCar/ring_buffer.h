/*
 * Copyright (C) 2018 Infineon Technologies AG. All rights reserved.
 *
 * Infineon Technologies AG (Infineon) is supplying this software for use with
 * Infineon's microcontrollers.
 * This file can be freely distributed within development tools that are
 * supporting such microcontrollers.
 *
 * THIS SOFTWARE IS PROVIDED "AS IS". NO WARRANTIES, WHETHER EXPRESS, IMPLIED
 * OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE.
 * INFINEON SHALL NOT, IN ANY CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL,
 * OR CONSEQUENTIAL DAMAGES, FOR ANY REASON WHATSOEVER.
 *
 */

#ifndef RING_BUFFER_H
#define RING_BUFFER_H




//helpfull macro for declaring RING_BUFFER
#define RING_BUFFER_DEF(x, sz)\
	uint8_t x##_data[sz];\
	ring_buffer_t x = {\
	  .buffer = x##_data,\
      .head = 0,\
	  .tail = 0,\
	  .len = sz\
	}

typedef struct ring_buffer
{
  uint8_t *buffer; //Pointer to array that holds data
  volatile uint32_t head; //location of the last pushed byte
  volatile uint32_t tail; //location of the last pulled byte
  const uint32_t len;//size of the buffer
} ring_buffer_t;

/**
 * @brief resets the buffer
 *
 * @param rb - rolling buffer device
 *
 */
void ring_buffer_init(ring_buffer_t *const rb);



/**
 * @brief puts a number in the buffer
 *
 * @param rb - rolling buffer device
 *
 * @param c data byte getting added to buffer
 *
 * @ret 0 on sucsess
 * @ret -1 on fULL buffer
 *
 */
int32_t ring_buffer_put(ring_buffer_t *const rb, uint8_t c);



/**
 * @brief pull a number out of the buffer
 *
 * @param rb - rolling buffer device
 *
 * @param *c data byte getting added to buffer
 *
 * @ret 0 on sucsess
 * @ret -1 if buffer is empty
 *
 */
int32_t ring_buffer_get(ring_buffer_t *const rb, uint8_t *const c);


/**
 * @brief checks if the buffer is empty
 *
 * @param rb - rolling buffer
 *
 * @ret true if the buffer has no items in it
 * @ret false if the buffer has items in it
 *
 */
__STATIC_INLINE bool ring_buffer_is_empty(ring_buffer_t *const rb)
{
  uint32_t head = rb->head;
  uint32_t tail = rb->tail;
  return (head == tail);
}

/**
 * @brief empties the buffer
 *
 * @param rb - rolling buffer
 *
 */
__STATIC_INLINE void ring_buffer_flush(ring_buffer_t *const rb)
{
	rb->tail = rb->head;
}


/**
 * @brief checks if the buffer is full
 *
 * @param rb - rolling buffer
 *
 * @ret true if the buffer is full
 * @ret false if the buffer has space
 *
 */
__STATIC_INLINE bool ring_buffer_is_full(ring_buffer_t *const rb)
{
  uint32_t head = rb->head;
  uint32_t tail = rb->tail;
  return (((head + 1) % rb->len) == tail);
}


/**
 * @brief checks how many items are in the ring buffer
 *
 * @param rb - rolling buffer
 *
 * @return amount of items in buffer
 */
__STATIC_INLINE uint32_t ring_buffer_avail(ring_buffer_t *const rb)
{
  uint32_t head = rb->head;
  uint32_t tail = rb->tail; 
  return (head - tail) % rb->len;
}

#endif
