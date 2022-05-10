##################################
# Group Name:   Team Hightower
# Members:      Cori Albritton, Megan Cox, Peter Ford, Timothy Oliver
# Assignment:   Program 6 - Rijndael (AES)
# Date:         11 May 2022
# Note:         This code is essentially a filled program 06 template.
#                The decrypt function has a block to remove padded characters from the plaintext.
#                The plaintext padding in encrypt also has a small change (...+PADS...) so that it can work with the input files easily
##################################

from sys import stdin, stdout
from hashlib import sha256
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode

# the AES block size to use
BLOCK_SIZE = 16
# the padding character to use to make the plaintext a multiple of BLOCK_SIZE in length
PAD_WITH = "#"
# the key to use in the cipher
KEY = b"heartburn" #b"rijndael"


# decrypts a ciphertext with a key
def decrypt(ciphertext, key):
        '''
        # lines to determine which characters of input are undecipherable (into Unicode)
        print(f"length of ciphertext: {len(ciphertext)}")
        print(f"\n\nciphertext:\n{(ciphertext)}\n\n")
        for i in range(len(ciphertext)):
                print(f"character {i} of ciphertext:\n{ciphertext[i]}\n")
                print (f"in bytes:\n{ciphertext[i].encode('utf-8')}\n\n")
        print(f"length of encoded ciphertext: {len(ciphertext.encode('utf-8'))}")
        '''
        # hash the key (SHA-256) to ensure that it is 32 bytes long
        key2 = sha256(key).digest()
	# get the 16-byte IV from the ciphertext
	# by default, we put the IV at the beginning of the ciphertext
        iv = ciphertext[:16]

	# decrypt the ciphertext with the key using CBC block cipher mode
        cipher = AES.new(key2, AES.MODE_CBC, iv)
	# the ciphertext is after the IV (so, skip 16 bytes)
        plaintext = cipher.decrypt(ciphertext[16:])
	# was ciphertext[16:]
	# ciphertext[16:].decode("utf-8","ignore")

	# remove potential padding at the end of the plaintext
	# figure this one out...
	# fix that relies on padded character being not used in plaintext
        toRemove = ord(PAD_WITH)
        while plaintext[-1] == toRemove:
                plaintext = plaintext[:-1]

        return plaintext

# encrypts a plaintext with a key
def encrypt(plaintext, key):
        padded = False
        PADS = 0 # variable to give extra pads to plaintext
                 #  (got ValueError for size of data in text files (06a-c, e) and needed to add 1)
	# hash the key (SHA-256) to ensure that it is 32 bytes long
        key = sha256(key).digest()
	# generate a random 16-byte IV
        iv = Random.new().read(BLOCK_SIZE)

	# encrypt the ciphertext with the key using CBC block cipher mode
        cipher = AES.new(key, AES.MODE_CBC, iv)
	# if necessary, pad the plaintext so that it is a multiple of BLOCK SIZE in length
        plaintext += ((BLOCK_SIZE - len(plaintext) % BLOCK_SIZE)+PADS) * PAD_WITH
        '''
        while not(padded):
                try:
                        plaintext += ((BLOCK_SIZE - len(plaintext) % BLOCK_SIZE)+PADS) * PAD_WITH
                        padded = True
                except ValueError:
                        PADS+=1
                        print("here")
        '''
                        
	# add the IV to the beginning of the ciphertext
	# IV is at [:16]; ciphertext is at [16:]
	
        ciphertext = iv + cipher.encrypt(plaintext.encode("utf-8","ignore")) #"utf-8","ignore" OR "utf-7"

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
print(plaintext.decode("utf-8", "ignore")) # "utf-8", "ignore"

