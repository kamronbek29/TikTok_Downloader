import json
import os
import random

import requests


HEADERS = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
           }


def main(link):
    print('Getting direct link...')
    download_url = get_url(link)

    print('Downloading the file...')
    file_dir = download_file(download_url)

    print('File downloaded in {}'.format(file_dir))


# Function to get direct url of the file
def get_url(video_url):
    get_video_page = requests.get(video_url, headers=HEADERS)
    video_page_content = get_video_page.content
    video_info = str(video_page_content, 'utf-8').split(
                'application/json" crossorigin="anonymous">')[1].split('</script><script crossorigin')[0]

    result_json = json.loads(video_info)
    page_json = result_json['props']['pageProps']

    if 'videoData' in page_json.keys():
        direct_url = page_json['videoData']['itemInfos']['video']['urls'][0]
    else:
        direct_url = page_json['musicData']['playUrl']['UrlList'][0]

    return direct_url


# Function to download the file
def download_file(url_to_download):
    file_name = str(random.randrange(100000000000))

    if not os.path.exists('downloads'):
        os.mkdir('downloads')

    if any(x in url_to_download for x in ['.mp3', '.m4a']):
        file_directory = 'downloads/{}.mp3'.format(file_name)
    else:
        file_directory = 'downloads/{}.mp4'.format(file_name)

    with open(file_directory, 'wb') as file_to_save:
        file_content = requests.get(url_to_download).content
        file_to_save.write(file_content)

    return file_directory


if __name__ == '__main__':
    input_url = input('Paste TikTok video or music url here: ')
    main(input_url)


