import json
import os
import random
from log import create_logger

logger = create_logger(__name__, "log.txt")


def change_pace(path, target_speed: float):
    logger.info("当前处理：" + path)
    logger.info("目标配速：" + str(target_speed))
    tasklist_ = dict()
    with open(file=path, mode="r+", encoding="utf-8") as f:
        data = f.read()
        tasklist_ = json.loads(data)
    tasklist = tasklist_["data"]
    logger.info("当前配速：" + str(tasklist["recodePace"]))
    factor = target_speed / tasklist["recodePace"]
    logger.info("时间放缩因子：" + str(factor))
    if factor > 1:
        logger.info("已经超越目标时间，停止放缩。")
        return
    tasklist["recodePace"] = round(target_speed, 2)
    tasklist["duration"] = int(factor * tasklist["duration"])  # 放缩时间
    tasklist["recodeCadence"] = int(tasklist["recodeCadence"] / factor)  # 增大步频
    pointList = tasklist["pointsList"]
    for point in pointList:
        point["speed"] = round(factor * point["speed"], 2)
        point["runTime"] = str(int(float(point["runTime"]) * factor))
        point["runStep"] = str(int(float(point["runStep"]) / factor))
    logger.info(
        f"完成，耗时变为：{tasklist['duration']}秒, 步频变成{tasklist['recodeCadence']}每分钟"
    )
    with open(file=path, mode="w+", encoding="utf-8") as f:
        data = json.dumps(tasklist_)
        logger.info(f"写入文件: {path} ")
        f.write(data)


def change_all(path_dir, target_speed: str):
    files = os.listdir(path_dir)
    for file in files:
        target_speed = round(random.uniform(4.5, 5.5), 2)
        change_pace(os.path.join(path_dir, file), target_speed)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    path = os.path.abspath("../tasks")
    tasks_list = os.listdir(path)
    tasks_list.sort()
    print("检测到可用Tasklist: ")
    for i, p in enumerate(tasks_list):
        print(f"({i}) : {p}")
    choice = input("你需要修改哪一个tasklist?[All or index]: ")
    speed = input("你要的配速是多少分(4.5~5.5之间,-1随机): ")
    try:
        speed_f = None
        if speed == "-1":
            speed_f = round(random.uniform(4.5, 5.5), 2)
        else:
            speed_f = round(float(speed), 2)
        if choice == "All":
            change_all(path, speed)
        else:
            chi = int(choice)
            if chi > len(tasks_list):
                logger.error("输入错误，退出")
                exit()
            change_pace(f"{path}/{tasks_list[choice]}", speed_f)

    except Exception as e:
        logger.error("输入错误，退出!")
        print(e)
        print('错误退出,如果显示"写入文件",可能已经更改了文件,请自行确认是否可用。')
        input()
