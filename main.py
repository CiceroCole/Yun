from req import *

"""
加密模式：sm2非对称加密sm4密钥
"""
# 偏移量
# default_iv = '\1\2\3\4\5\6\7\x08' 失效

PublicKey = "BL7JvEAV7Wci0h5YAysN0BPNVdcUhuyJszJLRwnurav0CGftcrVcvrWeCPBIjIIBF371teRbrCS9V1Wyq7i3Arc="
PrivateKey = "P3s0+rMuY4Nt5cUWuOCjMhDzVNdom+W0RvdV6ngM+/E="
PUBLIC_KEY = b64decode(PublicKey)
PRIVATE_KEY = b64decode(PrivateKey)


def get_format_log(message):
    message_stream = StringIO()
    pprint(message, stream=message_stream)
    return message_stream.getvalue()


def exit_msg(msg: str = ""):
    if msg:
        print(">>>" * 10, msg, "<<<" * 10)
    print("\a")
    time.sleep(5)
    sys.exit(0)


def parse_args():
    parser = argparse.ArgumentParser(description="云运动自动跑步脚本")
    parser.add_argument(
        "-f", "--config_path", type=str, default="./config.ini", help="配置文件路径"
    )
    parser.add_argument(
        "-a", "--auto_run", action="store_true", help="自动跑步，默认打表"
    )
    parser.add_argument("-d", "--drift", action="store_true", help="是否添加漂移")
    return parser.parse_args()


def string_to_hex(input_string):
    # 将字符串转换为十六进制表示，然后去除前缀和分隔符
    hex_string = hex(int.from_bytes(input_string.encode(), "big"))[2:].upper()
    return hex_string


def bytes_to_hex(input_string):
    # 将字符串转换为十六进制表示，然后去除前缀和分隔符
    hex_string = hex(int.from_bytes(input_string, "big"))[2:].upper()
    return hex_string


sm2_crypt = sm2.CryptSM2(
    public_key=bytes_to_hex(PUBLIC_KEY[1:]),
    private_key=bytes_to_hex(PRIVATE_KEY),
    mode=1,
    asn1=True,
)


def encrypt_sm4(value, SM_KEY, isBytes=False):
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(SM_KEY, SM4_ENCRYPT)
    if not isBytes:
        encrypt_value = b64encode(crypt_sm4.crypt_ecb(value.encode("utf-8")))
    else:
        encrypt_value = b64encode(crypt_sm4.crypt_ecb(value))
    return encrypt_value.decode()


def decrypt_sm4(value, SM_KEY):
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(SM_KEY, SM4_DECRYPT)
    decrypt_value = crypt_sm4.crypt_ecb(b64decode(value))
    return decrypt_value


# warning：实测gmssl的sm2加密给Java Hutool解密结果不对，所以下面的2函数暂不使用
def encrypt_sm2(info):
    encode_info = sm2_crypt.encrypt(info.encode("utf-8"))
    encode_info = b64encode(encode_info).decode()  # 将二进制bytes通过base64编码
    return encode_info


def decrypt_sm2(info):
    decode_info = b64decode(info)  # 通过base64解码成二进制bytes
    decode_info = sm2_crypt.decrypt(decode_info)
    return decode_info


def getsign(utc, uuid):
    sb = "platform={}&utc={}&uuid={}&appsecret={}".format(
        yun_info["platform"], str(utc), str(uuid), yun_info["md5key"]
    )
    m = hashlib.md5()
    m.update(sb.encode("utf-8"))
    return m.hexdigest()


