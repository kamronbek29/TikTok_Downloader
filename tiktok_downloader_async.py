import asyncio
import json
import os
import random

import aiohttp


HEADERS = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
           }


async def main(link):
    print('Getting direct link...')
    download_url = await get_url(link)

    print('Downloading the file...')
    file_dir = await download_file(download_url)

    print('File downloaded in {}'.format(file_dir))


# Function to get direct url of the file
async def get_url(video_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url, headers=HEADERS) as get_video_page:
            video_page_content = await get_video_page.content.read()
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
async def download_file(url_to_download):
    file_name = str(random.randrange(100000000000))

    if not os.path.exists('downloads'):
        os.mkdir('downloads')

    if any(x in url_to_download for x in ['.mp3', '.m4a']):
        file_directory = 'downloads/{}.mp3'.format(file_name)
    else:
        file_directory = 'downloads/{}.mp4'.format(file_name)

    async with aiohttp.ClientSession() as session:
        async with session.get(url_to_download, allow_redirects=True) as get_video:
            with open(file_directory, "wb") as file_to_save:
                file_content = await get_video.content.read()
                file_to_save.write(file_content)

    return file_directory


if __name__ == '__main__':
    input_url = input('Paste TikTok video or music url here: ')
    asyncio.run(main(input_url))


