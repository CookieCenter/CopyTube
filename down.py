from pytube import YouTube
from pydub import AudioSegment

import configparser

# Create config
config = configparser.ConfigParser()
config.read('prop.cfg')

link = input("[ Download ] Enter Link -> ")
# Filename without extension
name = input("[ Download ] Enter FileName -> ")

audio = config['main']['only_audio']
convert = config['main']['convert_to_audio']
debug = config['main']['debug']

import os

try:
    os.mkdir(config['main']['path'])
except:
    pass

try:
    os.mkdir('crash')
except:
    pass

import datetime

def log(msg):
    file_name = 'crash/' + str(datetime.datetime.now()).replace(':', '-').replace('.', '-')
    if not os.path.exists(file_name):
        file = open(file_name, "w")
        file.write(msg)

path = config['main']['path'] + name + '.'

# Audio
mime_aud = config['audio']['mime_type']
aud_ext = config['audio']['ext']
abr = config['audio']['abr']

# Video
mime_vid = config['video']['mime_type']
vid_ext = config['video']['ext']
res = config['video']['res']

print("[ Download ] Starting ...")

yt = None
stream = None

down_file_name = ''

try:
    try:
        yt = YouTube(link)
    except Exception as exception:
        log(str(exception))
        print('[ Download ] Link does not work ...')

    if debug == 'True':
        print('[ Download ] Stream list ...')
        for stream in yt.streams:
            if stream.type == 'video':
                print('[ Download ] -> Mime_type =', stream.mime_type, '| Res =', stream.resolution, '| Fps =', stream.fps)
            if stream.type == 'audio':
                print('[ Download ] -> Mime_type =', stream.mime_type, '| Bitrate =', stream.abr)
    
    if audio == 'True':
        stream = None

        print('[ Download ] Bitrate -', abr, '| Mime_type -', mime_aud)
        stream_ls = yt.streams.filter(only_audio=True, mime_type=mime_aud, abr=abr)
        if len(stream_ls) > 0:
            stream = stream_ls.first()
        else:
            print('[ Download ] No stream found -> Trying other bitrate ...')
            stream_ls = yt.streams.filter(only_audio=True, mime_type=mime_aud)

            if len(stream_ls) > 0:
                stream = stream_ls.first()
            else:
                print('[ Download ] No stream found -> Maybe Mimetype wrong ...')
                stream_ls = yt.streams.filter(only_audio=True)

                if len(stream_ls) > 0:
                    print('[ Download ] Chosing first stream without filter ...')
                    stream = stream_ls.first()
                else:
                    print('[ Download ] No stream found at all ...')

        down_file_name = path + 'tmp'
        stream.download(output_path=None, filename=down_file_name)
    else:
        stream = None

        print('[ Download ] Resolution -', res, '| Mime_type -', mime_vid)
        stream_ls = yt.streams.filter(mime_type=mime_vid, res=res)
        if len(stream_ls) > 0:
            stream = stream_ls.first()
        else:
            print('[ Download ] No stream found -> Trying other resolution ...')
            stream_ls = yt.streams.filter(mime_type=mime_vid)

            if len(stream_ls) > 0:
                stream = stream_ls.first()
            else:
                print('[ Download ] No stream found -> Maybe Mimetype wrong ...')
                stream_ls = yt.streams

                if len(stream_ls) > 0:
                    print('[ Download ] Chosing first stream without filter ...')
                    stream = stream_ls.first()
                else:
                    print('[ Download ] No stream found at all ...')

        down_file_name = path + vid_ext
        stream.download(output_path=None, filename=down_file_name)
    
    print("[ Download ] Finished ...")
except Exception as exception:
    log(str(exception))
    print('[ Download ] Err ...')

if convert == 'True':
    print('[ Convert ] Starting ...')
    try:
        AudioSegment.from_file(down_file_name).export(path + aud_ext, format=aud_ext)
        print('[ Convert ] Finished ...')
    except Exception as exception:
        log(str(exception))
        print('[ Convert ] Err, probably audio missing ...')
        print('[ Convert ] At higher res, video and audio is seperate ...')