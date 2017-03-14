#!/usr/bin/python3

from sys import argv
import os
import hashlib
import urllib.request as urllib

USER_AGENT = 'SubDB/1.0 (sub_down/0.1; http://github.com/vin8003/sub_down)'


def net_check():
    try:
        data = urllib.urlopen("http://www.google.com")
    except Exception as e:
        print(e)
        print('Please check your internet connection')
        exit()


def get_hash(name):
    try:
        readsize = 64 * 1024
        with open(name, 'rb') as f:
            size = os.path.getsize(name)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()
    except Exception as e:
        print(e)
        print('Unable to calculate hash')
        exit()


def download(f_hash, filename):
    try:
        url = 'http://sandbox.thesubdb.com/?action=download&language=en&hash=' + f_hash
        req = urllib.Request(url)
        req.add_header('User-Agent', USER_AGENT)

        response = urllib.urlopen(req)
        ext = response.info()['Content-Disposition'].split(".")[1]
        file = os.path.splitext(filename)[0] + "." + ext
        with open(file, "wb") as fout:
            fout.write(response.read())
        return 200
    except Exception as e:
        print(e)
        print('Unable to download subtitle')
        exit()


if __name__ == '__main__':
    first, file_name = argv

    net_check()
    file_hash = get_hash(file_name)
    print(download(file_hash, file_name))
