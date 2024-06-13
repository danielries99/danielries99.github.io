from TikTokApi import TikTokApi
import asyncio
import os
import json

# Chrome
# - go to the "Network" tab.
# - find the file with "common?msToken..." that is the last on the list
# - Copy the token from the field 'X-Ms-Token'
# token = 'fvt2MXYD38y2e_i-Z9GcTNQql9w2Kine-k9vYCYoSoDZhYkk0XLYdhXuRLwgB8jAxWD3F11oKR3qNWOmFuZ7-1pi0-KdMgJ66-xDxBbzEAgsFVoVDFneCBDbAZmKvkqzT4592td5_o2spy6nx-91wXM='
# token = 'gG8Wu4JDZfHDlD2YFG69dY8Z5OCbgEuncqZ1B-_s5H5kGNOCwhhz6bkgiD3QL0Q3w2DmbxZEcp-xU4pO2ERiEOVT4YOdgaf_W3r3y5c02dRY_CjA3pcMAAAjGwxHpq_7NrhQ3WQL_zTR7T3pIXXQqrY='
token = 'rLv9-x3wFIxPxaaERpmxTjp4qUcctwtgA2JzP6dzD_an0SEd7xOz4u4SpF4Aw1fRTaNKBppDIaOjpzejkaMzta3OQrmsfA495dsqvLGHrhc2Ik6g5pRkqRqBEJae0lD4qnusINC9ZmYvr-M_JmRs0K0='

ms_token = token # os.environ.get("ms_token", token) # get your own ms_token from your cookies on tiktok.com

list_of_vid = []

async def trending_videos():    
    async with TikTokApi() as api:
        
        list_of_vid = []
        
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)  # Added headless = False - Found in Issue on Github
        tag = api.hashtag(name="Decubal")
        # async for video in api.trending.videos(count=5):
        async for video in tag.videos(count=100):
            # print(video)
            # print(video.as_dict)
            list_of_vid.append(video.as_dict)
    
    return list_of_vid





if __name__ == "__main__":
    vid_sample = asyncio.run(trending_videos())
    
    with open("sample_100.json", "w") as outfile: 
        json.dump(vid_sample, outfile)
    
    