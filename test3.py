from cryptography.fernet import Fernet
 
# we will be encrypting the below string.
message = "hello geeks welcome to python"
 
# generate a key for encryption and decryption
# You can use fernet to generate
# the key or use random key generator
# here I'm using fernet to generate key
 
key = Fernet.generate_key()
 
# Instance the Fernet class with the key
 
fernet = Fernet(key)
 
# then use the Fernet class instance
# to encrypt the string string must
# be encoded to byte string before encryption

encMessage = fernet.encrypt(message.encode())
 
print("original string: ", message)
print("encrypted string: ", encMessage)
 
# decrypt the encrypted string with the
# Fernet instance of the key,
# that was used for encrypting the string
# encoded byte string is returned by decrypt method,
# so decode it to string with decode methods

#encMessage=b'gAAAAABjoY66u7ez3iyLdE4EEITqmIW6roMZ_4ebe9IkmHwiIb5TnJsW5JZDiZzUL8iPtrPC2oOGuOdrL4eflWh75uGXoXRAwYzjKN0UKZTCR4y24W3ULNY='
decMessage = fernet.decrypt(encMessage).decode()
 
print("decrypted string: ", decMessage)
