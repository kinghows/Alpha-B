# !/usr/bin/python
# -*- coding:utf-8 -*-

import requests, time, hashlib,urllib.request,urllib.error,re, json
import imageio
imageio.plugins.ffmpeg.download()
from moviepy.editor import *
import os, sys, threading
from tkinter import *
from tkinter import ttk
from tkinter import StringVar
import configparser

root=Tk()

# 将输出重定向到表格
def print(theText):
    msgbox.insert(END,theText+'\n')


# 访问API地址
def get_play_list(start_url, cid, quality):
    entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
    appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
    params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
    chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
    url_api = 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
    headers = {
        'Referer': start_url,  # 注意加上referer
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    # print(url_api)
    html = requests.get(url_api, headers=headers).json()
    # print(json.dumps(html))
    video_list = []
    for i in html['durl']:
        video_list.append(i['url'])
    # print(video_list)
    return video_list


# 下载视频
'''
 urllib.urlretrieve 的回调函数：
def callbackfunc(blocknum, blocksize, totalsize):
    @blocknum:  已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
'''


def Schedule_cmd(blocknum, blocksize, totalsize):
    global starttime
    recv_size = blocknum * blocksize
    if blocknum == 0:
        starttime = time.time()
        speed = 0
    else:
        cost_time = time.time() - starttime
        speed = recv_size / cost_time
    speed_str = "%s" % format_size(speed)

    # 设置下载进度条
    pervent = recv_size / totalsize
    percent_str = "%.2f%%" % (pervent * 100)
    download.coords(fill_line1,(0,0,pervent*465,23))
    root.update()
    #pct.set(percent_str)
    pct.set(speed_str +'    '+percent_str)

# 字节bytes转化K\M\G
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("输入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.1fG" % (G)
        else:
            return "%.1fM" % (M)
    else:
        return "%.1fK" % (kb)


#  下载视频
def down_video(owner_name,video_list, title, start_url, page):
    num = 1
    
    currentVideoPath = os.path.join(os.getcwd(), 'bilibili_video',owner_name)  # 当前目录作为下载目录
    print('下载中...')

    for i in video_list:
        opener = urllib.request.build_opener()
        # 请求头
        opener.addheaders = [
            # ('Host', 'upos-hz-mirrorks3.acgvideo.com'),  #注意修改host,不用也行
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),  # Range 的值要为 bytes=0- 才能下载完整视频
            ('Referer', start_url),  # 注意修改referer,必须要加的!
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
        ]
        urllib.request.install_opener(opener)
        # 创建文件夹存放下载的视频
        if not os.path.exists(currentVideoPath):
            os.makedirs(currentVideoPath)
        # 开始下载
        if len(video_list) > 1:
            filename = os.path.join(currentVideoPath, r'{}-{}.flv'.format(title, num))
        else:
            filename = os.path.join(currentVideoPath, r'{}.flv'.format(title))

        try:
            urllib.request.urlretrieve(url=i, filename=filename,reporthook=Schedule_cmd)
        except urllib.error.HTTPError as e:
            print('HTTPError reason: '+ e.reason)
        except urllib.error.URLError as e:
            print('URLError reason: '+ e.reason)

        num += 1

#  下载视频
def down_videos(start,quality, start_url, headers,uid_no):
    html = requests.get(start_url, headers=headers).json()
    if html['code']==0:
        data = html['data']
        if uid_no != '0' and uid_no != 'dlist' :
            owner_name = data['owner']['name']
        else:
            owner_name = 'dlist'
        pre_title = data['title']
        cid_list = []
        if '?p=' in start_url:
            # 单独下载分P视频中的一集
            p = re.search(r'\?p=(\d+)',start).group(1)
            cid_list.append(data['pages'][int(p) - 1])
        else:
            # 如果p不存在就是全集下载
            cid_list = data['pages']

        cidcount = len(cid_list)

        for item in cid_list:
            cid = str(item['cid'])
            part = item['part']
            if cidcount > 1 :
                title = pre_title + part
            else:
                title = pre_title
            title = re.sub(r'[\/\\:*?"<>|]', '', title)  # 替换为空的
            print('[标题]:' + title)
            page = str(item['page'])
            start_url = start_url + "/?p=" + page
            video_list = get_play_list(start_url, cid, quality)
            start_time = time.time()
            down_video(owner_name,video_list, title, start_url, page)
            end_time = time.time()  # 结束时间
            print('下载完成,耗时%.2f分钟' % (int(end_time - start_time) / 60))
            print('*' * 30)

        if uid_no != '0' and uid_no != 'dlist' :
            config = configparser.ConfigParser()
            config.read("Alpha-B.ini")
            config.set("bili_set", "last_av"+uid_no,start)
            config.write(open('Alpha-B.ini', 'w')) 

def down_uid(uid,last_aid,quality,headers,uid_no):
    avlist = []
    pages = ''
    start_url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid="+ uid +"&pagesize=30&tid=0&page=1&keyword=&order=pubdate"
    html = requests.get(start_url, headers=headers).json()
    pages = html['data']['pages']
    flag = True
    for page in range(pages): 
        start_url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid="+ uid +"&pagesize=30&tid=0&page="+ str(page+1) +"&keyword=&order=pubdate"
        html = requests.get(start_url, headers=headers).json()
        jsonvlist = html['data']['vlist']
        for i in range(len(jsonvlist)):
            aid = jsonvlist[i]['aid']
            if str(aid) == last_aid:
                flag = False
                break
            else:
                avlist.append(aid)
        if not flag:
            break
    
    for aid in sorted(avlist):
    # 获取cid的api, 输入aid即可
        start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + str(aid)
        down_videos(str(aid),quality, start_url, headers,uid_no) 

def get_uid_list(uid,headers):
    avlist = []
    pages = ''
    start_url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid="+ uid +"&pagesize=30&tid=0&page=1&keyword=&order=pubdate"
    html = requests.get(start_url, headers=headers).json()
    pages = html['data']['pages']
    for page in range(pages): 
        start_url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid="+ uid +"&pagesize=30&tid=0&page="+ str(page+1) +"&keyword=&order=pubdate"
        html = requests.get(start_url, headers=headers).json()
        jsonvlist = html['data']['vlist']
        for i in range(len(jsonvlist)):
            aid = jsonvlist[i]['aid']
            title = jsonvlist[i]['title']
            avlist.append({'title':title,'aid':aid})
    with open(uid+'.json', 'w',encoding='utf-8') as f:
        json.dump(avlist, f,ensure_ascii=False, indent=2)

def do_prepare(inputStart,downloadMode):
    # 清空进度条
    download.coords(fill_line1,(0,0,0,23))
    pct.set('0.00%')
    root.update()
    # 清空文本栏
    msgbox.delete('1.0','end')
    start_time = time.time()
    # 用户输入av号或者视频链接地址
    print('*' * 30 + 'B站视频下载小助手' + '*' * 30)

    # 视频质量
    # <accept_format><![CDATA[flv,flv720,flv480,flv360]]></accept_format>
    # <accept_description><![CDATA[高清 1080P,高清 720P,清晰 480P,流畅 360P]]></accept_description>
    # <accept_quality><![CDATA[80,64,32,16]]></accept_quality>
    quality = '80'
    # 获取视频的cid,title
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    
    mode = downloadMode
    start = inputStart
    if start == '':
        if mode == '订阅更新':
            config = configparser.ConfigParser()
            config.read("Alpha-B.ini")
            uid_count = int(config.get("bili_set","uid_count"))
            n = 1
            while n <= uid_count:
                uid_no = str(n)
                uid = config.get ( "bili_set", "uid"+uid_no)
                last_aid = config.get ( "bili_set", "last_av"+uid_no)
                down_uid(uid,last_aid,quality,headers,uid_no)
                print('UID' + uid_no.rjust(2) + ' : 最新视频已下载。')
                n += 1
            print('*** 所有最新视频已下载。')
        else:
            with open("dlist.json", "r", encoding="utf-8") as f:
                j = json.load(f)
            uid_no = 'dlist'
            avlist = []
            for i in range(len(j)):
                aid = str(j[i]['aid'])
                avlist.append(aid)
            for aid in avlist:
                start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + aid
                down_videos(aid,quality, start_url, headers,uid_no)
                j.pop(0)
                with open('dlist.json', 'w',encoding='utf-8') as f:
                    json.dump(j, f,ensure_ascii=False, indent=2)
            print('*** 所有下载列表视频已下载。***')
    elif start[0:4] == 'UID:': 
        uidlist=[]
        uidlist = start[4:].split(",")
        for uid in uidlist:
            get_uid_list(uid,headers)
            print('UID:' + uid +'下载列表已完成。')        
    elif start[0:4] == 'AID:':
        aidlist=[]
        uid_no = '0'
        aidlist = start[4:].split(",")
        for aid in aidlist:
        # 获取cid的api, 输入aid即可
            start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + aid
            down_videos(aid,quality, start_url, headers,uid_no)

    # 如果是windows系统，下载完成后打开下载目录
    #currentVideoPath = os.path.join(os.getcwd(), 'bilibili_video')  # 当前目录作为下载目录
    #if (sys.platform.startswith('win')):
    #    os.startfile(currentVideoPath)

def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args) 
    # 守护 !!!
    t.setDaemon(True) 
    # 启动
    t.start()


