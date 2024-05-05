###Updateプログラムの組み込み完了 2/10###
###try構文を組み込んだが絶対にexceptに飛ばされるエラー 2/14###
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import time
import re
from urllib import request
from bs4 import BeautifulSoup
import urllib.request, urllib.error
import sys
import codecs
import threading
import os

def home():
    frame_home.tkraise()
def DP():
    frame_dl.tkraise()
def UP():
    frame_up.tkraise()
def wait():
    frame_wait.tkraise()
def comp():
    frame_comp.tkraise()
def Er():
        frame_Er.tkraise()
def close():
        sys.exit()

###download###
def checkURL(tem,ncode,nm,fld_name):
        try:
            wait()
            Pb.start(100)
            f = urllib.request.urlopen(tem)
            print ("OK:" + tem )
            info_url = "https://ncode.syosetu.com/novelview/infotop/ncode/{}".format(ncode)
            info_res = request.urlopen(info_url)
            soup = BeautifulSoup(info_res, "html.parser")
            pre_info = soup.select_one("#pre_info").text
            num_parts = int(re.search(r"全([0-9]+)部分", pre_info).group(1))
            print(nm)
            print(num_parts)
            with codecs.open(
                "{}\\{}({}_{}).txt".format(fld_name,nm,ncode,num_parts),
                "w",
                encoding="utf-8"
                ) as f:
                for part in range(1, num_parts+1):
                    label_DLed = ttk.Label(
                        frame_wait,
                        text="{}/{} downloaded".format(part,num_parts),
                        )
                    label_DLed.pack()
                    url= "{}/{:d}".format(tem, part)
                    res = request.urlopen(url)
                    soup = BeautifulSoup(res, "html.parser")
                    honbun = soup.select_one("#novel_honbun").text
                    honbun += "\n"
                    f.write(honbun)
                    print("{:d}/{:d} downloaded ".format(part, num_parts))
                    time.sleep(0.3)
                    label_DLed.pack_forget()
            f.close()
            Pb.stop()
            print("completed")
            comp()
        except:
            print("NOT FOUND:" + tem)
            Pb.stop
            Er()

def get():
        ncode = entry_nc.get()
        nm = entry_nm.get()
        nm = nm.strip()
        dir = 'C:\\'
        fld_name = filedialog.askdirectory(initialdir = dir)
        print(fld_name)
        tem = "http://ncode.syosetu.com/{}".format(ncode)
        thread = threading.Thread(target=checkURL,args=[tem,ncode,nm,fld_name])
        thread.start()

###Update###
def createList(n):
    lst = []
    for i in range(n+1):
        lst.append(i)
    return(lst)

def deff(x, y):
    return list(set(x) ^ set(y))

def select():
    #更新対象指定
    typ = [('テキストファイル','*.txt')]
    dir = 'C://Users/h_ab/Documents/programs/my_novels/'
    fle_path = filedialog.askopenfilename(filetypes = typ, initialdir = dir).replace("/", "\\")
    fle = os.path.basename(fle_path)
    print(fle)
    thread = threading.Thread(
        target=update,
        args=[fle_path, fle]
        )
    thread.start()

def update(fle_path, fle):
        #name,ncode,old_patsの抽出
        wait()
        Pb.start(100)
        name = (re.sub("\(.+?\.txt", "", fle))
        ncode = (re.findall("(?<=\().+?(?=\_)", fle))[0]
        old_parts = (re.findall("(?<=\_).+?(?=\))", fle))[0]
        old_parts = createList(int(old_parts))
        print(name)
        print(old_parts)

        # 全部分数を取得
        info_url = "https://ncode.syosetu.com/novelview/infotop/ncode/{}/".format(ncode)
        info_res = request.urlopen(info_url)
        soup = BeautifulSoup(
            info_res,
            "html.parser"
            )
        pre_info = soup.select_one("#pre_info").text
        new_parts_num = int(
            re.search(r"全([0-9]+)部分",pre_info).group(1))
        print(new_parts_num)
        new_parts = createList(int(new_parts_num))
        print(new_parts)

        #取得する部分のリスト作成
        get_parts = deff(old_parts, new_parts)
        if not get_parts:
            print("This file is already up to date.")
            Pb.stop
            comp()
        else:
            print(get_parts)
            progress_num = min(get_parts)
            max_num= max(get_parts)
            for part in get_parts:
                label_DLed = ttk.Label(
                    frame_wait,
                    text="{}/{} downloaded".format(part,new_parts_num),
                    )
                label_DLed.pack()
                # 作品のURL
                url = "https://ncode.syosetu.com/{}/{:d}/".format(ncode, part)
                res = request.urlopen(url)
                soup = BeautifulSoup(res, "html.parser")
                #本文を指定
                honbun = soup.select_one("#novel_honbun").text
                honbun += "\n"
                #保存
                with codecs.open(fle_path, "a", encoding="utf-8") as f:
                    f.write(honbun)
                # 進捗を表示
                print("part {:d} downloaded (rest: {:d} parts)".format(progress_num, max_num))
                progress_num = progress_num + 1
                label_DLed.pack_forget()
                time.sleep(0.3)

            #file name update
            fle_path_new = fle_path.replace(str(old_parts[-1]), str(new_parts_num))
            os.rename(fle_path, fle_path_new)
            Pb.stop
            print("completed")
            comp()

