import time
from random import randint
from datetime import datetime, timedelta


def format_timedelta(td):
    # 获取总秒数，并转换为天、小时、分钟和秒
    total_seconds = int(td.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return days, hours, minutes, seconds


def timer():
    # 获取当前时间
    now = datetime.now()
    if now.hour < 6:
        day_info = "今日"
    else:
        day_info = "明日"
    print(f"请输入{day_info}开始跑步的时间(回车使用随机时间6:00~7:30)")
    minute = hour = 0
    try:
        hour = int(input("小时: "))
        minute = int(input("分钟: "))
    except ValueError:
        hour = hour if hour else randint(6, 7)
        minute = randint(0, 30) if hour == 7 else randint(0, 59)

    target_time = now.replace(
        hour=hour, minute=minute, second=randint(0, 59), microsecond=randint(0, 59)
    )

    if now.hour > 8:
        target_time += timedelta(days=1)
    print("目标时间:", target_time.strftime("%Y年%m月%d日 %H时%M分%S秒"))
    while datetime.now() < target_time:
        countdown = format_timedelta(target_time - datetime.now())
        print("\r倒计时: {0:2d}时{1:2d}分{2:2d}秒".format(*(countdown[1:])), end="")
        time.sleep(1)
    return True
