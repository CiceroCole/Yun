# 自动获取token等信息，点进跑步信息自动保存跑步记录tasklist
# 安装mitmproxy 运行mitmweb -s proxy.py
# 手机代理设置为电脑ip:8080
# 这个会自动创建新的config_studentnumber.ini
import os
import sys
import mitmproxy
import json
import subprocess
import configparser

sys.path.append("..")
from main import *

# default_url = "210.45.246.53:8080"
# 合工大主机地址
# 加载配置文件
conf = configparser.ConfigParser()
conf.read("../config.ini", encoding="utf-8")
default_url = conf.get("Yun", "school_host")  # 学校的host
tasks_path = (
    "/".join(os.path.abspath(__file__).replace("\\", "/").split("/")[:-2]) + "/tasks"
)


def decode(key_enc, data, use_gzip):

    use_gzip_str = str(use_gzip).lower()
    java_path = "java.exe"
    # java_path = "D:/Environment/Java/JDK/17/bin/java.exe"
    classpath = ";".join(
        [
            os.path.abspath(p)
            for p in [
                "./classes",
                "./jars/cn/hutool/hutool-all/5.6.0/hutool-all-5.6.0.jar",
                "./jars/com/jgoodies/jgoodies-common/1.8.1/jgoodies-common-1.8.1.jar",
                "./jars/org/bouncycastle/bcprov-jdk15on/1.69/bcprov-jdk15on-1.69.jar",
                "./jars/org/bouncycastle/bcpkix-jdk15on/1.69/bcpkix-jdk15on-1.69.jar",
                "./jars/org/bouncycastle/bcutil-jdk15on/1.69/bcutil-jdk15on-1.69.jar",
            ]
        ]
    )
    # prime_args = " ".join()
    # print(prime_args)
    process = subprocess.Popen(
        [
            java_path,
            "-Dfile.encoding=UTF-8",
            "-classpath",
            classpath,
            "org.decrypt.App",
        ],
        stdin=subprocess.PIPE,  # 打开标准输入管道
        stdout=subprocess.PIPE,  # 打开标准输出管道
        stderr=subprocess.PIPE,  # 打开标准错误管道（可选）
        # capture_output=True,
        # text=True,
    )
    # 向子进程的标准输入写入数据
    for i in (
        key_enc,
        data,
        use_gzip_str,
    ):
        process.stdin.write((i + " ").encode())  # 需要将字符串编码为字节
    process.stdin.close()  # 关闭标准输入管道，表示输入结束
    # 从子进程的标准输出和标准错误读取数据
    stdout, stderr = process.communicate()  # 等待子进程结束并获取输出
    # 打印子进程的标准输出和标准错误
    stdout = stdout.decode()
    with open("./DecyrptOut.txt", "w") as f:
        f.write(stdout)
        f.write(stderr.decode())
        # 获取子进程的返回码
        return_code = process.returncode
        f.write(str(return_code))
    output = stdout.split("\n")
    # print(output)
    decrypted_key = output[0]
    decrypted_text = output[1]
    return decrypted_key, decrypted_text


def match_str(str, patterns):
    for pattern in patterns:
        if pattern in str:
            return True
    return False


fields_to_keep = [
    "recordMileage",
    "recodePace",
    "recodeCadence",
    "recodeDislikes",
    "duration",
    "pointsList",
    "schoolId",
    "manageList",
]


