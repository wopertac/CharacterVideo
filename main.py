from PIL import Image
import os
import sys
import cv2
import time
import yt_dlp
import numpy as np

g2 = np.array([' ', '.', ':', '-', '=', '+', '*', '#', '%', '@'])

def render(img, reverse = False, hdif = 0):
    w, h = os.get_terminal_size()
    h -= hdif

    img = img.resize((w, h), Image.Resampling.LANCZOS)
    img2 = np.array(img)

    t1 = np.array([.299, .587, .114])

    t2 = img2 * t1
    mas = t2.sum(axis=2)

    n2 = 256 / len(g2)

    mas = mas // n2

    mas = np.astype(mas, int)

    mas2 = g2[mas]

    res = ""
    for i in g2[mas]:
        res += "".join(i)
        res += "\n"

    return res

if len(sys.argv) == 1:
    cam = cv2.VideoCapture(0)
    while True:
        w, h = os.get_terminal_size()
        cap, frame = cam.read()
        clrconv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(clrconv)

        t1 = time.time()
        res = render(img, True, hdif = -3)

        dt = time.time() - t1

        print(res)
        print("Frame render time", dt)
        print("FPS:", int(1/dt), "Resolution:", w, h)
elif sys.argv[1] == "-v":
    t = 0
    video = cv2.VideoCapture(sys.argv[2])
    fps = video.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30
    frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    f = frames
    t = frames/fps
    while True:
        w, h = os.get_terminal_size()
        f -= 1
        t1 = time.time()
        cap, frame = video.read()
        if not cap:
            break
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        clrconv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(clrconv)

        res = render(img, hdif = -4)
        print(res)
        print("Time:", str(int(t//60)) + ":" + str(int(t%60)).zfill(2), "Frames left:", int(f))
        dt = time.time() - t1
        dt2 = 1/fps - dt
        print("Frame render time", dt)
        print("FPS:" + str(int(1/dt)) + "/" + str(int(fps)), "Resolution:", w, h)
        if dt2 > 0:
            time.sleep(dt2)
        t -= 1/fps
elif sys.argv[1] == "-l":
    URL = sys.argv[2]
    ydl_opts = {'format': 'best[ext=mp4]', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)
        stream_url = info.get('url') or info.get('formats', [{}])[0].get('url')

    t = 0
    video = cv2.VideoCapture(stream_url)
    fps = video.get(cv2.CAP_PROP_FPS)
    frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    print(fps, frames)
    f = frames
    t = frames / fps
    while True:
        f -= 1
        t1 = time.time()
        cap, frame = video.read()
        if not cap:
            break
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        clrconv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(clrconv)

        res = render(img, hdif = -4)
        print(res)
        print("Time:", str(int(t // 60)) + ":" + str(int(t % 60)).zfill(2), "Frames left:", int(f))
        dt = time.time() - t1
        dt2 = 1 / fps - dt
        print("Frame render time", dt)
        print("FPS:", int(1/dt))
        if dt2 > 0:
            time.sleep(dt2)
        t -= 1 / fps