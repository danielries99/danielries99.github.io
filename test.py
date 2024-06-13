import nest_asyncio
import asyncio
from playwright.async_api import async_playwright
from TikTokApi import TikTokApi
import json

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

async def get_tiktok_ms_token():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Go to TikTok homepage
        await page.goto('https://www.tiktok.com/')

        # Wait for a short time to allow tokens to settle
        await page.wait_for_timeout(5000)  # Wait for 5 seconds

        # Refresh the page
        await page.reload()

        # Wait for another short time after refresh
        await page.wait_for_timeout(10000)  # Wait for 5 seconds

        # Get cookies
        cookies = await context.cookies()

        # Extract the ms_token from cookies
        ms_tokens = [cookie['value'] for cookie in cookies if cookie['name'] == 'msToken']

        await browser.close()

        if ms_tokens:
            return ms_tokens[0]  # Return the first ms_token found
        else:
            return None

async def fetch_videos_by_hashtag(ms_token, hashtag):
    async with TikTokApi() as api:
        list_of_vid = []
        
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)
        tag = api.hashtag(name=hashtag)
        async for video in tag.videos(count=5):
            list_of_vid.append(video.as_dict())
    
    return list_of_vid

# Function to run the asyncio code
def run_async(func, *args):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        future = asyncio.ensure_future(func(*args))
        loop.run_until_complete(future)
        return future.result()
    else:
        return loop.run_until_complete(func(*args))

# Example hashtag to search for
hashtag = "Decubal"

# Run the asynchronous function to get the ms_token
ms_token = run_async(get_tiktok_ms_token)
print(f"ms_token: {ms_token}")

# Fetch and print videos by hashtag
videos = run_async(fetch_videos_by_hashtag, ms_token, hashtag)

# Save the first video to a JSON file
if videos:
    with open("sample.json", "w") as outfile:
        json.dump(videos[0], outfile)
