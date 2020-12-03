from __future__ import unicode_literals

import os
from functools import partial
from threading import Thread, Timer
from time import sleep
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

import pygame


class PlayNow:
    music_now = None
    index_music_now = 0
    music_list = None
    directory_music = None
    timer = None


play_now = PlayNow
os.system('pulseaudio --kill')
os.system('jack_control  start')
sleep(2)
pygame.mixer.init()
if not os.path.exists('.name.txt'):
    with open('.name.txt', 'w') as f:
        f.write('.')
else:
    pass
with open('.name.txt', 'r') as g:
    play_now.directory_music = g.read()
files = os.listdir(play_now.directory_music)
os.chdir(play_now.directory_music)
play_now.music_list = files


def grab1():
    Thread(target=grab2).start()


def grab2():
    try:
        import youtube_dl
        import os
        from sys import argv

        # Download data and config

        download_options = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'nocheckcertificate': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
        }

        # Song Directory

        if not os.path.exists(play_now.directory_music):
            os.mkdir(play_now.directory_music)
        else:
            os.chdir(play_now.directory_music)

        # Download Songs
        with youtube_dl.YoutubeDL(download_options) as dl:
            dl.download([url_for_song.get()])
        files = os.listdir(play_now.directory_music)
        play_now.music_list = files
        combo['values'] = files
        messagebox.showinfo('success', 'Your music was successful downloaded from youtube')
    except:
        messagebox.showerror('Error', 'I can`t download music from youtube(Invalid url)')
    url_for_song.delete(0, 'end')


def play2(song):
    if play_now.music_now is None:
        pass
    else:
        play_now.music_now.stop()
        paus11.configure(command=pause1, text='pause')
    try:
        music = pygame.mixer.Sound(play_now.directory_music + '/' + song)
        lbl_value1.configure(text='music: ', bg='green')
        music.play()
        play_now.music_now = music
    except:
        messagebox.showerror('Music Error', 'Invalid music format(only wav)')


def play1():
    if play_now.music_now is None:
        pass
    else:
        play_now.music_now.stop()
        paus11.configure(command=pause1, text='pause')
    lbl_value1.configure(text='playing now: ', bg='green')
    try:
        music = pygame.mixer.Sound(play_now.directory_music + '/' + combo.get())
        music.play()
        play_now.music_now = music
        play_now.index_music_now = play_now.music_list.index(combo.get())
    except:
        messagebox.showerror('Music Error', 'Invalid music format(only wav)')


def apply():
    with open('.name.txt', 'w') as f:
        f.write(dire.get())
    with open('.name.txt', 'r') as g:
        play_now.directory_music = g.read()
    os.chdir(play_now.directory_music)
    files = os.listdir(play_now.directory_music)
    play_now.music_list = files
    combo['values'] = files


def remove_m():
    ans = messagebox.askquestion('Remove', 'Are you sure want to remove song?')
    if ans == 'yes':
        os.remove(play_now.directory_music +'/'+ combo.get())
        files = os.listdir(play_now.directory_music)
        play_now.music_list = files
        combo['values'] = files
        if play_now.music_list.__len__() > play_now.index_music_now + 1:
            play_now.index_music_now = play_now.index_music_now + 1
        else:
            play_now.index_music_now = 0
        combo.current(play_now.index_music_now)


def repeating1():
    while play_now.timer:
        sleep(2)
        if not pygame.mixer.get_busy() and play_now.timer is True:
            next_s()



def repeat():
    play1()
    play_now.timer = True
    t = Thread(target=repeating1)
    t.start()
    rep.configure(command=stop_repeat, text='stop')
    repeating.configure(text='repeating: True', bg='green')


def stop_repeat():
    play_now.timer = False
    pygame.mixer.stop()
    rep.configure(command=repeat, text='repeat')
    repeating.configure(text='repeating: False', bg='yellow')


def pause1():
    pygame.mixer.pause()
    paus11.configure(command=unpause1, text='unpause')
    lbl_value1.configure(text='paused: ', bg='orange')