def default_post(
    router: str,
    data: bytes | str,
    headers: dict = None,
    host: str = None,
    isBytes: bool = False,
    gen_sign: bool = True,
) -> dict | None:
    host = host if host else yun_info["school_host"]
    url = "http://" + host + router
    if gen_sign:
        utc = str(int(time.time()))
        sign = getsign(utc, user_info["uuid"])
    else:
        sign = user_info["sign"]
    if headers is None:
        headers = {
            "token": user_info["token"],
            "isApp": "app",
            "device_id": user_info["device_id"],
            "deviceName": user_info["device_name"],
            "version": yun_info["app_edition"],
            "platform": yun_info["platform"],
            "Content-Type": "application/json; charset=utf-8",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.0",
            "utc": user_info["utc"],
            "uuid": user_info["uuid"],
            "sign": sign,
        }
    data_json = {
        "cipherKey": yun_info["cipherkeyencrypted"],
        "content": encrypt_sm4(data, b64decode(yun_info["cipherkey"]), isBytes=isBytes),
    }
    try:
        req = requests.post(
            url=url, data=json.dumps(data_json), headers=headers
        )  # data进行了加密
        Byte_result = decrypt_sm4(req.text, b64decode(yun_info["cipherkey"]))
        result = Byte_result.decode("utf-8")
        status_code = json.loads(result)["code"]
        logger.debug(f"请求地址: {url}")
        if not data:
            logger.debug("请求数据为空")
        elif not isBytes:
            logger.debug(f"请求数据: ")
            logger.debug(get_format_log(data))
        else:
            logger.debug(f"请求数据: ")
            logger.debug(get_format_log(json.loads(gzip.decompress(data))))
        logger.debug(f"请求响应: ")
        logger.debug(get_format_log(json.loads(result)))
        return result
    except requests.exceptions.ConnectionError as e:
        logger.error(f"网络异常，请检查网络连接")
        logger.error(f"请求异常报错: {e}")
        exit_msg("网络异常，请检查网络连接")
    except Exception as e:
        logger.error(f"请求异常报错: {e}")
        logger.error(f"请求异常响应: {req.text}")
        if status_code == 500:
            logger.error("远程服务器服务异常!(500)")
            exit_msg("远程服务器服务异常!(500)")
        if status_code == 401:
            Logout()
            logger.error("登录失效，请重新登录!(401)")
            exit_msg("登录失效，请重新登录!(401)")
        return False


def Logout():
    config = configparser.ConfigParser()
    config.read(cfg_path, encoding="utf-8")
    for key in user_info_list:
        config.set("User", key, "")
    with open("config.ini", "w+", encoding="utf-8") as f:
        config.write(f)


def save_config():
    config = configparser.ConfigParser()
    config.read(cfg_path, encoding="utf-8")
    for key in user_info_list:
        config.set("User", key, str(user_info[key]))
    with open("config.ini", "w+", encoding="utf-8") as f:
        config.write(f)


def confirm(show_msg: str = "是否继续?"):
    if input(show_msg + "[Y/N]: ") in ["Y", "y", "yes", "Yes", ""]:
        return True
    return False


