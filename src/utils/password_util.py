import hashlib


def encrypt_password(password, noise='smart_stock*&!#'):
    """密码加密"""
    # 使用 hashlib 中的 md5() 函数创建 MD5 哈希对象
    md5_hash = hashlib.md5()
    password = password + noise
    # 更新哈希对象的值，将密码编码为 utf-8 格式
    md5_hash.update(password.encode('utf-8'))
    # 获取 MD5 加密后的密码的十六进制表示
    encrypted_password = md5_hash.hexdigest()

    return encrypted_password
