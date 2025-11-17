from numpy.typing import NDArray
from numba import njit
from os import path
from zlib import crc32
import numpy as np

class Decompress:
    def __init__(self):
        pass
    
    def _read_header(self, file_path: str):
        try:
            # Reading the header
            with open(file_path, "rb") as file:
                # Magic number
                magic = file.read(4).decode()
                # Is the file compressed
                is_compress = int.from_bytes(file.read(1), "little")
                # Algoritm version
                version = int.from_bytes(file.read(1), byteorder="little")
                # Compression mode ( In development )
                mode = int.from_bytes(file.read(1), byteorder="little")
                # size of the decompressed file
                decompress_size = int.from_bytes(file.read(8), byteorder="little")
                # CRC32 control sum
                crc32 = int.from_bytes(file.read(4), byteorder="little")
                # Reserved bytes
                reserved = file.read(4)

            return magic, version, decompress_size, crc32, mode, is_compress, reserved
        
        except Exception as e:
            return f"Error: {e}"

    def _read_file(self, file_path: str):
        try:
            return np.memmap(file_path, dtype=np.uint8, mode="r")[23:]

        except Exception as e:
            return f"Error: {e}"
    
    @staticmethod
    @njit(fastmath=True, cache=True, nogil=True, looplift=True, parallel=True)
    def _decompress(file_data: NDArray[np.uint8], file_size: int):
        decompress_data = np.zeros(file_size, dtype=np.uint8)
        i = 0
        pos = 0
        data_size = file_data.size

        while i < data_size and pos < file_size:
            # Checking whether a byte is uncompressed
            if file_data[i] != 0xFF:
                decompress_data[pos] = file_data[i]
                i += 1
                pos += 1
                continue
            
            next_byte = file_data[i+1]
            # If the byte is 0xFF, check if it is escaped
            if next_byte == 0x00:
                decompress_data[pos] = 0xFF
                i += 2
                pos += 1
                continue
            
            # If the byte is not escaped, then unpack the data
            value = file_data[i+2]
            for _ in range(next_byte):
                decompress_data[pos] = value
                pos += 1
            i += 3
        
        return decompress_data

    def decompress_file(self, file_path: str, decompress_path: str):
        header_data = self._read_header(file_path)

        # Check file exist
        if not path.exists(file_path):
            return "File not exist"

        # Check magic number
        if header_data[0] != "ABYS":
            return "Incorrect magic number"
        
        # Reading a compress file
        compress_data = self._read_file(file_path)

        # If the file is not compressed
        if header_data[5] == 0:
            try:
                with open(decompress_path, "wb") as file:
                    file.write(compress_data)
                
            except Exception as e:
                return f"Error: {e}"
        # Decompressing a compress file
        decompress_data = self._decompress(compress_data, header_data[2])
        # Calculating rc32 for unpacked data
        decompress_crc32 = crc32(decompress_data)

        # Checking the correctness of unpacking
        if decompress_crc32 != header_data[3]:
            return "Incorrect CRC32"
            
        try:
            with open(decompress_path, "wb") as file:
                file.write(decompress_data)
                
        except Exception as e:
            return f"Error: {e}"


decompressor = Decompress()

# "Cold start" protection
decompressor._decompress(np.array([0], dtype=np.uint8), 1)
