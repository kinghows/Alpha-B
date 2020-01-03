# Alpha-B
Bilibili视频下载

下载方式：

1、订阅方式：配置Alpha-B.ini，直接按开始下载，自动按照配置下载最新的视频。

2、下载UP主全部视频：输入UP主UID号，例如：UID:456065280，把UP主已经发布的视频全部下载。

3、下载单个视频：输入逗号分隔的AV号，例如：70052790,71075368,71272687

[bili_set]

uid_count = 2

uid1 = 456065280

last_av1 = 71584262

uid2 = 296793775

last_av2 = 

#uid_count 需要下载的UP主数量，超过这个数字的配置忽略

#uid：关注的UP主的UID号

#last_av：不需要输入，程序自动记载最后一次下载的AV号

下载ffmpeg-win32-v3.2.4.exe, 放到文件夹下:C:\Users\XXX\AppData\Local\imageio\ffmpeg

确保放进去的文件名一定改成ffmpeg-win32-v3.2.4.exe, 因为"D:\Python37\lib\site-packages\imageio\plugins\ffmpeg.py"文件里就是硬编码的这个文件名.

python 版本：Python 3.7.4rc2

开发安装：

pip install pyinstaller

如果报错，请安装numpy1.16.2

ModuleNotFoundError: No module named 'numpy.random.common'

pip uninstall numpy

pip install numpy==1.16.2

打包成一个exe文件：

pyinstaller –F –p moviepy Alpha-B.py


## 好玩的Alpha系列，喜欢的打颗星：

- [Alpha-12306：买个票](https://github.com/kinghows/Alpha-12306)

- [Alpha-C：智能闲聊](https://github.com/kinghows/Alpha-C)

- [Alpha-P：检测手机照片的拍摄时间和地点以及颜值](https://github.com/kinghows/Alpha-P)

- [Alpha-D：人工智能刷抖音](https://github.com/kinghows/Alpha-D)

- [Alpha-J：微信跳一跳python玩法](https://github.com/kinghows/Alpha-J)

- [Alpha-A：量化投资--一个全栈实验项目](https://github.com/kinghows/Alpha-A)