#window
root = tk.Tk()
root.title("narou_downloader")
root.geometry("256x192")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
#frame
frame_home = tk.Frame(root)
frame_home.grid(
    row=0,
    column=0,
    sticky="nsew",
    pady=20
    )
frame_dl = tk.Frame(root)
frame_dl.grid(
    row=0,
    column=0,
    sticky="nsew",
    pady=20
    )
frame_up = tk.Frame(root)
frame_up.grid(
    row=0,
    column=0,
    sticky="nsew",
    pady=20
    )
frame_wait = tk.Frame(root)
frame_wait.grid(
    row=0,
    column=0,
    sticky="nsew",
    pady=20
    )
frame_comp = tk.Frame(root)
frame_comp.grid(
    row=0,
    column=0,
    sticky="nsew",
    pady=20
    )
frame_Er = tk.Frame(root)
frame_Er.grid(
    row=0,
    column=0,
    sticky="nsew",
    pady=20
    )
#widget#
#home
label_home = ttk.Label(
    frame_home,
    text="Welcome to NR_Downloader!!",
)
button_DP = ttk.Button(
    frame_home,
    text="Download",
    command=DP
)
button_UP = ttk.Button(
    frame_home,
    text="update",
    command=UP
)
#dl
label_nc = ttk.Label(
    frame_dl,
    text="Please enter the N code of the work.",
    anchor=tk.CENTER
    )
entry_nc = tk.Entry(frame_dl)
label_nm = ttk.Label(
    frame_dl,
    text="Please enter the work name.",
    anchor=tk.CENTER)
entry_nm = tk.Entry(frame_dl)
button_DL = ttk.Button(
    frame_dl,
    text="download",
    command=get
    )
label_dl = ttk.Label(
    frame_wait,
    text="Please wait..."
)
Pb = ttk.Progressbar(
    frame_wait,
    maximum=10,
    value=0,
    length=200,
    mode='indeterminate'
    )
label_comp = ttk.Label(
    frame_comp,
    text="completed"
    )
button_home = ttk.Button(
    frame_dl,
    text="home",
    command=home
    )
button_comp = ttk.Button(
    frame_comp,
    text="home",
    command=home
    )
button_exit = ttk.Button(
    frame_comp,
    text="exit",
    command=close
    )
label_Er = ttk.Label(
    frame_Er,
    text="Error"
    )
button_Er = ttk.Button(
    frame_Er,
    text="home",
    command=home
    )
#up
label_up = ttk.Label(
    frame_up,
    text="Select to file",###英語テキトー直し必要
    anchor=tk.CENTER
)
button_select = ttk.Button(
    frame_up,
    text="select",
    command=select
)
button_home_up = ttk.Button(
    frame_up,
    text="home",
    command=home
    )
#pack
#home
label_home.pack()
button_DP.pack()
button_UP.pack()
#dl
label_nc.pack()
entry_nc.pack()
label_nm.pack()
entry_nm.pack()
button_DL.pack()
label_comp.pack()
button_home.pack()
button_exit.pack()
label_Er.pack()
button_Er.pack()
button_comp.pack()
label_dl.pack()
Pb.pack()
#up
label_up.pack()
button_select.pack()
button_home_up.pack()

frame_home.tkraise()
root.mainloop()
