## 云运动代刷脚本(安徽三联学院)
> 免责声明：一切内容只能用于交流学习，24h内自觉卸载，否则后果自负。

**此库基于原作者[Zirconium233](https://github.com/Zirconium233 "Zirconium233")的[yunForNewVersion](https://github.com/Zirconium233/yunForNewVersion "yunForNewVersion")专门针对我所在的学校([安徽三联学院](https://www.slu.edu.cn/ "安徽三联学院"))修改而来，若是同校校友可直接使用，否则请看根据所在学校[自行修改](# 自行修改简要教程)。**

### 简要教程:
> 以下只做简要使用介绍，若想查看细节请查看原作者的[Zirconium233](https://github.com/Zirconium233 "Zirconium233")的[yunForNewVersion](https://github.com/Zirconium233/yunForNewVersion "yunForNewVersion")项目

#### 1.安装Python及项目依赖
##### 在 Windows 上安装 Python
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
   - 首先打开命令行并进入项目所在目录
   - **创建一个新的虚拟环境**：
   ```bash
   python -m venv ./venv
   ```
   - **激活虚拟环境**：
       ```bash
       ./venv/Scripts/activate
       ```
 - **安装依赖**
   - 在激活的虚拟环境中，使用以下命令安装 `requirements.txt` 中列出的所有依赖：
     ```bash
     pip install -r requirements.txt
     ```

#### 2.运行脚本并登录
##### 1.运行脚本
- 在命令行中运行以下命令 (已经创建好虚拟环境并激活过且已进入项目目录):
```bash
python main.py
```
之后若是没有意外退出并显示以下信息:
```
config中token为空，是否尝试使用账号密码登录?[Y/N]: 
```
则成功运行该脚本

##### 2.登录
登录方式有两种：[账号密码登录](# 账号密码登录), [token登录](# token登录)
###### 账号密码登录
在运行后显示以下信息:
```
config中token为空，是否尝试使用账号密码登录?[Y/N]: 
```
输入`Y`并回车
之后根据输入提示输入对应信息即可登录
###### token登录
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

#### 3.模式介绍
在项目路径运行脚本并登录之后，会输出类似以下信息
```
您的信息为:
Token:         ***********************
deviceId:      **********************
deviceName:    *******************
utc:           123456789
uuid:          987654321
sign:          *************
请确定数据无误[Y/N]: 
```
以上为您的个人信息请确认后输入`Y`并回车,会输出以下信息:
```
(1) 打表模式 : 固定路线无需高德地图key
(2) 导航模式 : 根据选点与高德地图key自动生成路线
(3) 快速模式 : 直接提交路线(不建议)
(4) 退出程序
请输入序号选择模式:
```
##### (1) 打表模式 (推荐)
打表模式会根据已有的跑步记录生成任务，任务文件在项目目录的`tasks`下
输入`1`选择打表模式后会提示：
```
是否为数据添加漂移[y/n]:
```
若准许为数据添加漂移可以为跑步路线添加一些移动变化
输入`Y`或`N`之后会提示:
```
检测到可用表格:
(0) : 2.4km.json
(1) : 2.5km.json
(2) : 2.6km.json
(3) : 2.7km.json
(4) : 2.8km.json
(5) : 2.9km.json
(6) : 3km.json
(7) : 4km.json
(8) : 5km.json
选择(输入序号,-1随机):
```
以上是在三联学院的已经生成的跑步路线，文件名对应运动路程，
输入序号选择任务文件即开始运动
> 项目中已有的跑步记录是在三联学院操场的运动记录，若是其他学校请[自行生成跑步记录](# 自行生成跑步记录)

##### (2) 导航模式
> 此处教程改编于[kontori](https://github.com/kontori)的[yun](https://github.com/kontori/yun?tab=readme-ov-file)
1. 获取高德地图开发者密钥
脚本使用高德地图API规划跑步路径，故需要获取开发者密钥。有能力的可以自己尝试更精确的路径规划哦
登录 https://console.amap.com/dev/key/app 
![image](https://github.com/kontori/images/raw/main/yun-1.png)
点击右上角的创建新应用，应用名称随便，应用类型选择出行。
创建完毕后，点击应用上方的添加按钮，
<img src="https://github.com/kontori/images/raw/main/yun-2.png" alt="" width="450">
Key名称随便，服务平台选择**Web服务**，IP白名单留空即可。你将会得到一个Key，这就是我们的开发者密钥。**（不是安全密钥！）**
2.配置
你需提前在config.ini文件中完成一些简单的配置。**不要随意删除配置字段。**
```ini
[User]
; 高德地图开发者密钥
map_key = 
```
- 在此处填入得到的Key,并通过[坐标拾取器](https://lbs.amap.com/tools/picker)获得想要打卡点经纬度按照`map.json`的格式填入`map.json`中。
- 之后会根据项目目录下的`map.json`文件中的坐标生成跑步任务，路线可能会比较不规则

##### (3) 快速模式 (不推荐)
无需等待直接通过，没有跑步轨迹，程序可以通过，但是具有被人工检测的风险
------------


### 自行修改简要教程
#### 更改目标服务器地址
#### 自行地图选点
#### 自行生成跑步记录
