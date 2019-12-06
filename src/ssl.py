# a bunch of assorted function for various keys and generations
# comment/uncomment/use whatever you'd like to
#
# Use cryptography module, do NOT use crypto,pycrypto or that kind of stuff
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Private/Public key pair
key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=2048)

# BEGIN/END RSA PRIVATE KEY
keyPrivate = key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption())
# BEGIN/END PRIVATE KEY
keyPrivate = key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption())

# Public key, RSA PEM container format
# BEGIN/END RSA PUBLIC KEY
keyPublic = key.public_key().public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.PKCS1)
# BEGIN/END PUBLIC KEY
keyPublic = key.public_key().public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo)
# ssh-rsa [OpenSSL format]
keyPublic = key.public_key().public_bytes(
                        encoding=serialization.Encoding.OpenSSH,
                        format=serialization.PublicFormat.OpenSSH)

# decode to printable strings
keyPrivateStr = keyPrivate.decode('utf-8')
keyPublicStr  = keyPublic.decode('utf-8')

print('Private key = {}'.format(keyPrivateStr))
print('Public  key = {}'.format(keyPublicStr))
