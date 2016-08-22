import sys
import cv2
import numpy
import base64
import urllib2 # TODO python3
import urllib
import subprocess as sp
import socket
import threading
import struct
import Queue
import time
import os
from goprohero import GoProHero
# TODO: toggle GoPro interaction?
camera = None
WEBURL = "http://10.5.5.9:8080/"
FFMPEG_BIN = "ffmpeg"
# HOST = "192.168.0.109"
HOST = "127.0.0.1"
# PORT = 5551
PORT = 8888

# goProPass = os.environ.get('LOCAL_GOPRO')
goProPass = 'PumpTh3J4m1985'

# Establish connection if ENV variable doesn't exist
# while goProPass == None:
#     goProPass = raw_input("enter GoPro password: ")


def streamToOpenCV ():
    # http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
    VIDEO_URL = WEBURL + "live/amba.m3u8"

    cv2.namedWindow("GoPro",cv2.CV_WINDOW_AUTOSIZE)
    # https://docs.python.org/2/library/subprocess.html#popen-constructor
    pipe = sp.Popen([ FFMPEG_BIN, "-i", VIDEO_URL,
               "-loglevel", "quiet", # no text output
               "-an",   # disable audio
               "-f", "image2pipe",
               "-pix_fmt", "bgr24",
               "-vcodec", "rawvideo", "-"],
               stdin = sp.PIPE, stdout = sp.PIPE)
    while True:
        raw_image = pipe.stdout.read(432*240*3) # read 432*240*3 bytes (= 1 frame)
        image =  numpy.fromstring(raw_image, dtype='uint8').reshape((240,432,3))
        cv2.imshow("GoPro",image)
        if cv2.waitKey(5) == 27:
            break
    cv2.destroyAllWindows()

def retrieveJson (resource):
    return urllib2.urlopen(resource).read()


# def postFrame (resource, encoded = False, img = None):
#     img = "media/test.jpg" if img is None else img
#     if not encoded:
#         with open(img, "rb") as image_file:
#             encoded_image = base64.b64encode(image_file.read())
#     else:
#         encoded_image = img
#
#     raw_params = {'image': encoded_image} # TODO figure out payload structure for API
#     params = urllib.urlencode(raw_params)
#     request = urllib2.Request(resource, params)
#     # request.add_header("Content-type", "application/x-www-form-urlencoded; charset=UTF-8")
#     resource = urllib2.urlopen(request)
#     info = resource.read()
#
# def postJson (url, jObject):
#     data = urllib.urlencode(jObject)
#     req = urllib2.Request(url, data)
#     response = urllib2.urlopen(req)
#     return response.read()

def send(sock, payload):
    try:
        sock.connect((HOST, PORT))
        sock.sendall(payload)
        print sock.recv(1024)
    finally:
        return True

def connectToServer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    conversing = True
    print "Conversin"
    while conversing:
        try:
            sock.connect((HOST, PORT))
            with open("media/test.jpg", "rb") as imageFile:
                f = imageFile.read()
                b = bytearray(f)

            sock.send(b)
            print sock.recv(1024)
        finally:
            return True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

try:
    while(1):
        msg = sock.recv(1024)
        msg = msg.strip()
        if("CurrFrame" in msg):
            print "got frame request"
            # GENERATES AN IMAGE
            VIDEO_URL = WEBURL + "live/amba.m3u8"
            print "have a vid URL"
            # https://docs.python.org/2/library/subprocess.html#popen-constructor
            # pipe = sp.Popen([ FFMPEG_BIN,
            #            "-i", VIDEO_URL,
            #            "-loglevel", "quiet", # no text output
            #            "-an", # disable audio
            #            "-f", "image2pipe",
            #            "-pix_fmt", "bgr24", # GoPro funkeh
            #            "-vcodec", "rawvideo", "-"],
            #            stdin = sp.PIPE, stdout = sp.PIPE)
            print "about to read from pipe"
            # while True:
            #     print "inf loop?"
            #     raw_image = pipe.stdout.read(432*240*3)
            #     print "not stuck on pipe read"
            #     if len(raw_image) < 10:
            #         print "sm len"
            #         continue
            #     image = numpy.fromstring(raw_image, dtype='uint8').reshape((240,432,3))
            #     success = cv2.imwrite('media/omg.png',image)
            #     if success:
            #         break
            print "about to open img"
            with open("media/omg.png", "rb") as imageFile:
               f = imageFile.read()
               b = bytearray(f)
            newMsg = "SendingFrame,%d\n" % len(b)
            print "sending: " + newMsg
            sock.sendall(newMsg)
            sock.send(b)
            print "finished sending frame"

except KeyboardInterrupt:
    print "Ctrl-c pressed ..."
    sock.close()
    sys.exit(1)
finally:
    sock.close()


#while True:
    #command = input("supply url for GET: ")
    #send(command)
    #print postFrame("http://localhost:3000/images")

# Start interfaceing
while True:
    command = int(input("What would you like to do: "))
    if command == 0:
        break
    #cameraOpts.get(command)
    if command == 1:
        camera.command('record', 'on')
    elif command == 2:
        camera.command('record', 'off')
    elif command == 3:
        camera.command('preview', 'on')
    elif command == 4:
        camera.command('preview', 'off')
    elif command == 5:
        VIDEO_URL = WEBURL + "live/amba.m3u8"
        # https://docs.python.org/2/library/subprocess.html#popen-constructor
        pipe = sp.Popen([ FFMPEG_BIN,
                   "-i", VIDEO_URL,
                   "-loglevel", "quiet", # no text output
                   "-an", # disable audio
                   "-f", "image2pipe",
                   "-pix_fmt", "bgr24", # GoPro funkeh
                   "-vcodec", "rawvideo", "-"],
                   stdin = sp.PIPE, stdout = sp.PIPE)
        while True:
            # So the
            raw_image = pipe.stdout.read(432*240*3)
            if len(raw_image) < 10:
                continue
            image = numpy.fromstring(raw_image, dtype='uint8').reshape((240,432,3))
            success = cv2.imwrite('media/omg.png',image)
            if success:
                break
    else:
        pass
    #
    # elif command == 6:
    #     print "hey"
    #     break
    # elif command == 7:
    #     #http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
    #     # VIDEO_URL = WEBURL + "live/amba.m3u8"
    #     # VIDEO_URL = "http://10.5.5.9/gp/gpControl/execute?p1=gpStream&c1=restart"
    #
    #     cv2.namedWindow("GoPro",cv2.CV_WINDOW_AUTOSIZE)
    #
    #     pipe = sp.Popen([ FFMPEG_BIN, "-i", VIDEO_URL,
    #                "-loglevel", "quiet",  #no text output
    #                "-an",    #disable audio
    #                "-f", "image2pipe",
    #                "-pix_fmt", "bgr24",
    #                "-vcodec", "rawvideo", "-"],
    #                stdin = sp.PIPE, stdout = sp.PIPE)
    #     while True:
    #         raw_image = pipe.stdout.read(432*240*3)#read 432*240*3 bytes (= 1 frame)
    #         image =  numpy.fromstring(raw_image, dtype='uint8')#.reshape((240,432,3))
    #         cv2.imshow("GoPro",image)
    #
    #         if cv2.waitKey(5) == 27:
    #             break
    #     cv2.destroyAllWindows()
