# Alpha-B
Bilibili视频下载

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