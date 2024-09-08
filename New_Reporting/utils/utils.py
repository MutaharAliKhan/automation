import os
import json
import random
import socket
import string
from conftest import PROJECT_ROOT


def get_root_path_join(*sub_paths):
    return os.path.join(PROJECT_ROOT, *sub_paths)


def get_system_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        print("Error:", e)
        return None


def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def generate_random_cnic():
    five = str(random.randint(10000, 99999))
    seven = str(random.randint(1000000, 9999999))
    one = str(random.randint(0, 9))
    random_cnic = f"{five}-{seven}-{one}"
    return random_cnic


def generate_random_number(minimum, maximum):
    return random.randint(minimum, maximum)
