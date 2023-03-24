import errno
import time
import requests
import os
import json
# import tweepy
import pandas as pd
import numpy as np
from illust_urls_list import *

try:
       filtered_urls
       print('Variable filtered_urls exists.')
except NameError:
       filtered_urls = []
       print("Variable filtered_urls doesn't exist. New variable [filtered_urls] created.")

consumer_key = "5niJQn0HKrTqrVXJiEbPy4oe8" #Your API/Consumer key 
consumer_secret = "ukvUPN8Gtn6t0rCaFcZ64szPUMT4kR9JEPku8sWNoEBbWwYnND" #Your API/Consumer Secret Key
access_token = "1394043240844652545-YVJiE6UEbAndM80sjO0bZAJuJerdBO"    #Your Access token key
access_token_secret = "lbXb7yZ9Eb48Mfcj42EwC4EVKVLkCjj5t7CKQUXvMAeSn" #Your Access token Secret key
bearer_token = "AAAAAAAAAAAAAAAAAAAAABP%2BigEAAAAAG%2FDNqABohIVFg8bWcfJqf33PAnI%3DUgD5Hz6mPyN7lSC5UJ0rmMAXjw8vdBqySDSqjCQHjKIutr8PQc"
og_filtered_urls_count = len(filtered_urls)
max_results = 50
minimum_likes = 1
search_url = "https://api.twitter.com/2/tweets/search/recent"
query_params = {'query': '(#illustration OR #rkgk OR #イラスト) has:media -is:retweet', 'expansions': 'attachments.media_keys', 'tweet.fields': 'author_id,created_at,public_metrics,possibly_sensitive', 'media.fields': 'url', 'max_results':max_results}
file_name = 'AI_test'
folder = r'C:\Users\Tagami\OneDrive\Documents\GitHub\ai_art_classification_model\illust_script\illust_urls_list.py'
urls_file = r'C:\Users\Tagami\OneDrive\Documents\GitHub\ai_art_classification_model\illust_script\illust_urls_list.py'
loop_count = 1
sleep_duration = 60

# Bearer OAuth2 Function
def bearer_oauth(r):
        """
        Method required by bearer token authentication.
        """
        print(f'Running bearer_oauth({r})')
        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r
    
