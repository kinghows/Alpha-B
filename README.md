# Alpha-B
Bilibili视频下载

建议下载方式：

首先输入UP主UID号，例如：UID:456065280，把UP主已经发布的视频全部下载。然后在有更新视频后，输入逗号分隔的AV号，例如：70052790,71075368,71272687

或者采用订阅方式：配置Alpha-B.ini

[bili_set]

uid_count = 2

uid1 = 456065280

last_av1 = 71584262

uid2 = 296793775

last_av2 = 

#uid_count 需要下载的UP主数量，超过这个数字的配置忽略

#uid：关注的UP主的UID号

#last_av：不需要输入，程序自动记载最后一次下载的AV号

下载ffmpeg-win32-v3.2.4.exe, 放到ffmpeg的appdata文件夹下:C:\Users\XXX\AppData\Local\imageio\ffmpeg

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
