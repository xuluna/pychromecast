import time
import pychromecast
import argparse
import os
import sys

parser = argparse.ArgumentParser(
    description="Cast a video in videos directory"
)

parser.add_argument("--cast", "-c", help="File name to cast")
parser.add_argument("--speed", "-r", help="speed to cast", default=1.5, type=int)
parser.add_argument("--play", help="Resume playing", action="store_true")
parser.add_argument("--pause", "-p", help="Pause playing", action="store_true")
parser.add_argument("--stop", "-s", help="Stop playing", action="store_true")

chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Basement TV"])

if not chromecasts:
    print('No chromecast discovered!')
    sys.exit(1)

args = parser.parse_args()

cast = chromecasts[0]
cast.wait()
mc = cast.media_controller

if args.play:
    mc.play()
elif args.pause:
    mc.pause()
elif args.stop:
    mc.stop()
    os.system("rm ~/photos/*.mp4")
elif args.cast is not None:
    os.system(f"cp ~/videos/${args.cast}.mp4 ~/photos/${args.cast}.mp4")
    mc.play_media('http://192.168.10.105/'+args.cast+'.mp4', 'video/mp4', playback_rate=args.speed)
    mc.block_until_active()

browser.stop_discovery()
