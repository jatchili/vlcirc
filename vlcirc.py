#
# Usage:
# python vlcirc.py /path/to/video/file irc_channel
#
# Example: (Linux and MacOS)
#
# 1) Execute command:
#    python vlcirc.py /home/mindey/AlienPlanet.avi MindeyXX1
# 2) Open website:
#    http://webchat.freenode.net/?channels=MindeyXX1
# 3) Once all of your friends had come to channel, type:
#    PLAY @45:18
#    or just
#    PLAY
#
# Will start VLC player on all of the friends' computers almost simultaneously.
#
# For convenience, you may consider adding some thing like:
#        alias vlci='python /home/mi/vlcirc.py $*'
# to your ~/.bashrc

#
# Example: (Windows)
# 
# cp vlcirc.py C:\Python27\
# cp AlienPlanet.avi C:\Python27\
# cd C:\Python27\
# python.exe vlcirc.py AlienPlanet.avi MindeyXX1
#
# This project is licensed under GPLv3.0 license:
# http://www.gnu.org/licenses/gpl-3.0.txt

from random import random
from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
from os import system
from os.path import exists
from platform import system as syst
from time import sleep

video_path = argv[1]
irc_nickname = 'VLC_'+str(int(random()*10**5))
irc_channel = argv[2]
try:
  correction = float(argv[3])
except:
  correction = 0

# IRC Connect
network = 'irc.freenode.net'
port = 6667
irc = socket ( AF_INET, SOCK_STREAM )
irc.connect ( ( network, port ) )
print irc.recv ( 4096 )
irc.send ( 'NICK %s\r\n' % irc_nickname )
irc.send ( 'USER %s PyIRC PyIRC :Python IRC\r\n' % irc_nickname )
irc.send ( 'JOIN #%s\r\n' % irc_channel)

# IRC Stream
def ircstream():
  while True:
    data = irc.recv ( 4096 )
    print data # IRC channel data
    if 'End of /NAMES list' in data:
      print "Now, join the channel: http://webchat.freenode.net/?channels=%s channel, and type 'PLAY @2:00' to start video at 2:00." % irc_channel 
    if ('PLAY' in data):
      if 'PLAY @' in data:
        T = [int(t) for t in data.split('PLAY @')[1].split(' ')[0].split(':')]
        if len(T) == 3:
          time = T[0]*3600+T[1]*60+T[2]
        elif len(T) == 2:
          time = T[0]*60+T[1]
        elif len(T) == 1:
          time = T[0]
        else:
          time = 0
      else:
        time = 0
      if correction > 0:
        sleep(correction)
      # Linux
      if syst()=='Linux':
        system('vlc --start-time %s %s &' % (time,video_path))
      # Mac-OS
      elif syst()=='Darwin':
        if exists('/Applications/VLC.app/Contents/MacOS/VLC'):
          system('/Applications/VLC.app/Contents/MacOS/VLC --start-time %s %s &' % (time,video_path))
        else:
          versions = ['1.1.2', '1.1.3', '1.1.4', '1.1.4.1', '1.1.5', '1.1.6', '1.1.7', '1.1.8', '1.1.9', \
                      '2.0.0', '2.0.1', '2.0.2', '2.0.3', '2.0.4', '2.0.5', '2.0.6']
          # If your version is not here, more versions are: http://download.videolan.org/pub/videolan/vlc/
          for version in versions:
            if exists('/Volumes/vlc-%s/VLC.app/Contents/MacOS/VLC' % version):
              system('/Volumes/vlc-%s/VLC.app/Contents/MacOS/VLC --start-time %s %s &' % (version,time,video_path))
              break
      # Win-OS
      elif syst()=='Windows':
        if exists('C:\\Program Files\\VideoLAN\\VLC\\vlc.exe'):
            system('"C:\\Program Files\\VideoLAN\\VLC\\vlc.exe" --start-time %s %s &' % (time,video_path))
        if exists('C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe'):
            system('"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe" --start-time %s %s &' % (time,video_path))
  pass

# Main
ircstream()
