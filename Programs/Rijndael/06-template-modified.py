# Rijndael
# Sample template to show how to implement AES in Python

from sys import stdin
from hashlib import sha256
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode

# the AES block size to use
BLOCK_SIZE = 16
# the padding character to use to make the plaintext a multiple of BLOCK_SIZE in length
PAD_WITH = "#"
# the key to use in the cipher
KEY = b"rijndael"

# decrypts a ciphertext with a key
def decrypt(ciphertext, key):
	# hash the key (SHA-256) to ensure that it is 32 bytes long
	key = sha256(key).digest()
	# get the 16-byte IV from the ciphertext
	# by default, we put the IV at the beginning of the ciphertext
	iv = ciphertext[:16]

	# decrypt the ciphertext with the key using CBC block cipher mode
	cipher = AES.new(key, AES.MODE_CBC, iv)
	# the ciphertext is after the IV (so, skip 16 bytes)
	plaintext = cipher.decrypt(ciphertext[16:])
	# was ciphertext[16:]
	# ciphertext[16:].decode("utf-8","ignore")

	# remove potential padding at the end of the plaintext
	# figure this one out...
	# fix that relies on padded character being not used in plaintext
	toRemove = plaintext[-1]
	while plaintext[-1] == toRemove:
                plaintext = plaintext[:-1]

	return plaintext

# encrypts a plaintext with a key
def encrypt(plaintext, key):
	# hash the key (SHA-256) to ensure that it is 32 bytes long
	key = sha256(key).digest()
	# generate a random 16-byte IV
	iv = Random.new().read(BLOCK_SIZE)

	# encrypt the ciphertext with the key using CBC block cipher mode
	cipher = AES.new(key, AES.MODE_CBC, iv)
	# if necessary, pad the plaintext so that it is a multiple of BLOCK SIZE in length
	plaintext += ((BLOCK_SIZE - len(plaintext) % BLOCK_SIZE)+1) * PAD_WITH
	# add the IV to the beginning of the ciphertext
	# IV is at [:16]; ciphertext is at [16:]
	'''
	print(len(plaintext))
	print(len(bytes(plaintext.encode("utf-8","ignore"))))
	'''
	ciphertext = iv + cipher.encrypt(plaintext.encode("utf-8", "ignore"))

	return ciphertext

# MAIN
plaintext = stdin.read().rstrip("\n")
print("Plaintext:")
print(plaintext)
print()

ciphertext = encrypt(plaintext, KEY)
print("Ciphertext (encrypted with {}):".format(KEY))
print(ciphertext)
print()
print("Ciphertext (in binary):")
print(ciphertext.decode("utf-8", "ignore"))
print()
print("Ciphertext (encoded in base64):")
print(b64encode(ciphertext).decode("UTF-8", "ignore"))
print()

plaintext = decrypt(ciphertext, KEY)
print("Plaintext (decrypted with {}):".format(KEY))
print(plaintext)
print()
print("Plaintext (in ASCII):")
print(plaintext.decode("utf-8", "ignore"))
