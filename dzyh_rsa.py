import base64

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


# ------------------------生成密钥对------------------------
def create_rsa_pair(is_save=False):
    '''
    创建rsa公钥私钥对
    :param is_save: default:False
    :return: public_key, private_key
    '''
    f = RSA.generate(2048)
    private_key = f.exportKey("PEM")  # 生成私钥
    public_key = f.publickey().exportKey()  # 生成公钥
    if is_save:
        with open("crypto_private_key.pem", "wb") as f:
            f.write(private_key)
        with open("crypto_public_key.pem", "wb") as f:
            f.write(public_key)
    return public_key, private_key


def read_public_key(file_path="crypto_public_key.pem") -> bytes:
    with open(file_path, "rb") as x:
        b = x.read()
        return b


def read_private_key(file_path="crypto_private_key.pem") -> bytes:
    with open(file_path, "rb") as x:
        b = x.read()
        return b


# ------------------------加密------------------------
def encryption(text: str, public_key: bytes):
    # 字符串指定编码（转为bytes）
    text = text.encode('utf-8')
    # 构建公钥对象
    cipher_public = PKCS1_v1_5.new(RSA.importKey(public_key))
    # 加密（bytes）
    text_encrypted = cipher_public.encrypt(text)
    # base64编码，并转为字符串
    text_encrypted_base64 = base64.b64encode(text_encrypted).decode()
    return text_encrypted_base64


# ------------------------解密------------------------
def decryption(text_encrypted_base64: str, private_key: bytes):
    # 字符串指定编码（转为bytes）
    text_encrypted_base64 = text_encrypted_base64.encode('utf-8')
    # base64解码
    text_encrypted = base64.b64decode(text_encrypted_base64)
    # 构建私钥对象
    cipher_private = PKCS1_v1_5.new(RSA.importKey(private_key))
    # 解密（bytes）
    text_decrypted = cipher_private.decrypt(text_encrypted, Random.new().read)
    # 解码为字符串
    text_decrypted = text_decrypted.decode()
    return text_decrypted

	
if __name__ == '__main__':
	private_key = b'''-----BEGIN RSA PRIVATE KEY-----
MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBALbOds/iZZN4lFpU/4lJTYRdyyIQ/2u8A48x79XR21ZMbxiUc+hUYz1plccnd6ag1ks/A4Eb1Eu1bHEsGFmLtDSk/53WSlGavd7RH/upXUL3ZscoMIk/TVqfNPctNVGqQ1i8waUeDD+XrS86NwsKe4oJxCEdqF/vA2D6RZkRS9ZpAgMBAAECgYEAse+viFPXCT9SL8cSYGAgetoM8mDXLdd5I3W4/EhjldGaRbOiSp9xZYKTjqFk/qUJUX7Je29KKlMydco0/VxVj0vk1V4btHJcpCd/Q/im92vKQlUaZbtdbyutC7fI1IEsvrkxHunFCsgM0dlg9atJi0ovQmvG/kFFvovx3xI0inECQQD2WA9oJkrXubzCd3zy3ElLFkpWETYok5O9HcT25sIm4zhcFmjKc3u3cvz2gprojg1jvuE6yngZsIGchWoXwae9AkEAvfjWNXisMJLVPeoyFkXWfsVdYXOVmlnSRqNaLejFYpVaSn47dcz1FpYhA+3o1W3T5P73dBl0uGa54IUkgyWOHQJAUKdaO/41iNXOAFmAtj77XDMrGWy/L5/JwiRKBZBdxr+kBzprCsWunsxuGAOA1l0T8zFeqpH5qmeIuAdSSf7kfQJBALZ24jA7to91CNJONkuESrA6myV14jR9n2VvkrdTwvqcXzv7oNrVwHYwPofKo/8TXRmu9ziRFrXjHReUamx4ztUCQQDNqnYTFE4toqkrxPLSfH/0IXBX4yaUzt3IxoBUSac+uDu403sfcTELkP00cLY0YGvAKVfxKCah+uMc65OWsMu6
-----END RSA PRIVATE KEY-----'''
	text_encrypted_base64 = '''Hi5zL9E4rtzBiSxPosp+8g5MGg+tMFJhWzyBZVZHI5l3jmbvPUIxiE90f2iwKN5Mwas10zyuU38jQf9HinfQAelKTRWgWJPuXFmDhA39QGAkUBNECofs2lXNVsqJZSX4nv83ul3KZN5t3zpylYQF+gpmm4YUw8rasRTVU7UcOJk='''
	text_decrypted = decryption(text_encrypted_base64, private_key)
	print('密文：',text_decrypted)
	# '1SW3j8hpowd2Dy01'
