from pytube import YouTube

import configparser
import os
import datetime

# Create config
config = configparser.ConfigParser()
config.read('prop.cfg')

enter_name = config['main']['enter_name']
auto = config['main']['auto_select']

print('[ Download ]')
link = input("[ Download ] Enter Link -> ")
# Filename without extension
name = ''
if enter_name == 'True':
    name = input("[ Download ] Enter FileName -> ")

try:
    os.mkdir(config['main']['path'])
except:
    pass

try:
    os.mkdir('crash')
except:
    pass

def crash_path():
    return 'crash/' + str(datetime.datetime.now()).replace(':', '-').replace('.', '-')

def log_exception(e):
    p = crash_path()
    f = open(p, "w")
    f.write(str(e))
    exit()

print("[ Download ] Starting ...")

def print_vs(vs):
    print('[ Download ] res =', vs.resolution, '| fps =', vs.fps, '| mime =', vs.mime_type)

def print_vs_ls(vs_ls):
    for idx in range(0, len(vs_ls)):
        vs = vs_ls[idx]
        print('[ Download ] [', idx, '] res =', vs.resolution, '| fps =', vs.fps, '| mime =', vs.mime_type)

def print_as(a_s):
    print('[ Download ] abr =', a_s.abr, '| mime =', a_s.mime_type)

def print_as_ls(as_ls):
    for idx in range(0, len(as_ls)):
        a_s = as_ls[idx]
        print('[ Download ] [', idx, '] abr =', a_s.abr, '| mime =', a_s.mime_type)

yt = None
try:
    yt = YouTube(link)
except Exception as e:
    print('[ Download ] Link does not work ...')
    log_exception(e)

if enter_name == 'False':
    name = yt.streams[0].title

path = config['main']['path'] + name + '.'

vs_ls = yt.streams.filter(type='video')
vs_ls = vs_ls.order_by('resolution')
vs = None
if auto == 'False':
    print('[ Download ]')
    print('[ Download ] > Select video stream <')
    print_vs_ls(vs_ls)
    try:
        vs = vs_ls[int(input('[ Download ] Enter index -> '))]
    except Exception as e:
        print('[ Download ] Enter an index ...')
        log_exception(e)
else:
    vs = vs_ls[-1]
print('[ Download ]')
print('[ Download ] > Selected video stream <')
print_vs(vs)

as_ls = yt.streams.filter(type='audio')
as_ls = as_ls.order_by('abr')
a_s = None
if auto == 'False':
    print('[ Download ]')
    print('[ Download ] > Select audio stream <')
    print_as_ls(as_ls)
    try:
        a_s = as_ls[int(input('[ Download ] Enter index -> '))]
    except Exception as e:
        print('[ Download ] Enter an index ...')
        log_exception(e)
else:
    a_s = as_ls[-1]
print('[ Download ]')
print('[ Download ] > Selected audio stream <')
print_as(a_s)

v_ext = vs.mime_type.split('/')[1]
a_ext = a_s.mime_type.split('/')[1]

vs_p = path + v_ext + '.vs'
as_p = path + a_ext + '.as'

print('[ Download ]')
print('[ Download ] > Download starting <')

try:
    vs.download(output_path=None, filename=vs_p)
    a_s.download(output_path=None, filename=as_p)
except Exception as e:
    print('[ Download ] There was an error during download ...')
    log_exception(e)

a_p = path + 'mp3'
v_p = path + 'mp4'

from subprocess import DEVNULL, STDOUT, check_call, Popen

print('[ Convert ] Starting ...')
print('[ Convert ] Getting audio ...')
p = crash_path() + '.txt'
f = open(p, "w")

Popen('ffmpeg -y -i ' + as_p + ' ' + a_p, stdout=f, stderr=STDOUT, shell=True)

print('[ Convert ] Getting video ...')
p = crash_path() + '.txt'
f = open(p, "w")

Popen('ffmpeg -y -i ' + vs_p + ' -i ' + as_p + ' -c:v copy -c:a aac ' + v_p, stdout=f, stderr=STDOUT, shell=True)

print('[ Convert ] Finished ...')
    