class Yun_For_New:

    def __init__(
        self,
        info: dict,
        auto_generate_task=False,
    ):
        self.run_info = info["run_info"]
        self.yun_info = info["yun_info"]
        self.user_info = info["user_info"]
        rawdata = default_post(router="/run/getHomeRunInfo", data="")
        data = json.loads(rawdata)["data"]["cralist"][0]
        self.raType = data["raType"]
        self.raId = data["id"]
        self.strides = self.run_info["strides"]
        self.schoolId = data["schoolId"]
        self.raRunArea = data["raRunArea"]
        self.raDislikes = data["raDislikes"]
        self.raMinDislikes = data["raDislikes"]
        self.raSingleMileageMin = (
            data["raSingleMileageMin"] + self.run_info["single_mileage_min_offset"]
        )
        self.raSingleMileageMax = (
            data["raSingleMileageMax"] + self.run_info["single_mileage_max_offset"]
        )
        self.raCadenceMin = data["raCadenceMin"] + self.run_info["cadence_min_offset"]
        self.raCadenceMax = data["raCadenceMax"] + self.run_info["cadence_max_offset"]
        points = data["points"].split("|")
        logger.info("跑步点位:")
        logger.info(get_format_log(points))
        self.now_path = 0

        # self.manageList: List[Dict] = []  # 列表的每一个元素都是字典
        # self.now_time = int(
        #     random.uniform(min_consume, max_consume) * 60 * (self.now_dist / 1000)
        # )
        # self.task_list = []
        # self.task_count = 0
        # self.myLikes = 0
        if auto_generate_task:
            # 如果只要打表，完全可以不执行下面初始化代码
            if not self.user_info["map_key"]:
                logger.error("若使用导航模式请填写高德地图Key")
                self.user_info["map_key"] = input("请输入高德地图Key: ")
                if not self.user_info["map_key"]:
                    os.system(
                        "start https://github.com/CiceroCole/Yun?tab=readme-ov-file#2-%E5%AF%BC%E8%88%AA%E6%A8%A1%E5%BC%8F"
                    )
                    exit_msg("若使用导航模式请填写高德地图Key")
                if confirm("是否保存高德地图Key?"):
                    save_config()
            self.my_select_points = ""
            with open("./map.json") as f:
                my_s = f.read()
                tmp = json.loads(my_s)
                self.my_select_points = tmp["mypoints"]
                self.my_point = tmp["origin_point"]
            for my_select_point in self.my_select_points:  # 手动取点
                if my_select_point in points:
                    logger.info(my_select_point + " 存在")
                else:
                    logger.info(my_select_point + " 不存在")
                    # raise ValueError
            logger.info("开始标记打卡点...")
            if not printLog:
                print("开始标记打卡点...")
            # for exclude_point in exclude_points:
            #     try:
            #         points.remove(exclude_point)
            #         logger.log("成功删除打卡点", exclude_point)
            #     except ValueError:
            #         logger.log("打卡点", exclude_point, "不存在")
            #         # 删除容易跑到学校外面的打卡点
            # # 采取手动选择点的方式，上面的放出圈方法弃用
            self.now_dist = 0
            i = 0
            while (
                self.now_dist / 1000
                > self.run_info["min_distance"]
                + self.run_info["allow_overflow_distance"]
            ) or self.now_dist == 0:
                i += 1
                logger.info("第" + str(i) + "次尝试...")
                self.manageList: List[Dict] = []  # 列表的每一个元素都是字典
                self.now_dist = 0
                self.now_time = 0
                self.task_list = []
                self.task_count = 0
                self.myLikes = 0
                self.generate_task(self.my_select_points)
            self.now_time = int(
                random.uniform(
                    self.run_info["min_consume"], self.run_info["max_consume"]
                )
                * 60
                * (self.now_dist / 1000)
            )
            msg = (
                "打卡点标记完成！本次将打卡"
                + str(self.myLikes)
                + "个点，处理"
                + str(len(self.task_list))
                + "个点，总计"
                + format(self.now_dist / 1000, ".2f")
                + "公里，将耗时"
                + str(self.now_time // 60)
                + "分"
                + str(self.now_time % 60)
                + "秒"
            )
            logger.info(msg)
            if not printLog:
                print(msg)
            # 这三个只是初始化，并非最终值
            self.recordStartTime = ""
            self.crsRunRecordId = 0
            self.userName = ""

    def generate_task(self, points):
        # random_points = random.sample(points, self.raDislikes) # 在打卡点随机选raDislike个点
        logger.info(get_format_log(points))
        for point_index, point in enumerate(points):
            if (
                self.now_dist / 1000 < self.run_info["min_distance"]
                or self.myLikes < self.raMinDislikes
            ):  # 里程不足或者点不够
                self.manageList.append(
                    {"point": point, "marked": "Y", "index": str(point_index)}
                )
                self.add_task(point)
                self.myLikes += 1
                # 必须的任务
            else:
                self.manageList.append({"point": point, "marked": "N", "index": ""})
                # 多余的点
        # 如果跑完了表都不够
        if self.now_dist / 1000 < self.run_info["min_distance"]:
            logger.info("跑完了一圈关键点，长度仍然不够，会自动回跑绕圈圈")
            logger.info(
                "公里数不足"
                + str(self.run_info["min_distance"])
                + "公里，将自动回跑..."
            )
            if printLog:
                print("跑完了一圈关键点，长度仍然不够，会自动回跑绕圈圈")
                print(
                    "公里数不足"
                    + str(self.run_info["min_distance"])
                    + "公里，将自动回跑..."
                )
            index = 0
            while self.now_dist / 1000 < self.run_info["min_distance"]:
                logger.debug(get_format_log(("manageList : \n", self.manageList)))
                self.add_task(self.manageList[index]["point"])
                index = (index + 1) % self.raDislikes

    # 每10个路径点作为一组splitPoint;
    # 若最后一组不满10个且多于1个，则将最后一组中每两个点位分取10点（含终点而不含起点），作为一组splitPoint
    # 若最后一组只有1个（这种情况只会发生在len(splitPoints) > 0），则将已插入的最后一组splitPoint的最后一个点替换为最后一组的点
    def add_task(self, point):  # add_ task 传一个点，开始跑
        if not self.task_list:
            origin = self.my_point
        else:
            origin = self.task_list[-1]["originPoint"]  # 列表的-1项当起始点
        data = {
            "key": self.user_info["map_key"],
            "origin": origin,  # 起始点
            "destination": point,  # 传入的点
        }
        resp = requests.get(
            "https://restapi.amap.com/v4/direction/bicycling", params=data
        )
        # 规划的点
        resp_json = json.loads(resp.text)
        if resp_json.get("errcode") == 10021:
            logger.warning("请求频繁,高德地图API限流,等待1s")
            time.sleep(1)
            self.add_task(point)
            return
        if resp_json.get("errcode") == 10001:
            logger.error("高德地图API密钥错误")
            exit_msg("高德地图API密钥错误")
        if resp_json.get("errcode") == 10044:
            logger.error("今日高德地图API已达使用上限")
            exit_msg("今日高德地图API已达使用上限")
        logger.info("高德地图响应: ")
        logger.info(get_format_log(resp_json))
        paths = resp_json["data"]["paths"]
        split_points = []
        split_point = []
        for path in paths:
            self.now_dist += path["distance"]  # 路径长度
            path["steps"][-1]["polyline"] += ";" + point  # 补上了一个起始点
            for step in path["steps"]:
                polyline = step["polyline"]
                points = polyline.split(";")
                for p in points:
                    i = len(split_point)
                    distForthis = (
                        self.now_dist
                        - path["distance"]
                        * (self.run_info["split_count"] - i)
                        / self.run_info["split_count"]
                    )
                    timeForthis = int(
                        (
                            (
                                self.run_info["min_consume"]
                                + self.run_info["max_consume"]
                            )
                            / 2
                        )
                        * 60
                        * (
                            self.now_dist
                            - path["distance"] * (self.run_info["split_count"] - i)
                        )
                        / 1000
                    )
                    split_point.append(
                        {
                            "point": p,
                            "runStatus": "1",
                            "speed": format(
                                (
                                    self.run_info["min_consume"]
                                    + self.run_info["max_consume"]
                                )
                                / 2,
                                ".2f",
                            ),
                            # 最小和最大速度之间的随机
                            "isFence": "Y",
                            "isMock": False,
                            "runMileage": distForthis,
                            "runTime": timeForthis,
                        }
                    )
                    if len(split_point) == self.run_info["split_count"]:
                        # 到了10个，加入列表组中
                        split_points.append(split_point)
                        # 任务数量加一
                        self.task_count = self.task_count + 1
                        # 清空组
                        split_point = []

        if len(split_point) > 1:  # 不满10个且多于一个
            b = split_point[0]["point"]
            # 上一个点坐标
            for i in range(1, len(split_point)):
                # 建立一个分割列表
                new_split_point = []
                # 保存上一个点的信息
                a = b
                b = split_point[i]["point"]
                # 对a和b求坐标
                a_split = a.split(",")
                b_split = b.split(",")
                a_x = float(a_split[0])
                a_y = float(a_split[1])
                b_x = float(b_split[0])
                b_y = float(b_split[1])
                # 真就均匀等分啊
                d_x = (b_x - a_x) / self.run_info["split_count"]
                d_y = (b_y - a_y) / self.run_info["split_count"]
                # 补上10个点
                for resp_json in range(0, self.run_info["split_count"]):
                    distForthis = (
                        self.now_dist
                        - (path["distance"] / len(split_point))
                        * (self.run_info["split_count"] - resp_json)
                        / self.run_info["split_count"]
                    )
                    timeForthis = int(
                        (
                            (
                                self.run_info["min_consume"]
                                + self.run_info["max_consume"]
                            )
                            / 2
                        )
                        * 60
                        * (
                            self.now_dist
                            - (path["distance"] / len(split_point))
                            * (self.run_info["split_count"] - resp_json)
                            / self.run_info["split_count"]
                        )
                        / 1000
                    )
                    new_split_point.append(
                        {
                            "point": str(a_x + (resp_json + 1) * d_x)
                            + ","
                            + str(a_y + (resp_json + 1) * d_y),
                            "runStatus": "1",
                            "speed": format(
                                (
                                    self.run_info["min_consume"]
                                    + self.run_info["max_consume"]
                                )
                                / 2,
                                ".2f",
                            ),
                            # 最小和最大速度之间的随机
                            "isFence": "Y",
                            "isMock": False,
                            "runMileage": distForthis,
                            "runTime": timeForthis,
                        }
                    )
                split_points.append(new_split_point)
                # 最后一组被分成了 2 ~ 9 组
                self.task_count = self.task_count + 1
        elif len(split_point) == 1:  # 直接把最后一个点扔进去
            split_points[-1][-1] = split_point[0]  # 最后的最后点直接替换
        # 把任务列表加入
        self.task_list.append({"originPoint": point, "points": split_points})

    def start(self):
        # default_post("/run/crsReocordInfo", "")
        data = {"raRunArea": self.raRunArea, "raType": self.raType, "raId": self.raId}
        j: dict = json.loads(default_post("/run/start", json.dumps(data)))
        # 发送开始请求
        if j["code"] == 200:
            jdata: dict = j["data"]
            warnContent = jdata.get("warnContent", "")
            if warnContent:
                info_ = ""
                if "继续跑步不算当天有效次数" in warnContent:
                    info_ = "您的今日跑步任务已完成"
                if "由于当前时间不在学校规定的跑步时间内" in warnContent:
                    info_ = "当前不在您的学校规定的跑步时间段内"
                logger.error(f'云运动任务创建失败！: {jdata["warnContent"]}')
                exit_msg(info_)
            self.recordStartTime = jdata["recordStartTime"]
            self.crsRunRecordId = jdata["id"]
            self.userName = jdata["studentId"]
            logger.info("云运动任务创建成功!")

    def split(self, points):
        data = {
            "StepNumber": int(points[9]["runMileage"] - points[0]["runMileage"])
            / self.strides,
            "a": 0,
            "b": None,
            "c": None,
            "mileage": points[9]["runMileage"] - points[0]["runMileage"],
            "orientationNum": 0,
            "runSteps": random.uniform(self.raCadenceMin, self.raCadenceMax),
            "cardPointList": points,
            "simulateNum": 0,
            "time": points[9]["runTime"] - points[0]["runTime"],
            "crsRunRecordId": self.crsRunRecordId,
            "speeds": format(
                (self.run_info["min_consume"] + self.run_info["max_consume"]) / 2, ".2f"
            ),
            "schoolId": self.schoolId,
            "strides": self.strides,
            "userName": self.userName,
        }
        default_post(
            "/run/splitPointCheating",
            gzip.compress(data=json.dumps(data).encode("utf-8")),
            isBytes=True,
        )  # 这里是特殊的接口，不清楚其他学校，但合工大的完全OK。
        # 发送一组点

    def do(self):
        print(">>>" * 10 + "开始跑步" + "<<<" * 10)
        sleep_time = self.now_time / (self.task_count + 1)
        logger.info("跑步任务点位列表:")
        logger.info(get_format_log(self.task_list))
        logger.info("等待" + format(sleep_time, ".2f") + "秒...")
        if not printLog:
            print("等待" + format(sleep_time, ".2f") + "秒...")
        time.sleep(sleep_time)  # 隔一段时间
        task_index = 0
        for task in tqdm(
            self.task_list,
            leave=True,
            desc="正在跑步...",
            unit="点",
        ):
            logger.info("开始处理第" + str(task_index + 1) + "个点...")  # 打卡点组
            for split_index, split in enumerate(
                task["points"]
            ):  # 一组splitpoints （高德点10个一组）
                self.split(split)  # 发送一组splitpoint （发送的高德点）
                logger.info(
                    "  第"
                    + str(split_index + 1)
                    + "次splitPoint发送成功！等待"
                    + format(sleep_time, ".2f")
                    + "秒..."
                )
                time.sleep(sleep_time)
            task_index += 1
            logger.info("第" + str(task_index + 1) + "个点处理完毕！")

    def do_by_points_map(self, path="./tasks", random_choose=False, isDrift=False):
        files = os.listdir(path)
        files.sort()
        if not random_choose:
            print("检测到可用表格:")
            print("===" * 20)
            i_ = 0
            for f in files:
                with open(os.path.join(path, f), "r", encoding="utf-8") as jf:
                    data = json.loads(jf.read())["data"]
                print("序号: ", i_ + 1)
                print("运动任务信息: ")
                print("名称: ", ".".join(f.split(".")[:-1]))
                print("里程: ", str(data["recordMileage"]).ljust(10) + "千米")
                print("速度: ", str(data["recodePace"]).ljust(10) + "千米每时")
                print("步频: ", str(data["recodeCadence"]).ljust(10) + "每分钟步数")
                duration = int(data["duration"] / 60 * 100) / 100
                print("时长: ", str(duration).ljust(10) + "分钟")
                print("===" * 20)
                i_ += 1
            try:
                choice = int(input("选择(输入序号,-1随机): "))
                if choice == -1:
                    file = os.path.join(path, random.choice(files)).replace("\\", "/")
                else:
                    file = os.path.join(path, files[choice - 1]).replace("\\", "/")
            except ValueError:
                print("输入错误，默认随机选择!")
                file = os.path.join(path, random.choice(files)).replace("\\", "/")
        else:
            file = os.path.join(path, random.choice(files)).replace("\\", "/")
        print("当前任务: ", os.path.splitext(os.path.basename(file))[0])
        with open(file, "r", encoding="utf-8") as f:
            self.task_map = json.loads(f.read())
        duration = str(int(self.task_map["data"]["duration"] / 60 * 100) / 100)
        print("时长: ", duration, "分钟")
        print("为防止被检测,将会对任务添加微小随机改变,实际任务会有些许不同")
        print(">>>" * 10 + "开始跑步" + "<<<" * 10)
        if isDrift:
            self.task_map = add_drift(self.task_map)
        points = []
        count = 0
        for point in tqdm(
            self.task_map["data"]["pointsList"],
            leave=True,
            desc="正在跑步...",
            unit="点",
        ):
            point_changed = {
                "point": point["point"],
                "runStatus": "1",
                "speed": point["speed"],
                # 打表，为了防止格式意外，来一个格式化
                "isFence": "Y",
                "isMock": False,
                "runMileage": point["runMileage"],
                "runTime": point["runTime"],
                "ts": str(int(time.time())),
            }
            points.append(point_changed)
            count += 1
            if count == self.run_info["split_count"]:
                self.split_by_points_map(points)
                sleep_time = (
                    self.task_map["data"]["duration"]
                    / len(self.task_map["data"]["pointsList"])
                    * self.run_info["split_count"]
                )
                logger.info(f" 等待{sleep_time:.2f}秒.")
                time.sleep(sleep_time)
                count = 0
                points = []
        if count != 0:
            self.split_by_points_map(points)
            count = 0
            points = []

    def split_by_points_map(self, points):
        data = {
            "StepNumber": int(
                float(points[-1]["runMileage"]) - float(points[0]["runMileage"])
            )
            / self.strides,
            "a": 0,
            "b": None,
            "c": None,
            "mileage": float(points[-1]["runMileage"]) - float(points[0]["runMileage"]),
            "orientationNum": 0,
            "runSteps": random.uniform(self.raCadenceMin, self.raCadenceMax),
            "cardPointList": points,
            "simulateNum": 0,
            "time": float(points[-1]["runTime"]) - float(points[0]["runTime"]),
            "crsRunRecordId": self.crsRunRecordId,
            "speeds": self.task_map["data"]["recodePace"],
            "schoolId": self.schoolId,
            "strides": self.strides,
            "userName": self.userName,
        }
        default_post(
            "/run/splitPointCheating",
            gzip.compress(data=json.dumps(data).encode("utf-8")),
            isBytes=True,
        )  # 这里是特殊的接口，不清楚其他学校，但合工大的完全OK。
        # 发送一组点

    def finish_by_points_map(self):
        logger.info("发送结束信号...")
        data = {
            "recordMileage": self.task_map["data"]["recordMileage"],
            "recodeCadence": self.task_map["data"]["recodeCadence"],
            "recodePace": self.task_map["data"]["recodePace"],
            "deviceName": self.user_info["device_name"],
            "sysEdition": self.user_info["sys_edition"],
            "appEdition": self.yun_info["app_edition"],
            "raIsStartPoint": "Y",
            "raIsEndPoint": "Y",
            "raRunArea": self.raRunArea,
            "recodeDislikes": str(self.task_map["data"]["recodeDislikes"]),
            "raId": str(self.raId),
            "raType": self.raType,
            "id": str(self.crsRunRecordId),
            "duration": self.task_map["data"]["duration"],
            "recordStartTime": self.recordStartTime,
            "manageList": self.task_map["data"]["manageList"],
            "remake": "1",
        }
        try:
            resp = default_post("/run/finish", json.dumps(data))
            if "合格" in str(resp):
                exit_msg("本次运动成功结束！")
            else:
                exit_msg("本次运动失败！详见日志")
        except Exception as e:
            logger.error(e)
            logger.error("发送失败！")

    def finish(self):
        logger.info("发送结束信号...")
        data = {
            "recordMileage": format(self.now_dist / 1000, ".2f"),
            "recodeCadence": str(random.randint(self.raCadenceMin, self.raCadenceMax)),
            "recodePace": format(self.now_time / 60 / (self.now_dist / 1000), ".2f"),
            "deviceName": self.user_info["device_name"],
            "sysEdition": self.user_info["sys_edition"],
            "appEdition": self.yun_info["app_edition"],
            "raIsStartPoint": "Y",
            "raIsEndPoint": "Y",
            "raRunArea": self.raRunArea,
            "recodeDislikes": str(self.myLikes),
            "raId": str(self.raId),
            "raType": self.raType,
            "id": str(self.crsRunRecordId),
            "duration": str(self.now_time),
            "recordStartTime": self.recordStartTime,
            "manageList": self.manageList,
            "remake": "1",
        }
        try:
            resp = default_post("/run/finish", json.dumps(data))
            if "合格" in str(resp):
                exit_msg("本次运动成功结束！")
        except Exception as e:
            logger.error(e)
            logger.error("发送失败！")


if __name__ == "__main__":
    printLog = False
    if "--printLog" in sys.argv:
        printLog = True
    main_path = os.path.dirname(os.path.abspath(__file__))
    log_file_name = f"{datetime.datetime.now().strftime('%Y-%m-%d')}.log"
    logger = create_logger(__name__, f"{main_path}/logs/{log_file_name}")
    if not printLog:
        logger.removeHandler(logger.handlers[1])
    args = parse_args()
    cfg_path = args.config_path
    # 加载配置文件
    # cfg_path = "./config.ini"
    conf = configparser.ConfigParser()
    conf.read(cfg_path, encoding="utf-8")

    # 学校、keys和版本信息
    yun_info = {}
    yun_info_list = [
        "yun_host",  # 云运动服务器host
        "school_host",  # 学校的host
        "publickey",  # sm2公钥
        "privatekey",  # sm2私钥
        "cipherkeyencrypted",  # 加密密钥的sm2加密版本
        "cipherkey",  # 加密密钥
        "md5key",  # md5加密密钥
        "platform",  # 平台
        "app_edition",  # app版本
        "school_id",  # 学校id
    ]
    for key in yun_info_list:
        yun_info[key] = conf.get("Yun", key)
    user_info = {}
    user_info_list = [
        "token",  # 用户token
        "device_id",  # 设备id
        "map_key",  # map_key是高德地图的开发者密钥
        "device_name",  # 手机名称
        "utc",  # 时间戳
        "uuid",  # uuid
        "sign",  # sign
        "sys_edition",  # 手机操作系统版本
        "username",  # 用户名
        "password",  # 密码
    ]
    for key in user_info_list:
        user_info[key] = conf.get("User", key)

    # 跑步相关的信息
    run_info = {}
    # my_point = conf.get("Run", "point") # 当前位置，取消，改到map.json
    run_info_list = [
        "min_distance",
        "allow_overflow_distance",  # 允许偏移超出的公里数
        "single_mileage_min_offset",  # 单次配速偏移最小
        "single_mileage_max_offset",  # 单次配速偏移最大
        "cadence_min_offset",  # 最小步频偏移
        "cadence_max_offset",  # 最大步频偏移
        "split_count",  # 每10个路径点作为一组splitPoint
        "exclude_points",  # 排除点
        "min_consume",  # 配速最小
        "max_consume",  # 配速最大
        "strides",  # 步幅
    ]
    for key in run_info_list:
        run_info[key] = eval(conf.get("Run", key))
    user_info = Login.main()
    info = {"run_info": run_info, "yun_info": yun_info, "user_info": user_info}
    PUBLIC_KEY = b64decode(yun_info["publickey"])
    PRIVATE_KEY = b64decode(yun_info["privatekey"])
    # config app版本检查 当前可用3.4.5
    if user_info["frist_login"] and confirm("是否保留登录信息?"):
        save_config()
    logger.info("您的信息为: ")
    for key in user_info_list:
        logger.info(key.ljust(15) + str(user_info[key]))
    if user_info["username"]:
        print(f"您的账号为: {user_info['username']}")
    else:
        print(f"你的token为: {user_info['token']}")
    while True:
        if not args.auto_run:
            print("(1) 重演模式 : (建议选择)固定路线无需高德地图key")
            print("(2) 导航模式 : 根据选点与高德地图key自动生成路线")
            print("(3) 定时模式 : 到达输入的时间自动执行运动任务")
            print("(4) 退出登录 : 退出程序并清除登录信息")
            log_table = input("请输入序号选择模式: ")
        else:
            log_table = "1"
        if log_table == "1":
            driftChoice = args.drift if args.auto_run else True
            task_choose = True if args.auto_run else False
            Yun = Yun_For_New(info)
            Yun.start()
            Yun.do_by_points_map(
                path="./tasks", random_choose=task_choose, isDrift=driftChoice
            )
            Yun.finish_by_points_map()
        if log_table == "2":
            Yun = Yun_For_New(
                info=info,
                auto_generate_task=True,
            )
            Yun.start()
            Yun.do()
            Yun.finish()
        # 取消快速模式
        # if log_table == "3":
        #     Yun = Yun_For_New(auto_generate_task=True)
        #     Yun.start()
        #     Yun.finish()
        if log_table == "3":
            timer()
            Yun = Yun_For_New(info)
            Yun.start()
            Yun.do_by_points_map(path="./tasks", random_choose=True, isDrift=True)
            Yun.finish_by_points_map()
        if log_table == "4":
            Logout()
            exit_msg("退出程序")
