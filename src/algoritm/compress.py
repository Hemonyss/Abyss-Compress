from numpy.typing import NDArray
from src.tools import *
from numba import njit
from crc32c import crc32c
from os import path
import numpy as np


class Compressor:
    def __init__(self):
        self.version = 1
    
    @staticmethod
    @njit(fastmath=True, cache=True, nogil=True, looplift=True)
    def _rle_compress(file_data: NDArray[np.uint8], file_size: int):
        result = []
        i = 0
        
        while i < file_size:
            # Sequence search
            run_length = 1
            while i + run_length < file_size and file_data[i] == file_data[i + run_length] and run_length < 255:
                run_length += 1

            # Compression if the sequence is long enough
            if run_length >= 4:
                result.extend([0xFF, run_length, file_data[i]])
                i += run_length
                continue
                
            # Escaping the nearest source bytes 0xFF
            for j in range(run_length):
                val = file_data[i + j]
                if val == 0xFF:
                    result.extend([0xFF, 0x00])
                else:
                    result.append(val)

            i += run_length

        # Creating a NumPy array
        compressed = np.array(result, dtype=np.uint8)

        return compressed if compressed.size < file_size else file_data
    
    def _create_header(self, compress_path: str, file_size: str, crc32_data: int, is_compessed: bool):
        try:
            # Creating a header
            with open(f"{compress_path}", "wb") as file:
                # Magic number
                file.write(b"ABYS")
                # Is compressed
                file.write(bytes([is_compessed]))
                # Algoritm version
                file.write(self.version.to_bytes(1, "little"))
                # Compression mode ( In development )
                file.write(0x00.to_bytes(1, "little"))
                # Uncompressed file size
                file.write(file_size.to_bytes(8, "little"))
                # Uncompressed CRC32 control sum
                file.write(crc32_data.to_bytes(4, "little"))
                # Reserved bytes
                file.write(b"\x00" * 4)
        
        except Exception as e:
            return f"Error: {e}"
    
    def _read_file(self, file_path: str):
        try:
            return np.memmap(file_path, dtype=np.uint8, mode="r")
            
        except Exception as e:
            return f"Error: {e}"
    
    def compress_file(self, file_path: list | tuple | set | str, compress_path: str, compress_it: bool = True):
        """str only if there is one path"""
        try:
            # Create output path
            compress_path = f"{compress_path}.tar.aby"
            # validate file_path type
            if isinstance(file_path, str):
                file_path = [file_path]
            
            # Create tar in memmory
            file_data = tar_packer.create_tar(file_path)
            # Getting the file size
            file_size = file_data.size
            # Calculating the CRC32
            crc32_data = crc32c(file_data.tobytes())
            # File compression
            compress_file = self._rle_compress(file_data, file_size)

            # Write the original data if compression is ineffectictive or
            if compress_file.size >= file_size or not compress_it:
                self._create_header(compress_path, file_size, crc32_data, False)
                with open(f"{compress_path}", "ab") as file:
                    file.write(file_data)

                return

            # Writing the header and data
            self._create_header(compress_path, file_size, crc32_data, True)
            with open(f"{compress_path}", "ab") as file:
                file.write(compress_file)

        except Exception as e:
            return f"Error: {e}"
            

compressor = Compressor()

# "Cold start" protection
compressor._rle_compress(np.array([0], dtype=np.uint8), 1)
