#ifndef ABY_FILES_IO_H
#define ABY_FILES_IO_H

#include <stdio.h>

#ifdef __cplusplus
extern "C" {
    #endif

    void* read_file(const char* filename, size_t* size);
    void* write_file(const char* filename, size_t size);
    void mmap_free(void* data, size_t size);
    void mmap_sync_free(void* data, size_t size);

    #ifdef __cplusplus
}
#endif


#endif // ABY_FILES_IO_H