# Connect to endpoint to retrieve JSON
def connect_to_endpoint(url, params):
        print(f"# Running function connect_to_endpoint({url}, {params})")
        response = requests.get(url, auth=bearer_oauth, params=params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

#Get Tweets function nesting all other functions
def get_tweets(loop_count, sleep_duration, filtered_urls):
        print("# Running function get_tweets()...")
        media_count = 0 #number of images to get (unused)
        array_count = -1 #The n'th array that the current tweet belongs in
        filtered_count = 0 #The number of filtered tweets in total
        possibly_sensitive_count = 0 #The number of possibly sensitive tweets
        not_enough_likes_count = 0 
        no_url_found_count = 0
        errored_tweets = []
        valid_tweets = []
        json_response = connect_to_endpoint(search_url, query_params)
        # print(json.dumps(json_response, indent=4, sort_keys=True))
        url_counter(json_response)
        # For function to call for every media key in array
        for y in json_response['data']:
            array_count += 1
            #and y['possibly_sensitive'] is False
            if y['public_metrics']['like_count'] >= minimum_likes and 'url' in json_response['includes']['media'][array_count]:
                filtered_count += 1
                valid_tweets.append(array_count)
                print(f"Tweet {array_count} accepted.")
            elif y['public_metrics']['like_count'] < minimum_likes:
                    not_enough_likes_count += 1
            elif y['possibly_sensitive'] is True:
                    possibly_sensitive_count += 1
            elif not 'url' in json_response['includes']['media'][array_count]:
                    no_url_found_count += 1
            else:
                errored_tweets.append(array_count)
                print(f'!!! Tweet {array_count} errored. !!!')
        print(f"{not_enough_likes_count + possibly_sensitive_count} rejected; \n {not_enough_likes_count} had less than {minimum_likes} likes; \n {possibly_sensitive_count} were possibly sensitive; \n {no_url_found_count} tweets had no url; \n {filtered_count} tweets accepted; \n {len(errored_tweets)} tweets rejected: Tweets {errored_tweets};")
        # print_image_url2(valid_tweets, json_response)
        filtered_urls = filter_urls(get_media_keys(valid_tweets, json_response, filtered_urls, urls_file, loop_count, sleep_duration))

        return filtered_urls

        # write_url_to_file(filtered_urls, urls_file, og_filtered_urls_count)




def test_current_mk(json_response, image_urls, i, sf, no_url, media_keys, fail):
      cmk_image_url = []
      for y in json_response['includes']['media']:
                testing_media_key = [y['media_key']]
                tmk_str = testing_media_key[0]
                # print(f'Media_array: {tmk_str}')

                if tmk_str == i and 'url' in y:
                                cmk_image_url = y['url']
                                
                                image_urls.append(cmk_image_url)
                                # print(f'Url obtained: {cmk_image_url}')
                                sf = 1

                elif tmk_str == i and not 'url' in y:
                                print(f'No URL found for Media Key [{testing_media_key}]')
                                no_url += 1
                if sf == 1:
                        print(f'URL for Media Key {i} obtained.\n Proceeding to next Media Key')
                        break
                else:
                        fail += 1
                        print(f'[{sf}] Failed to obtain URL for Media Key {i}. \n Proceeding to next Media Key')
                        break

def get_media_keys(valid_tweets, json_response, image_urls, urls_file, loop_count, sleep_duration):
      media_keys = []
      fail = 0
      no_url = 0
      for x in valid_tweets:
            num_of_media_keys = len(json_response['data'][x]['attachments']['media_keys'])
            media_key_countdown = num_of_media_keys
            media_keys_of_tweet = []
            while media_key_countdown >= 0:
                   current_media_keys = json_response['data'][x]['attachments']['media_keys'][media_key_countdown - 1]
                   media_keys.append(current_media_keys)
                   media_keys_of_tweet.append(current_media_keys)
                   media_key_countdown -= 1
                   
           # print(f'Media Keys of Tweet {x} [{num_of_media_keys}] Keys:\n{media_keys_of_tweet}')
      og_len_mk = len(media_keys)
      media_keys = list(dict.fromkeys(media_keys))
      media_key_count = len(media_keys)
      print(f'{og_len_mk - media_key_count} duplicates deleted.')
      # print(f'all media keys: {media_keys}')
      for i in media_keys:
       # print(f'Seaching for {i}...')
        sf = 0
        #test_current_mk(json_response, image_urls, i, sf, no_url, media_keys, fail)
        cmk_image_url = []
        for y in json_response['includes']['media']:
                        testing_media_key = [y['media_key']]
                        tmk_str = testing_media_key[0]
                        # print(f'Media_array: {tmk_str}')

                        if tmk_str == i and 'url' in y:
                                cmk_image_url = y['url']
                                
                                image_urls.append(cmk_image_url)
                               # print(f'Url obtained: {cmk_image_url}')
                                sf = 1

                        elif tmk_str == i and not 'url' in y:
                                print(f'No URL found for Media Key [{testing_media_key}]')
                                no_url += 1
        if sf == 1:
                print(f'URL for Media Key {i} obtained.\n Proceeding to next Media Key')
                                
        else:
                fail += 1
                print(f'[{sf}] Failed to obtain URL for Media Key {i}. \n Proceeding to next Media Key')
                                
      image_url_count = len(image_urls)
      #print(f'All Media Keys attempted. \n All URLS: {image_urls}')
      print(f'All Media Keys attempted. \n All URLS: [image_urls]')
      print(f'Fetch failed for [{fail}] media keys. \n{no_url} links were missing')
      print(f'{image_url_count} out of {media_key_count} were obtained.')
      print(f'{image_url_count} URLS / {media_key_count} Media Keys / {valid_tweets} Valid Tweets')
      return image_urls

      # write_to_file(list_to_string(image_urls), file_name)
      # download_image_list(image_urls, image_url_count, folder)


def print_image_url(valid_tweets, json_response):
      image_urls = [json_response['includes']['media'][i]['url'] for i in valid_tweets]
      # print(image_urls)

def print_image_url2(media_keys, json_response):
      for i in media_keys:
            # print([json_response['includes']['media'][i]['url']])
            current_tweet_urls = np.array([json_response['includes']['media'][i]['url']])
            number_of_urls = len(current_tweet_urls)
            # print(f'Tweet {i} // {tweet_number}/{number_of_valid_tweets} // {len(current_tweet_urls)} Urls Found // \n {current_tweet_urls}')

def url_counter(json_response,):
        url_count = 0
        for x in json_response['includes']['media']:
              if 'url' in x:
                
                print(x['url'])
                url_count += 1
              else:
                    print('no_url')
        print(f"{url_count} illustrations found")

def write_to_file(text, file_name):
       print(f'Opening file [{file_name}]')
       f = open(file_name, "a")
       print(f'Writing to {file_name} \n {text}')
       f.write(text)
       print('Finished writing.')
       f.close()

def list_to_string(x):
       s = ''.join(x)
       print(type(s))
       print (s)
       return s

def filter_urls(image_urls):
        og_len_urls = len(image_urls)
        filtered_urls = list(dict.fromkeys(image_urls))
        url_count = len(filtered_urls)
        print(f'{og_len_urls - url_count} duplicate urls deleted.')
        # print(f'all urls: {filtered_urls}')
        return filtered_urls

def write_url_to_file(filtered_urls, file, og_filtered_urls_count):
       #open file
        opened_file = safe_open(file, "w")
        print(f'File {file} opened')
 
#convert variable to string
        str = repr(filtered_urls)
        print('Convereted filtered_urls to string')
        opened_file.write("filtered_urls = " + str + "\n")
        print(f'Succesfully written to {file}')

 
#close file
        opened_file.close()
        print(f'Closed file {file}')
        f = safe_open(file, 'r')
        contents= f.read()
        print(f'CONTENTS: \n     {contents}')

#count
        filtered_urls_count = len(filtered_urls)
        new_urls_count =  filtered_urls_count - og_filtered_urls_count
        print(f'{filtered_urls_count} Total Urls \n {og_filtered_urls_count} Old Urls \n {new_urls_count} New Urls')

def clear_filtered_urls(file):
       filtered_urls = []
       str = repr(filtered_urls)
       print('Created empty filtered_urls and converted to string')
       opened_file = safe_open(file, 'w')
       print(f'Opened file [{file}]')
       opened_file.write("filtered_urls = " + str + "\n")
       print(f'Succesfully written to {file}')
       
       opened_file.write("filtered_urls = " + "\n")
def download_image_list(image_urls, image_url_count, folder):
        total_link_list = image_url_count - 1
        x = -1
        buffer = 4
        while x <= total_link_list:
                x += 1
                url = image_urls[x]
                image_name = url.split("/")[-1]
                image_full_name = folder + '\\' + image_name
                img_data = requests.get(url).content
                with safe_open(image_full_name, 'wb') as handler:
                        print(f'Downloading {image_name} to {image_full_name}')
                        handler.write(img_data)
                        print(f'{image_name} downloaded')
                time.sleep(buffer)
                print(f'Slept for {buffer}')


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
      print('huh')
      try:
             c_loop
             print('c_loop exists.')
      except: 
             c_loop = 0
             print('c_loop created.')
      while not c_loop > loop_count -2:
               c_loop += 1
               get_tweets(loop_count, sleep_duration, filtered_urls)
               print('[get_media_keys] has run ', c_loop, 'times')
               print('Sleeping for', sleep_duration)
               time.sleep(sleep_duration)
               print('Running gettweets')
      else:
               print('############Ran get_media_keys', c_loop, 'times###########')
               write_url_to_file(get_tweets(loop_count, sleep_duration, filtered_urls), urls_file, og_filtered_urls_count)

if __name__ == "__main__":
    main()