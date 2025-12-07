from pathlib import Path
from io import BytesIO
from numpy import frombuffer, uint8
import tarfile

def create_tar(file_paths: list | tuple | set | str) -> bytes: 
    """str only if there is one path"""
    buffer = BytesIO()

    if isinstance(file_paths, str):
        file_paths = [file_paths]

    with tarfile.open(fileobj=buffer, mode='w') as tar:
        for file in file_paths:
            file_name = Path(file).name
            tar.add(file, arcname=file_name)

    tar_bytes = buffer.getvalue()
    buffer.close()

    return frombuffer(tar_bytes, dtype=uint8)

def read_tar(tar_bytes: bytes) -> dict:
    buffer = BytesIO(tar_bytes)
    file_dict = dict()

    with tarfile.open(fileobj=buffer, mode='r') as tar:
        for member in tar.getmembers():
            member_data = tar.extractfile(member.name).read()
            if not member_data:
                return file_dict
            
            file_dict[member.name] = member_data
    
    buffer.close()
    
    return file_dict
