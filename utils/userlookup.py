import aiohttp
import asyncio
from tabulate import tabulate
from datetime import datetime
import time

# CLI colors
white = "\033[97m"
red = "\033[91m"
BEFORE = "["
AFTER = "]"
ADD = "[+]"
INPUT = "[?]"
WAIT = "[~]"

def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def Slow(text, delay=0.03):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

# Generate similar usernames
def generate_similar_usernames(username, limit=None):
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789-_'
    similar = set()
    # Replace each character
    for i in range(len(username)):
        for c in alphabet:
            if username[i] != c:
                similar.add(username[:i] + c + username[i+1:])
    # Insert characters
    for i in range(len(username) + 1):
        for c in alphabet:
            similar.add(username[:i] + c + username[i:])
    # Delete characters
    for i in range(len(username)):
        similar.add(username[:i] + username[i+1:])
    if limit:
        return list(similar)[:limit]
    return list(similar)

# Check a single URL
async def check_site(session, site, url, found):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    try:
        async with session.get(url, headers=headers, timeout=5) as resp:
            if resp.status == 200:
                found.append((site, url))
                print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} Username found on {site}: {white}{url}{red}")
            elif resp.status == 429:
                print(f"{BEFORE}{current_time_hour()}{AFTER} [!] Rate limit hit for {site}, skipping {url}")
    except:
        pass

# Check usernames for a platform
async def check_platform_usernames(session, platform, username, limit=None):
    sites = {
        "GitHub": "https://github.com/{}",
        "Reddit": "https://www.reddit.com/user/{}",
        "Facebook": "https://www.facebook.com/{}",
        "Twitter": "https://twitter.com/{}",
        "Instagram": "https://www.instagram.com/{}/",
        "TikTok": "https://www.tiktok.com/@{}",
        "Pinterest": "https://www.pinterest.com/{}/",
        "YouTube": "https://www.youtube.com/{}",
        "GitLab": "https://gitlab.com/{}",
        "Bitbucket": "https://bitbucket.org/{}/",
        "Medium": "https://medium.com/@{}",
        "Steam": "https://steamcommunity.com/id/{}",
        "Twitch": "https://www.twitch.tv/{}",
        "DeviantArt": "https://www.deviantart.com/{}",
        "Flickr": "https://www.flickr.com/people/{}/"
    }
    found = []

    # Decide limit per platform
    if platform == "GitHub":
        usernames = [username] + generate_similar_usernames(username, limit=10)
    elif platform == "Facebook":
        usernames = [username] + generate_similar_usernames(username, limit=20)
    else:
        usernames = [username] + generate_similar_usernames(username)

    tasks = [check_site(session, platform, sites[platform].format(u), found) for u in usernames]
    await asyncio.gather(*tasks)
    return found

# Main async username finder
async def userlookup():
    Slow("=== Username Checker ===")
    username = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Enter username -> {white}").strip()
    print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Checking username and similar ones per platform...{red}")
    print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Please wait this may take a while...{red}")
    platforms = ["GitHub", "Reddit", "Facebook", "Twitter", "Instagram", "TikTok",
                 "Pinterest", "YouTube", "GitLab", "Bitbucket", "Medium", "Steam", "Twitch", "DeviantArt", "Flickr"]
    all_found = []

    async with aiohttp.ClientSession() as session:
        for platform in platforms:
            found = await check_platform_usernames(session, platform, username)
            all_found.extend(found)

    if all_found:
        print(f"\n{BEFORE}{current_time_hour()}{AFTER} {ADD} Found profiles:")
        print(tabulate(all_found, headers=["Platform", "URL"], tablefmt="grid"))
    else:
        print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} No profiles found.")