def unpause1():
    pygame.mixer.unpause()
    paus11.configure(command=pause1, text='pause')
    lbl_value1.configure(text='music: ', bg='green')


def next_s():
    if play_now.music_list.__len__() > play_now.index_music_now + 1:
        play_now.index_music_now = play_now.index_music_now + 1
    else:
        play_now.index_music_now = 0
    combo.current(play_now.index_music_now)
    play2(play_now.music_list[play_now.index_music_now])


def prev_s():
    if 0 < play_now.index_music_now:
        play_now.index_music_now = play_now.index_music_now - 1
    else:
        play_now.index_music_now = play_now.music_list.__len__() - 1
    combo.current(play_now.index_music_now)
    play2(play_now.music_list[play_now.index_music_now])


def rename1():
    ans = messagebox.askquestion('Rename', 'Are you sure want to rename song?')
    if ans == 'yes':
        os.rename(combo.get(), ren.get())
        files = os.listdir(play_now.directory_music)
        play_now.music_list = files
        combo['values'] = files
        combo.current(play_now.index_music_now)
        ren.delete(0, 'end')


window = Tk()
window.title("Voven4ek")
window.geometry('600x350')
content = Frame()
frame = Frame(content, borderwidth=5, relief="ridge", width=600, height=300, bg='blue')
lbl_value = Label(master=content, text="Your music! ", font=("Arial Bold", 30), bg='Orange')
lbl_value.grid(row=0, column=0)
lbl_value1 = Label(master=content, text="chose your song: ", font=("Arial Bold", 12), bg='yellow')
lbl_value1.grid(row=1, column=0)
combo = Combobox(content)
if files.__len__() > 0:
    combo['values'] = files
else:
    combo['values'] = 'No music'
combo.current(0)  # установите вариант по умолчанию
combo.grid(column=1, row=1)
frame.grid(column=0, row=0, columnspan=10, rowspan=10)
content.grid(column=0, row=0)
play_m = Button(content, text="Remove", command=remove_m)
play_m.grid(column=2, row=1)
lbl_value2 = Label(master=content, text="Your music directory:", font=("Arial Bold", 12), bg='yellow')
lbl_value2.grid(row=2, column=0)
dire = Entry(content, width=20)
dire.insert(INSERT, str(play_now.directory_music))
dire.grid(column=1, row=2)
play_m = Button(content, text="Apply", command=apply)
play_m.grid(column=2, row=2)
l = Label(master=content, text="Rename:", font=("Arial Bold", 12), bg='yellow')
l.grid(row=3, column=0)
ren = Entry(content, width=20)
ren.insert(INSERT, str('new_name'))
ren.grid(column=1, row=3)
play_m = Button(content, text="Rename", command=rename1)
play_m.grid(column=2, row=3)
repeating = Label(master=content, text="repeating: False", font=("Arial Bold", 12), bg='yellow')
repeating.grid(row=4, column=0)
rep = Button(content, text="Repeat", command=repeat)
rep.grid(column=1, row=4)
content2 = Frame()
frame1 = Frame(content2, borderwidth=5, relief="ridge", width=600, height=50, bg='green')
frame1.grid(column=0, row=0, columnspan=20, rowspan=10)
play_m = Button(content2, text="Play", command=play1)
play_m.grid(column=1, row=1)
paus11 = Button(content2, text="Pause", command=pause1)
paus11.grid(column=2, row=1)
content2.grid(column=0, row=1)
play_m = Button(content2, text="Previous", command=prev_s)
play_m.grid(column=3, row=1)
play_m = Button(content2, text="Next", command=next_s)
play_m.grid(column=4, row=1)
url_for_song = Entry(content2, width=20)
url_for_song.insert(INSERT, 'Url for youtube music')
url_for_song.grid(column=5, row=1)
play_m = Button(content2, text="Download", command=grab1)
play_m.grid(column=6, row=1)
window.mainloop()
play_now.timer = False
