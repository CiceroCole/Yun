## 云运动代刷脚本(安徽三联学院)
> 免责声明：一切内容只能用于交流学习，24h内自觉卸载，否则后果自负。

**此库基于原作者[Zirconium233](https://github.com/Zirconium233 "Zirconium233")的[yunForNewVersion](https://github.com/Zirconium233/yunForNewVersion "yunForNewVersion")专门针对我所在的学校([安徽三联学院](https://www.slu.edu.cn/ "安徽三联学院"))修改而来，若是同校校友可直接使用，否则请看根据所在学校[自行修改](#自行修改简要教程)。**

### 简要教程:
> 以下只做简要使用介绍，若想查看细节请查看原作者的[Zirconium233](https://github.com/Zirconium233 "Zirconium233")的[yunForNewVersion](https://github.com/Zirconium233/yunForNewVersion "yunForNewVersion")项目

### 1.安装Python及项目依赖
> 可在[release](https://github.com/CiceroCole/Yun/releases)下载本项目的安装程序，打包集成了Python 3.10.0b1环境
### 在 Windows 上安装 Python
1. **下载安装程序**
   - 访问 [Python 官方网站](https://www.python.org/downloads/windows/)。
   - 下载最新版本的 Python 安装程序（通常是 `.exe` 文件）。

2. **运行安装程序**
   - 找到下载的 `.exe` 文件并双击运行。
   - 勾选 `Add Python 3.x to PATH` 选项，然后点击 `Install Now`。

3. **验证安装**
   - 打开命令提示符（Command Prompt），输入以下命令：
     ```bash
     python --version
     ```
   - 如果安装成功，将会显示已安装的 Python 版本号。
4. **创建虚拟环境并安装依赖**
   虚拟环境可以帮助隔离不同项目的依赖。
   - **首先打开命令行并进入项目所在目录**
   - **创建一个新的虚拟环境**：
      ```bash
      python -m venv ./venv
      ```
   - **激活虚拟环境**：
       ```bash
      act
       ```
   - **安装依赖**
   - 在激活的虚拟环境中，使用以下命令安装 `requirements.txt` 中列出的所有依赖：
     ```bash
     pip install -r requirements.txt 
     ```
     可以通过清华源镜像加速下载：
     ```bash
     pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
     ```

### 2.运行脚本并登录
#### 下载项目
若本地有`git`工具则可以通过`git clone https://github.com/CiceroCole/Yun.git`命令本项目下载到本地
若没有可直接在本项目上点击`code`后单击`Download ZIP`直接下载压缩包至本地后解压 
#### 1.运行脚本
- 确保已激活虚拟环境和安装项目依赖，并已进入项目目录
- 在命令行中运行以下命令 
   ```bash
   python main.py
   ```
- 之后若是没有意外退出并显示以下信息:
   ```   
   请输入用户账号: 
   ```
   则成功运行该脚本

### 2.登录
登录方式有两种：[账号密码登录](#账号密码登录), [token登录](#token登录)
#### 账号密码登录
**在运行后根据输入提示输入对应信息即可登录**
```
请输入用户账号: 你的云运动账号(一般来说时学院学号)
请输入用户密码: 你的云运动密码
```
之后登录成功会显示登录成功的信息，会出现以下信息
```
是否保持登录状态?[Y/N]: 
```
输入`Y`并回车即可保留登录状态，若输入`N`则只有本次程序临时有效，若想永久有效需重新登录保留登录状态。
#### token登录
> 此部分的教程改编于[Zirconium233](https://github.com/Zirconium233 "Zirconium233")的[yunForNewVersion](https://github.com/Zirconium233/yunForNewVersion "yunForNewVersion")

**1.手机安装抓包软件**（例如以下软件）:
![抓包软件](https://pic.superbed.cc/item/676659a5fa9f77b4dc0d73c2.jpg)

**2.启动抓包软件**（以PCAPdroid为例）
![启动抓包软件](https://pic.superbed.cc/item/676659e6fa9f77b4dc0d79f4.jpg)

**3.打开云运动APP，随意进行操作(不用跑步)
查看类似以下的请求（端口为8080，对于三联学生链接是`sports.aiyyd.com:8080`）:**
![请求](https://pic.superbed.cc/item/676659bdfa9f77b4dc0d75c8.png)

**4.查看请求的请求头:**
![请求头](https://pic.superbed.cc/item/67665986fa9f77b4dc0d7123.jpg)
把以上内容对应填入项目目录下的`config.ini`文件中保存，并重新启动脚本即可

### 3.模式介绍
在项目路径运行脚本并登录之后，会输出类似以下信息
```
您的账号为:  ******************
是否使用此账号进行运动?[Y/N]: 
```
或者
```
你的token为: ******************
是否使用此账号进行运动?[Y/N]: 
```
以上为您的个人信息请确认后输入`Y`并回车,会输出以下信息:
```
(1) 重演模式 : (建议选择)固定路线无需高德地图key
(2) 导航模式 : 根据选点与高德地图key自动生成路线
(3) 定时模式 : 到达输入的时间自动执行运动任务
(4) 退出程序
请输入序号选择模式:
```
#### (1) 重演模式 (推荐)
重演模式会根据已有的跑步记录生成任务，任务文件在项目目录的`tasks`下
输入`1`选择重演模式后会提示：

检测到可用表格:
```
============================================================
序号:  0
运动任务信息:
名称:  2.5km
里程:  2.5       千米
速度:  4.01      千米每时
步频:  247       每分钟步数
时长:  10.05     分钟
============================================================
序号:  1
运动任务信息:
名称:  2.6km
里程:  2.61      千米
速度:  5.97      千米每时
步频:  160       每分钟步数
时长:  15.56     分钟
============================================================
...(省略)
```
```
选择(输入序号,-1随机):
```
以上是在三联学院的已经生成的跑步路线，文件名对应运动路程，
输入序号选择任务文件即开始运动
> 项目中已有的跑步记录是在三联学院操场的运动记录，若是其他学校请[自行生成跑步记录](#自行生成跑步记录)

#### (2) 导航模式<a id=DaoHangMode></a>
> 此处教程改编于[kontori](https://github.com/kontori)的[yun](https://github.com/kontori/yun?tab=readme-ov-file)
1. 获取高德地图开发者密钥
   脚本使用高德地图API规划跑步路径，故需要获取开发者密钥。
   有能力的可以自己尝试更精确的路径规划哦
   
   登录高德开放平台 https://console.amap.com/dev/key/app 
   
   ![image](https://github.com/kontori/images/raw/main/yun-1.png)

   点击右上角的创建新应用，应用名称随便，
   ### **应用类型选择出行**
   创建完毕后，点击应用上方的添加按钮，
   <img src="https://github.com/kontori/images/raw/main/yun-2.png" alt="" width="450">
   Key名称随便，
   ### **服务平台选择Web服务**
   IP白名单留空即可。你将会得到一个Key，
   这就是我们的开发者密钥。**（不是安全密钥！）**

2. 配置
   你需提前在config.ini文件中完成一些简单的配置。**不要随意删除配置字段。**
   ```ini
   [User]
   ; 高德地图开发者密钥
   map_key = 
   ```
   - 在此处填入得到的Key,并通过[坐标拾取器](https://lbs.amap.com/tools/picker)获得想要打卡点经纬度按照`map.json`的格式填入`map.json`中。
   - 之后会根据项目目录下的`map.json`文件中的坐标生成跑步任务，路线可能会比较不规则

#### (3) 定时模式
当你选择`(3) 定时模式`会出现以下信息:
```
请输入明日开始跑步的时间(回车使用随机时间6:00~7:30)
小时: (此处输入您想要运行的时间的小时(例如7:10的7)) 
分钟: (此处输入您想要运行的时间的分钟(例如7:10的10))
```
之后若输出信息为以下信息，则说明已经成功设置好定时任务:
```
目标时间: 2024年12月28日 07时10分44秒
倒计时: 12时 0分20秒
```
**注意: 程序运行时请勿关机或退出**

------------
### 自行修改简要教程
   若是其他学院的学生也使用云运动进行运动，
   可以通过修改更改目标服务器地址，地图选点，自行生成跑步记录的方式使用本脚本
#### 更改目标服务器地址
1. 获取`school_host`,`school_id`
   在[token登录](#token登录)中，使用抓包软件可获取目标服务器地址(普遍使用8080端口号)
2. 修改`school_host`字段
   进入项目目录下`config.ini`文件中修改`school_host`字段
3. 修改`school_id`字段
   进入项目目录下`config.ini`文件中修改`school_id`字段

#### 自行地图选点
在[导航模式](#DaoHangMode)的说明中，我们获得了一个高德地图key并添加至`config.ini`中
之后应在项目目录下`map.json`文件中添加坐标，通过[坐标拾取器](https://lbs.amap.com/tools/picker)获得想要打卡点经纬度坐标,之后按照`map.json`的格式填入`map.json`中。
```json
{
   // 起点
   "origin_point":"117.194604,31.75284",
   // 途径点
   "mypoints": [
        "117.195176,31.752605",
        "117.195284,31.752222",
        "117.195386,31.751736",
        "117.194702,31.751597",
        "117.194555,31.752172",
        "117.194492,31.752537"
    ]
}
```
添加完成后即可选择导航模式进行运动任务
> 高德地图的key每日限制5000次请求上限

#### 自行生成跑步记录
> 此部分教程源自于[Zirconium233](https://github.com/Zirconium233 "Zirconium233")/[yunForNewVersion](https://github.com/Zirconium233/yunForNewVersion)的[proxy.md](https://github.com/Zirconium233/yunForNewVersion/blob/master/proxy.md)

**在 Windows 上安装 JDK 17**
1. **下载安装程序**
   - 访问 [mitmproxy](https://mitmproxy.org/) 
   - 下载 mitmproxy 安装包并安装
   - 访问 [Opne JDK 23 下载页面](https://jdk.java.net/23/)。
   - 下载适用于 Windows 的 JDK 23 压缩包文件
   - (Windows / x64	[zip](https://download.java.net/java/GA/jdk23.0.1/c28985cbf10d4e648e4004050f8781aa/11/GPL/openjdk-23.0.1_windows-x64_bin.zip) (sha256)	209134637)
   - 解压压缩包至您想安装 JDK 的文件夹。（例如 `C:\Program Files\Java\`）

2. **配置环境变量**
   - 打开“控制面板” -> “系统和安全” -> “系统” -> “高级系统设置”。
   - 点击“环境变量”按钮。
   - 在“系统变量”部分，找到 `Path` 变量并点击“编辑”。
   - 添加 JDK 的 `bin` 目录路径（例如 `C:\Program Files\Java\jdk-23.0.1\bin`）。
   - 确认所有对话框以保存更改。

3. **验证安装**
   - 打开命令提示符（Command Prompt），输入以下命令：
     ```
     java -version
     javac -version
     ```
   - 如果安装成功，将会显示已安装的 Java 和 Java 编译器版本号。
   - 输入以下命令
      ```
      mitmproxy
      ```
   - 如果安装成功，将会显示类似以下的信息并弹出网页:
      ```
      [17:48:16.304] HTTP(S) proxy listening at *:8080.
      [17:48:16.307] Web server listening at http://127.0.0.   1:8081/
      ```
      > 按下`Ctrl+C`可以退出代理服务

**启动代理获取手机云运动app的运动数据**

1. 使得手机和电脑处于同一局域网下。
   > 可以手机开热点，然后电脑连接手机热点，关闭windows系统防火墙记得
2. 进入项目目录下tools目录，运行以下命令启动代理服务
   ```bash
   mitmweb -p 8080 -s proxy.py
   ```
3. 手机端配置代理连接
   - 下载代理服务app (这里以[Super roxy](https://apkcombo.com/super-proxy/com.scheler.superproxy/)为例)
   - 配置代理服务app
      1. 获取PC端ip地址,在命令行输入``ipconfig``命令
      2. 找到`IPv4 Address`字段获取到ip地址
      ```bash
      IPv4 Address. . . . . . . . . . . : 192.168.1.106
      ```
      3. 打开代理服务app，配置获取到的ip地址和端口号(8080)
         ![添加配置1](https://pic.superbed.cc/item/67669676fa9f77b4dc104464.jpg)
         ![添加配置2](https://pic.superbed.cc/item/676696eafa9f77b4dc104898.jpg)
   - 启动代理服务app
      ![启动配置](https://pic.superbed.cc/item/676697ddfa9f77b4dc1052d1.jpg)
4. **添加打表任务**
   - **手机端打开云运动app**
   - **选择想要添加至打表任务运动记录**

之后脚本会自动捕捉运动记录，若输出类似以下信息，则说明已经成功获取运动任务
```
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> !!!获取到运动任务!!! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
里程:  2.42      千米
速度:  7.88      千米每时
步频:  133       每分钟步数
时长:  19.08     分钟
============================================================
请输入要保存的任务文件名(不保存输入回车跳过):
```
之后输入您想命名的打表任务名,就会将任务保存至`tasks`目录下