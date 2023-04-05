# CopyTube
## About
Download videos from Youtube. I wanted to keep it simple, so it is a simple commandline application.
Enter the link, then enter the filename without extension.
I'd like to note that this project is not fully complete and it would need further completion but I
don't have time for that. Also it can't download high resolutions like 1080p because youtube doesn't combine audio
and video at that resolution (it is seperated into two streams). You would have to download both video and audio seperately
and then combine it with some audio converter like ffmpeg. I use pytube and pydub for this project and
as you can see ffmpeg is directly included. Also crash reports are saved in crash, but you should create an Issue if you find
some errors. Additionally, i have create a settings file (prep.cfg), you can select some settings. I would
suggest you don't change mime_type, if you don't know what you're doing. You can change it if you enable debug and
select a mime_type, but it is not necessary.

## Install
0. Requirements: Python runtime environment
1. Download with git or as zip and unpack
2. Run prepare.bat (it will automatically install python libs)
3. Run down.bat (simple loop to directly download the next vid)
4. Enter Link & Filename without extension
5. Video / audio is located in ./data

Thanks to the devs of pytube, pydub and ffmpeg ❤️ ...
