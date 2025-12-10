#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include "../include/files_io.h"

void* read_file(const char *filename, size_t* size) {
    int fd = open(filename, O_RDONLY);
    if (fd == -1) return NULL;
    struct stat st;
    if (fstat(fd, &st) == -1) {
        fprintf(stderr, "fstat error!");
        close(fd);
        return NULL;
    }

    *size = st.st_size;
    if (*size == 0) {
        fprintf(stderr, "file size is zero!");
        close(fd);
        return NULL;
    }

    void* data = mmap(NULL, *size, PROT_READ, MAP_PRIVATE, fd, 0);
    close(fd);

    return data == MAP_FAILED ? NULL : data;
}

void* write_file(const char* filename, size_t size) {
    int fd = open(filename, O_RDWR | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) return NULL;

    if (ftruncate(fd, size) == -1) {
        close(fd);
        return NULL;
    }

    void* data = mmap(NULL, size, PROT_READ | PROT_WRITE , MAP_SHARED, fd, 0);
    close(fd);

    return data == MAP_FAILED ? NULL : data;
}

void mmap_free(void* data, size_t size) {
    if (data) munmap(data, size);
}

void mmap_sync_free(void* data, size_t size) {
    if (data) {
        msync(data, size, MS_SYNC);
        munmap(data, size);
    }
}