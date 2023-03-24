import requests
import time
import os
import json
import errno
from urls_list import *

url = ''
file_name = 'Ai'
folder = r'C:\Users\Tagami\OneDrive\Documents\GitHub\ai_art_classification_model\Images\Ai'
res = ''
image_class = 'Ai'
sleep_dur = 2
url_count = len(filtered_urls)

def train_test(url_count):
     print('Running train_test... \n Calculating train_count and test_count...')
     train_count = round(url_count * .8, 0)
     test_count = url_count - train_count
     print(f'Train count: {train_count} \n Test count: {test_count}')
     return train_count

def download_image_list(image_urls, url_count, folder, file_name, sleep_dur, train_count):
        total_link_list = url_count - 1
        x = 0
        while x <= total_link_list:
                if x <= train_count - 1:
                    image_full_name = f'{folder}\\train\\{x}.jpeg' 
                else:
                    image_full_name = f'{folder}\\test\\{x}.jpeg' 
                url = image_urls[x]
                image_full_name = f'{folder}\\train\\{x}.jpeg' 
                img_data = requests.get(url).content
                with open(image_full_name, 'wb') as handler:
                    print(f'Downloading {url.split("/")[-1]} to {image_full_name}')
                    handler.write(img_data)
                    print(f'{file_name} downloaded')
                time.sleep(sleep_dur)
                print(f'Slept for {sleep_dur}')
                x += 1

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
     train_count = train_test(url_count)
     download_image_list(filtered_urls, url_count, folder, file_name, sleep_dur)

if __name__ == "__main__":
    main()