if __name__ == "__main__":
    # 设置标题
    root.title('B站视频下载小助手')
    # 设置ico
    root.iconbitmap('favicon.ico')
    # 设置Logo
    photo = PhotoImage(file='logo.png')
    logo = Label(root,image=photo)
    logo.pack()
    # 各项输入栏和选择框
    inputStart = Entry(root,bd=4,width=600)
    labelStart=Label(root,text="请输入要下载的AID号进行下载或者UP主的UID号获取视频列表 : ") 
    labelStart.pack(anchor="w")
    inputStart.pack()
    labelQual = Label(root,text="或者选择您要下载视频的方式直接下载 : ") 
    labelQual.pack(anchor="w")
    downloadMode = ttk.Combobox(root,state="readonly")
    # 可供选择的表
    downloadMode['value']=('订阅更新','下载列表')
    # 对应的转换字典
    keyTrans=dict()
    keyTrans['订阅更新']='订阅更新'
    keyTrans['下载列表']='下载列表'
    # 初始值为订阅更新
    downloadMode.current(0)
    downloadMode.pack()
    confirm = Button(root,text="  开  始  ",command=lambda:thread_it(do_prepare,inputStart.get(), keyTrans[downloadMode.get()] ))
    msgbox = Text(root)
    msgbox.insert('1.0',"选择订阅更新:\n    根据 Alpha-B.ini 下载UP主最新视频。\n\n"+
                        "选择下载列表:\n    根据 dlist.json 下载列表中视频。\n\n"+
                        "获取视频列表:\n    输入UP主的UID(eg: UID:456065280,296793775),视频列表将写入 id.json文件。\n\n"+
                        "下载单个视频:\n    输入视频列表中的AID(eg: AID:71584262,71559288)\n\n")
    msgbox.pack()
    download=Canvas(root,width=465,height=23,bg="white")
    # 进度条的设置
    labelDownload=Label(root,text="下载进度 : ")
    labelDownload.pack(anchor="w")
    download.pack()
    fill_line1 = download.create_rectangle(0, 0, 0, 23, width=0, fill="green")
    pct=StringVar()
    pct.set('0.0%')
    pctLabel = Label(root,textvariable=pct)
    pctLabel.pack()
    root.geometry("600x600")
    confirm.pack()
    # GUI主循环
    root.mainloop()
    
