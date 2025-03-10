import pyaes, pbkdf2, binascii, os, secrets

# Derive a 256-bit AES encryption key from the password
#password = "s3cr3t*c0d3"
password="krishna"
passwordSalt = os.urandom(16)
key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
#print('AES encryption key:', binascii.hexlify(key))

# Encrypt the plaintext with the given key:
#   ciphertext = AES-256-CTR-Encrypt(plaintext, key, iv)
iv = secrets.randbits(256)
#plaintext = "Text for encryption"
plaintext = "Krishna"

aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
ciphertext = aes.encrypt(plaintext)
print(ciphertext)
#print('Encrypted:', binascii.hexlify(ciphertext))

ee=binascii.hexlify(ciphertext)
enc=ee.decode()
print(enc)



# Decrypt the ciphertext with the given key:
#   plaintext = AES-256-CTR-Decrypt(ciphertext, key, iv)
aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
decrypted = aes.decrypt(ciphertext)
print('Decrypted:', decrypted)
dd=decrypted.decode()
print(dd)
