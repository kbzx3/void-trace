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
module_display_name = "Username Lookup"
description = '''
Description:
An asynchronous OSINT scanner leveraging aiohttp to concurrently probe 18 social media 
URL patterns. It utilizes a mutation algorithm to generate and test similar-looking 
usernames to identify potential profile matches.

Usage:
1. Type the username you want to find.
2. Wait as the tool checks dozens of sites (like Reddit, TikTok, and Steam) at once.
3. It will list direct links to any profiles it finds registered with that name.
'''
def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def Slow(text, delay=0.03):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def generate_similar_usernames(username, limit=None):
    username = username.lower()
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789-_.'
    similar = set()
    base_tweaks = [
        f"{username}2",
        f"{username}_",
        f"{username}wastaken"
        
    ]
    if 'e' in username: 
        base_tweaks.append(f"{username.replace('e','3')}")
    if len(username) > 2:
        base_tweaks.append(f"{username[:2]}_{username[2:]}")
    if 'o' in username:
        base_tweaks.append(f"{username.replace('o','0')}")
    if '0' in username:
        base_tweaks.append(f"{username.replace('0','o')}")
    similar.update(base_tweaks)

    # Character substitutions, insertions, deletions
    for i in range(len(username)):
        for c in alphabet:
            if username[i] != c:
                similar.add(username[:i] + c + username[i+1:])
    for i in range(len(username) + 1):
        for c in alphabet:
            similar.add(username[:i] + c + username[i:])
    for i in range(len(username)):
        similar.add(username[:i] + username[i+1:])

    similar_list = list(similar)
    result = base_tweaks + [u for u in similar_list if u not in base_tweaks]
    
    if limit:
        return result[:limit]
    return result



BODY_ERROR_MARKERS = {
    "Steam": ["<title>Steam Community :: Error</title>", "The specified profile could not be found"],
}

async def check_site(session, site, url, username, found):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    try:
        need_body = site in BODY_ERROR_MARKERS
        async with session.get(url, headers=headers, timeout=10, allow_redirects=True, ssl=False) as resp:
            if resp.status == 200:
                if need_body:
                    body = await resp.text()
                    for marker in BODY_ERROR_MARKERS[site]:
                        if marker.lower() in body.lower():
                            return 
                found.append((site, url))
                print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} Username found on {site}: {white}{url}{red}")
            elif resp.status == 404:
                pass 
            elif resp.status == 429:
                print(f"{BEFORE}{current_time_hour()}{AFTER} [!] Rate limit hit for {site}, skipping {url}")
    except asyncio.TimeoutError:
        pass
    except Exception:
        pass

# Check usernames for a platform
async def check_platform_usernames(session, platform, username, limit=None):

    sites = {
        "GitHub": "https://github.com/{}",
        "Reddit": "https://old.reddit.com/user/{}",
        "Instagram": "https://www.instagram.com/{}/",
        "TikTok": "https://www.tiktok.com/@{}",
        "YouTube": "https://www.youtube.com/{}",
        "Twitch": "https://www.twitch.tv/{}",
        "Pinterest": "https://www.pinterest.com/{}/",
        "Snapchat": "https://www.snapchat.com/add/{}",
        "Spotify": "https://open.spotify.com/user/{}",
        "GitLab": "https://gitlab.com/{}",
        "Steam": "https://steamcommunity.com/id/{}",
        "DeviantArt": "https://www.deviantart.com/{}",
        "Chess.com": "https://www.chess.com/member/{}",
        "Roblox": "https://www.roblox.com/user.aspx?username={}",
        "Keybase": "https://keybase.io/{}",
        "Patreon": "https://www.patreon.com/{}",
        "Linktree": "https://linktr.ee/{}",
        "AboutMe": "https://about.me/{}",
    }
    found = []


    usernames = [username] + generate_similar_usernames(username,limit= 20)

    tasks = [check_site(session, platform, sites[platform].format(u), u, found) for u in usernames]
    await asyncio.gather(*tasks)
    return found

async def userlookup():
    Slow("=== Username Checker ===")
    username = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Enter username -> {white}").strip()
    print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Checking username and similar ones per platform...{red}")
    print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Please wait this may take a while...{red}")
    platforms = ["GitHub", "Reddit", "Instagram", "TikTok",
                 "YouTube", "Twitch", "Pinterest", "Snapchat", "Spotify",
                 "GitLab", "Steam", "DeviantArt", "Chess.com",
                 "Roblox", "Keybase", "Patreon", "Linktree", "AboutMe"]
    all_found = []

    async with aiohttp.ClientSession() as session:
        for platform in platforms:
            found = await check_platform_usernames(session, platform, username)
            all_found.extend(found)

    if all_found:
        print(f"\n{BEFORE}{current_time_hour()}{AFTER} {ADD} Found profiles:")
        for platform, url in all_found:
            print(f"  {platform}: {url}")
    else:
        print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} No profiles found.")

