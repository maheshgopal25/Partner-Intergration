import base64
from Cryptodome.Cipher import AES


class AESCipher(object):

    def __init__(self, iv, key):
        self.bs = AES.block_size
        self.iv = iv.encode()
        self.key = key.encode()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = self.iv
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = base64.b64encode(cipher.encrypt(raw.encode()))
        return encrypted

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:self.bs]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        obj = self._unpad(cipher.decrypt(enc[self.bs:])).decode('ascii')
        return '{"' + obj

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def hash(self, key):
        import hashlib
        result = hashlib.md5(key).hexdigest()
        return result
