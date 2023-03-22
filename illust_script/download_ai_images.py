import requests
import time
import os
import json
import errno
from urls_list import *

url = ''
file_name = ''
folder = ''
res = ''
image_class = 'Illust'
sleep_dur = 2
url_count = len(filtered_urls)

def download_image_list(image_urls, url_count, folder, file_name, sleep_dur):
        total_link_list = url_count - 1
        x = -1
        while x <= total_link_list:
                x += 1
                url = image_urls[x]
                image_full_name = folder + '\\' + file_name
                img_data = requests.get(url).content
                with safe_open(image_full_name, 'wb') as handler:
                        print(f'Downloading {url.split("/")[-1]} to {image_full_name}')
                        handler.write(img_data)
                        print(f'{file_name} downloaded')
                time.sleep(sleep_dur)
                print(f'Slept for {sleep_dur}')

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open(path, theb):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, theb)

def main():
     download_image_list(filtered_urls, url_count, folder, file_name, sleep_dur)

if __name__ == "__main__":
    main()