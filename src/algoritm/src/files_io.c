#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
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

void* write_file(const char* filename, const void* data, size_t size) {
    int fd = open(filename, O_RDWR | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) return NULL;

    ssize_t written = write(fd, data, size);
    close(fd);

    return (written == (ssize_t)size) ? 0 : -1;
}

void mmap_free(void* data, size_t size) {
    if (data) munmap(data, size);
}