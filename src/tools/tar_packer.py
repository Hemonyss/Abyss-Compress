from pathlib import Path
from io import BytesIO
from numpy import frombuffer, uint8
import tarfile

def create_tar(file_paths: list):
    buffer = BytesIO()

    with tarfile.open(fileobj=buffer, mode='w') as tar:
        for file in file_paths:
            file_name = Path(file).name
            tar.add(file, arcname=file_name)

    tar_bytes = buffer.getvalue()
    buffer.close()

    return tar_bytes

def read_tar(tar_bytes: bytes):
    buffer = BytesIO(tar_bytes)
    file_dict = dict()

    with tarfile.open(fileobj=buffer, mode='r') as tar:
        for member in tar.getmembers():
            member_data = tar.extractfile(member.name).read()
            if not member_data:
                return file_dict
            
            file_dict[member.name] = frombuffer(member_data, dtype=uint8)
    
    buffer.close()
    
    return file_dict