class Yun:
    saved = False

    def __init__(self):
        pass

    def request(s, flow: mitmproxy.http.HTTPFlow) -> None:
        if default_url not in flow.request.pretty_url:
            flow.live = False

    def response(self, flow: mitmproxy.http.HTTPFlow):

        req_url = flow.request.url
        if default_url in req_url:

            if self.saved == False and match_str(
                req_url,
                ["getStudentInfo", "AppSysMsgApi", "homePageApi", "crsReocordInfo"],
            ):

                # post信息
                new_values = {
                    "token": flow.request.headers.get("token", ""),
                    "device_Id": flow.request.headers.get("deviceId", ""),
                    "version": flow.request.headers.get("version", ""),
                    "device_Name": flow.request.headers.get("deviceName", ""),
                    "uuid": flow.request.headers.get("uuid", ""),
                    "utc": flow.request.headers.get("utc", ""),
                    "sign": flow.request.headers.get("sign", ""),
                }
                my_token = new_values["token"]
                my_device_id = new_values["device_Id"]
                my_version = new_values["version"]
                my_device_name = new_values["device_Name"]
                my_uuid = new_values["uuid"]
                my_utc = new_values[
                    "utc"
                ]  # 或者使用 flow.request.headers.get("utc", "")，但不知为什么会有bug.
                sign = new_values["sign"]  # 同上
                default_key = "ruC9+TPTkI3YzJTfbuFz9A=="
                CipherKeyEncrypted = "BIQWEosEECsZ6WdwU1lTkkLAXeN+t2rgDytWN+wMYKAXfDni7XUsfGcxsfQVCPrDrO73Wl6ZJd+/bJN+454r7W3XtWkF0SrqQ+khtaqOV9feXaNtvIB13ACUaWXtYEczSHenDnFfwqR0Y+YnHc+6ml+WY+oed3MfHg=="

                def proxy_post(
                    data, headers, isBytes=False
                ):  # 对default_post函数的模仿
                    url = f"http://{default_url}/login/getStudentInfo"
                    data_json = {
                        "cipherKey": CipherKeyEncrypted,
                        "content": encrypt_sm4(
                            data, b64decode(default_key), isBytes=isBytes
                        ),
                    }
                    req = requests.post(
                        url=url, data=json.dumps(data_json), headers=headers
                    )
                    try:
                        return decrypt_sm4(req.text, b64decode(default_key)).decode()
                    except:
                        return req.text

                def get_stuinfo():

                    headers = {
                        "token": my_token,
                        "isApp": "app",
                        "deviceId": my_device_id,
                        "deviceName": my_device_name,
                        "version": my_version,
                        "platform": "android",
                        "Content-Type": "application/json; charset=utf-8",
                        "Connection": "Keep-Alive",
                        "Accept-Encoding": "gzip",
                        "User-Agent": "okhttp/3.12.0",
                        "utc": my_utc,
                        "uuid": my_uuid,
                        "sign": sign,
                    }
                    info = json.loads(proxy_post("", headers=headers))
                    if info["code"] == 200:
                        userName = info["data"]["userName"]  # 学号
                        print("学号：" + userName)
                    return userName

                stu_number = get_stuinfo()
                config = configparser.ConfigParser()
                parentDirPath = os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__))
                )
                config_file_path = (
                    parentDirPath
                    + f"/tools/EasyAutoRunSever/configs/config_{stu_number}.ini"
                )
                default_config_file_path = parentDirPath + "/config.ini"
                # print(config_file_path)
                # print(default_config_file_path)
                try:
                    # 检查是否存在对应的配置文件
                    if os.path.exists(config_file_path):
                        config.read(config_file_path, encoding="utf-8")
                        print(f"Using existing configuration file: {config_file_path}")
                    else:
                        config.read(default_config_file_path, encoding="utf-8")
                        print(
                            f"Using default configuration file: {default_config_file_path}"
                        )
                except configparser.Error as e:
                    print(f"Error reading configuration file: {e}")
                    return

                # 获取当前的值
                current_values = {
                    "token": config.get("User", "token", fallback=""),
                    "device_Id": config.get("User", "device_Id", fallback=""),
                    "device_Name": config.get("User", "device_Name", fallback=""),
                    "uuid": config.get("User", "uuid", fallback=""),
                    "utc": config.get("User", "utc", fallback=""),
                    "sign": config.get("User", "sign", fallback=""),
                }
                # 检查是否有变化
                print(current_values)
                if current_values != new_values:
                    # 创建新的文件名
                    new_config_file_path = (
                        parentDirPath + "/tools/EasyAutoRunServer/configs"
                    )
                    new_filename = os.path.join(
                        new_config_file_path, f"config_{stu_number}.ini"
                    )
                    # print(new_filename)
                    # 更新配置
                    for key, value in new_values.items():
                        config.set("User", key, value)
                    # 写入新的文件
                    with open(new_filename, "w") as configfile:
                        config.write(configfile)
                    # 打印更新的信息
                    for key, value in new_values.items():
                        print(f"{key}: {value}")

                self.saved = True
            if "crsReocordInfo" in req_url:
                request_body = json.loads(flow.request.text)
                cipher_key = request_body.get("cipherKey", "")
                response_text = flow.response.text.strip('"')
                print("cipher_key", cipher_key)
                _, tasklist_raw = decode(cipher_key, response_text, True)
                tasklist_json = json.loads(tasklist_raw)
                data = tasklist_json["data"]
                if "pointsList" in data:
                    for point in data["pointsList"]:
                        if "ts" in point:
                            del point["ts"]
                filtered_data = {
                    key: value for key, value in data.items() if key in fields_to_keep
                }
                tasklist_json["data"] = filtered_data
                print(">>>" * 10, "!!!获取到运动任务!!!", "<<<" * 10)
                print("里程: ", str(data["recordMileage"]).ljust(10) + "千米")
                print("速度: ", str(data["recodePace"]).ljust(10) + "千米每时")
                print("步频: ", str(data["recodeCadence"]).ljust(10) + "每分钟步数")
                duration = int(data["duration"] / 60 * 100) / 100
                print("时长: ", str(duration).ljust(10) + "分钟")
                print("===" * 20)
                task_file_name = input("请输入要保存的任务文件名(不保存输入回车跳过): ")
                if not task_file_name:
                    return
                save_path = os.path.join(tasks_path, task_file_name)
                while os.path.exists(save_path):
                    task_file_name = input(
                        "文件名已存在，请重新输入要保存的任务文件名: "
                    )
                    save_path = os.path.join(tasks_path, task_file_name + ".json")
                if not task_file_name:
                    return
                print(f"已经保存任务文件 :", save_path)
                with open(save_path, "w", encoding="utf-8") as file:
                    json.dump(tasklist_json, file, ensure_ascii=False, indent=4)
        else:
            flow.live = False


addons = [Yun()]
