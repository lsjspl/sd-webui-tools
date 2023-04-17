import os
import shutil
import time
import tkinter as tk
from tkinter import messagebox

fileName = ""
base = f"D:\Mr5\Desktop\AI\\video"
workspace = f"{base}\\{fileName}"
src = workspace+"\\src"
inputFolder = workspace+"\\input"
output = workspace+"\\output"
output_h = workspace+"\\output_h"
videoPath = workspace+f"\\{fileName}.mp4"

# 利用ffmpeg视频取帧

# 转换视频


def img2Video(fps, path):
    rename(path)
    timeMill = int(round(time.time() * 1000))
    cmd = f'ffmpeg -f image2 -r {fps} -i "{path}\\%d.png"  -c:v libx264 -crf 1 -preset:v slow -pix_fmt yuv420p  -vf "scale=960:-2" {workspace}\\output_{timeMill}.mp4'
    exeCMD(cmd)


def img2VideoN(fps):
    img2Video(fps, output)


def img2VideoH(fps):
    img2Video(fps, output_h)


def videoInsFrame(videoPath=videoPath, fps=30):
    timeMill = int(round(time.time() * 1000))
    cmd = f'ffmpeg -threads 16 -i {videoPath} -filter_complex minterpolate="fps={fps}" {workspace}\\output_ins_{timeMill}.mp4'
    exeCMD(cmd)


def video2Img(fps=30):
    if os.path.exists(src):
        shutil.rmtree(src)
    os.makedirs(src, exist_ok=True)
    cmd = f'ffmpeg -i {videoPath} -vf fps={fps} {src}\\%d.png'
    exeCMD(cmd)


def video2ImgLimit(fps=30):
    if os.path.exists(src):
        shutil.rmtree(src)
    os.makedirs(src, exist_ok=True)
    cmd = f'ffmpeg -i {videoPath} -vframes {fps} {src}\\%d.png'
    exeCMD(cmd)


def zipVideo(videoPath):
    timeMill = int(round(time.time() * 1000))
    cmd = f'ffmpeg -i {videoPath} -c:v libx265 -x265-params crf=18 {workspace}\\output_zip_{timeMill}.mp4'
    exeCMD(cmd)

def exeCMD(cmd):
    print(cmd)
    os.system(f"powershell.exe -c {cmd}")

def diff_file():
    if not os.path.exists(output):
        os.makedirs(output)
    srcs = set([_ for _ in os.listdir(src)])
    outs = set([_ for _ in os.listdir(output)])
    # fileName1对比fileName2，fileName1中多出来的文件；注意，如果fileName2里有fileName1中没有的文件，也不会筛选出来
    diffs = srcs.difference(outs)
    print(diffs)

    # 删除input文件里的所有文件
    if os.path.exists(inputFolder):
        shutil.rmtree(inputFolder)

    os.makedirs(inputFolder)

    for name in diffs:
        shutil.copyfile(os.path.join(src, name),
                        os.path.join(inputFolder, name))


def rename(path):
    names = os.listdir(path)
    sorted_data = sorted(names, key=lambda x: (
        int(''.join(filter(str.isdigit, x))), ''.join(filter(str.isalpha, x))))
    i = 1
    for name in sorted_data:
        stuffx = name.split(".")[1]
        os.rename(f"{path}\{name}", f"{path}\{i}.{stuffx}")
        i = i+1


def mkdir(path):
    if not os.path.exists(path):
        print(path)
        os.makedirs(path)


def color(str):
    return f"\033[31m{str}\033[0m"


def init(path):

    global fileName, base, workspace, src, inputFolder, output, output_h, videoPath
    fileName = os.path.basename(path).replace(".mp4", "")
    # base = f"D:\Mr5\Desktop\AI\\video"
    base = os.path.dirname(path)
    workspace = f"{base}/{fileName}"
    src = workspace+"/src"
    inputFolder = workspace+"/input"
    output = workspace+"/output"
    output_h = workspace+"/output_h"
    videoPath = path

    for path in [workspace, src, output, output_h, inputFolder]:
        mkdir(path)


def start():
    isStart = False
    fps = 30
    path = r"C:\Users\Administrator\Desktop\a.mp4"

    def startNow():
        nonlocal isStart, fps, path
        isStart = True
        print(color(r"请输入视频地址 default:C:\\Users\Administrator\Desktop\\a.mp4"))
        pathInput = input("请输入:")
        print(color(r"请输入帧率 default:30"))
        inputFps = input("请输入:")
        path = pathInput if pathInput else path
        init(f"{path}")
        if inputFps:
            fps = int(inputFps)

    while (True):
        if isStart is False:
            print("------------------------------------------------------")
            startNow()

        print(color("请输入要执行的操作"))
        print(color("0:初始化视频地址"))
        print(color("1:视频转图片 video2Img(fps)"))
        print(color("2:input图片转视频 img2VideoN(fps)"))
        print(color("3:input_h图片转视频 img2VideoH(fps)"))
        print(color("4:提取src和out的差异帧到input diff_file()"))
        print(color("5:提取前多少帧 video2ImgLimit()"))
        print(color("6:提取src和out的差异帧到input videoInsFrame()"))
        print(color("7:无损压缩视频 zipVideo()"))
        print(color(f"当前配置 fps:{fps} 视频：{path}"))
        result = int(input("请输入:"))

        chooseIndex=0
       # 初始化视频地址
        if result == 0:
            startNow()

        # 视频转帧 fps:每秒多少帧
        if result == 1:
            video2Img(fps)
        # 从output文件夹生成视频fps:每秒多少帧
        if result == 2:
            img2VideoN(fps)

        # 从output_h文件夹生成视频 fps:每秒多少帧
        if result == 3:
            img2VideoH(fps)
        # 对比src和out的差异，并且把output里少的部分提取来到input文件夹里，用于重复生成坏掉的图
        if result == 4:
            diff_file()

        # 提取前多少帧
        if result == 5:
            fpsInput = inputFolder("请输入提取的帧数")
            video2ImgLimit(fpsInput)

        # 对视频进行插帧
        if str == 6:
            path = input("请输入地址")
            fpsInput = input("请输入提取的帧数")
            videoInsFrame(rf"{path}", fpsInput)
        
        if str == 7:
            path = input("请输入地址")
            zipVideo(path)


def startCode(path, fps):
    init(path)
    # 视频转帧 fps:每秒多少帧
    video2Img(fps)
    # 从output文件夹生成视频fps:每秒多少帧
    # img2VideoN(fps)
    # 从output_h文件夹生成视频 fps:每秒多少帧
    # img2VideoH(fps)
    # 对比src和out的差异，并且把output里少的部分提取来到input文件夹里，用于重复生成坏掉的图
    # diff_file()
    # 提取前多少帧
    # video2ImgLimit(fps)
    # 对视频进行插帧
    # videoInsFrame(rf"{path}",fps)

    #zipVideo()


start()

# startCode(r"C:\\Users\Administrator\Desktop\\a.mp4",30)


