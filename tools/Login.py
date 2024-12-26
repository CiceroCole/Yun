import random
import time
import sys
from gmssl import sm4
import hashlib
import base64
import requests
from Crypto.Util.Padding import pad, unpad
import json
import configparser

SM4_BLOCK_SIZE = 16
conf = configparser.ConfigParser()


class Login:
    def md5_encryption(data):
        md5 = hashlib.md5()  # 创建一个md5对象
        md5.update(data.encode("utf-8"))  # 使用utf-8编码数据
        return md5.hexdigest()  # 返回加密后的十六进制字符串

    def hex_to_bytes(hex_str):
        return bytes.fromhex(hex_str)

    def pkcs7_padding(data):
        return pad(data, SM4_BLOCK_SIZE)

    def pkcs7_unpadding(data):
        return unpad(data, SM4_BLOCK_SIZE)

    def sm4_encrypt(
        plaintext, key, iv=None, mode="ECB", padding="Pkcs7", output_format="Base64"
    ):
        crypt_sm4 = sm4.CryptSM4()
        key = Login.hex_to_bytes(key)
        # 设置加密模式
        if mode == "ECB":
            crypt_sm4.set_key(key, sm4.SM4_ENCRYPT)
        elif mode == "CBC":
            iv = Login.hex_to_bytes(iv) if iv else None
            crypt_sm4.set_key(key, sm4.SM4_ENCRYPT, iv)
        # 数据填充
        if padding == "Pkcs7":
            plaintext = Login.pkcs7_padding(plaintext.encode())
        # 加密操作
        if mode == "ECB":
            ciphertext = crypt_sm4.crypt_ecb(plaintext)
        elif mode == "CBC":
            ciphertext = crypt_sm4.crypt_cbc(plaintext)
        # 输出格式转换
        if output_format == "Base64":
            return base64.b64encode(ciphertext).decode()
        elif output_format == "Hex":
            return ciphertext.hex()

    def sm4_decrypt(
        ciphertext, key, iv=None, mode="ECB", padding="Pkcs7", input_format="Base64"
    ):
        crypt_sm4 = sm4.CryptSM4()
        key = Login.hex_to_bytes(key)
        # 设置解密模式
        if mode == "ECB":
            crypt_sm4.set_key(key, sm4.SM4_DECRYPT)
        elif mode == "CBC":
            iv = Login.hex_to_bytes(iv) if iv else None
            crypt_sm4.set_key(key, sm4.SM4_DECRYPT, iv)
        # 输入格式转换
        if input_format == "Base64":
            ciphertext = base64.b64decode(ciphertext)
        elif input_format == "Hex":
            ciphertext = bytes.fromhex(ciphertext)
        # 解密操作
        if mode == "ECB":
            plaintext = crypt_sm4.crypt_ecb(ciphertext)
        elif mode == "CBC":
            plaintext = crypt_sm4.crypt_cbc(ciphertext)
        # 数据去填充
        # if padding == 'Pkcs7':
        # plaintext = pkcs7_unpadding(plaintext)
        return plaintext.decode()

    def main():

        utc = int(time.time())
        # 读取ini
        conf.read("./config.ini", encoding="utf-8")

        # 判断[Login]是否存在
        if "Login" not in conf.sections():
            conf.add_section("Login")
            conf.set("Login", "username", "")
            conf.set("Login", "password", "")
            with open("./config.ini", "w", encoding="utf-8") as f:
                conf.write(f)

        # 判断school_id是否在[Yun]中
        if "school_id" not in conf["Yun"]:
            # 合工大 100
            # conf.set("Yun", "school_id", "100")
            # 三联学院 125
            conf.set("Yun", "school_id", "125")
            with open("./config.ini", "w", encoding="utf-8") as f:
                conf.write(f)

        # 读取ini配置
        if conf.get("Login", "username"):
            username = conf.get("Login", "username")
            password = conf.get("Login", "password")
        else:
            username = input("请输入用户账号: ")
            password = input("请输入用户密码: ")

        DeviceId = conf.get("User", "device_id") or str(
            random.randint(10e14, 10e15 - 1)
        )
        DeviceName = conf.get("User", "device_name") or random.choice(
            ["Xiaomi", "Huawei", "Vivo", "Oppo", "Meizu", "Samsung", "Honor"]
        )
        uuid = conf.get("User", "uuid") or DeviceId
        sys_edition = conf.get("User", "sys_edition") or str(random.randint(10, 14))
        appedition = conf.get("Yun", "app_edition")
        # 合工大登录账号专有链接
        # url = "http://" + conf.get("Yun", "school_host") + "/login/appLoginHGD"
        # 安徽三联学院登录账号链接
        school_host = conf.get("Yun", "school_host")
        url = "http://" + school_host + "/login/appLogin"
        platform = conf.get("Yun", "platform") or "android"
        schoolid = conf.get("Yun", "school_id")
        # 如果部分配置为空则随机生成
        # md5签名结果用hex
        encryptData = str(
            {
                "userName": username,
                "password": password,
                "schoolId": schoolid,
                "type": "1",
            }
        ).replace("'", '"')
        print("encryptData: ", encryptData)
        # 签名结果
        AppSecret = "pie0hDSfMRINRXc7s1UIXfkE"
        sign_data = "platform={}&utc={}&uuid={}&appsecret={}".format(
            platform, utc, uuid, AppSecret
        )
        sign = Login.md5_encryption(sign_data)
        key = "e2c9e15e84f93b81ee01bbd299a31563"
        content = Login.sm4_encrypt(
            encryptData, key, mode="ECB", padding="Pkcs7", output_format="Base64"
        )
        headers = {
            "token": "",
            "isApp": "app",
            "deviceId": uuid,
            "deviceName": DeviceName,
            "version": appedition,
            "platform": platform,
            "uuid": uuid,
            "utc": str(utc),
            "sign": sign,
            "Content-Type": "application/json; charset=utf-8",
            "Host": school_host,
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.0",
        }
        content = content[:-24]
        # 请求体内容
        data = {
            "cipherKey": "BL+FHB2+eDL3gMtv1+2UljBFraZYQFOXkmyKrqyRAzcw1R4rsq1i8p1tEOXhZMHTlFWmR+i/mdf4DNi0hCUSoQ88JMTUSUIkgU0+mowqRlVc/n/qYGqXERFqyMqn+GANUvWU65+F6/RLhpAB3AiYSJOY/RplvXmRvQ==",
            "content": content,
        }
        # 发送POST请求
        try:
            response = requests.post(url, headers=headers, json=data)
        except requests.exceptions.ConnectionErro as e:
            print("网络异常，请检查网络连接")
            return False
        # 打印响应内容
        result = response.text
        # print(result)
        rawResponse = json.dumps(json.loads(result))
        if rawResponse.find("500") != -1:
            print("返回数据报错 检查账号密码!")
            sys.exit()
        else:
            DecryptedData = json.loads(
                Login.sm4_decrypt(
                    result, key, mode="ECB", padding="Pkcs7", input_format="Base64"
                )
            )
            # print(DecryptedData)
        try:
            token = DecryptedData["data"]["token"]
        except KeyError:
            print("登录失败，请检查账号密码是否正确")
            sys.exit(0)
        if response.status_code == 200:
            conf.set("Login", "username", username)
            conf.set("Login", "password", password)
            with open("./config.ini", "w", encoding="utf-8") as f:
                conf.write(f)
            print(f"{'==='*10}登录成功!{'==='*10}\n")
            print(f"{'>>>'*10} 请注意 {'<<<'*10}\n")
            print("!!!使用脚本登录后会导致手机客户端登录失效!!!")
            print("!!!请尽量减少手机登录次数，避免被识别为多设备登录代跑!!!")
        return token, DeviceId, DeviceName, uuid, sys_edition
