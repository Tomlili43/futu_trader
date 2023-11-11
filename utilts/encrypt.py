def encrypt(original_string):
    byte_array = bytearray(original_string, 'utf-8')
    for i in range(0, len(byte_array)):
        byte_array[i] = byte_array[i] ^ 0x7f
    text = byte_array.decode('utf-8')
    return text

def decrypt(encrypt_string):
    byte_array = bytearray(encrypt_string, 'utf-8')
    for i in range(0, len(byte_array)):
        byte_array[i] = byte_array[i] ^ 0x7f
    text = byte_array.decode('utf-8')
    return text
