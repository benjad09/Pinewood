/*
 * memsafe.h
 *
 *  Created on: Oct 7, 2022
 *      Author: Ben deVries
 */

#ifndef SOURCE_SRC_UTILS_MEMSAFE_H_
#define SOURCE_SRC_UTILS_MEMSAFE_H_


#include <stdlib.h>


static inline void *memsafe_malloc(size_t size)
{
	void *ret = malloc(size);
	//if(!ret){app_oops("malloc fail");};
	return ret;
}

static inline void *memsafe_calloc(size_t num, size_t size)
{
	void *ret = calloc(num,size);
	//if(!ret){app_oops("calloc fail");};
	return ret;
}

static inline void *memsafe_realloc( void *ptr, size_t new_size )
{
	void *ret = realloc(ptr,new_size);
	//if(!ret && new_size != 0){app_oops("realloc fail");};
	return ret;
}

static inline void memsafe_free(void **ptr)
{
	if(*ptr != NULL)
	{
		free(*ptr);
	}
	*ptr = NULL;
}


//This is a file for helping you be memory safe when doing dynamic memory calls


#endif /* SOURCE_SRC_UTILS_MEMSAFE_H_ */
