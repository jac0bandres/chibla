import instaloader
from time import sleep
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

L = instaloader.Instaloader()
target = os.getenv('INSTA_TARGET')
profile_json_schema = {
    "username": "Lorem Ipsum",
    "userid": "Lorem Ipsum",
    "biography": "Lorem Ipsum",
    "external_url": "Lorem Ipsum",
    "followees": 0,
    "followers": 0,
    "updated": "00/00/0000 00:00:00",
    "last story": "00/00/0000 00:00:00",
    "log": "",
    "read": None
}

def check_data_dir():
    if not os.path.exists(f'{target}-data'):
        os.makedirs(f'{target}-data')
        os.makedirs(f'{target}-data/stories')
        with open(f'{target}-data/followers.txt', 'w') as f:
            f.write('')
        with open(f'{target}-data/followees.txt', 'w') as f:
            f.write('')
        with open(f'{target}-data/log.txt', 'w') as f:
            f.write('')
        with open(f'{target}-data/profile.json', 'w') as f:
            f.write(json.dumps(profile_json_schema, indent=4))
        print("[+] Insta Data directory created...")
        with open(f'{target}-data/follower-activity', 'w') as f:
            f.write('')

# bot insta login
def login():
    check_data_dir()
    try:
        L.test_login()
    except BaseException as e:
            print("[!] Error: ", e, "\n[!] Loading session from file...")
            try:
                L.load_session_from_file(os.getenv('INSTA_USER'))
            except BaseException as e:
                print("[!] Error: ", e, "\n[!] Logging in... again.")
                L.login(os.getenv('INSTA_USER'), os.getenv('INSTA_PASSWD'))
                L.save_session_to_file()

def log(content):
    log_content = f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\t\t{content}\n'
    with open(f'{target}-data/log.txt', 'a') as f:
        f.write(log_content)

    data = json.loads(open(f'{target}-data/profile.json').read())
    activity_log = json.loads(open(f'{target}-data/log.json').read())

    activity_log['log'] = activity_log['log'] + log_content
    activity_log['hourly log'] = activity_log['hourly log'] + log_content
    activity_log['read'] = False

    with open(f'{target}-data/profile.json', 'w') as f:
        f.write(json.dumps(data, indent=4))

    with open(f'{target}-data/log.json', 'w') as f:
        f.write(json.dumps(activity_log, indent=4))

# enumerate followers function
def enum_followers(followers):
    print('[+] Enumerating Insta followers...')
    unfollowed = []
    followed = []
    
    with open(f'{target}-data/new_followers.txt', 'w') as f:
        for follower in followers:
            f.write(follower.username + '\n') 

    with open(f'{target}-data/followers.txt', 'r') as f:
        old_followers = f.readlines() 

        with open(f'{target}-data/new_followers.txt', 'r') as f:
            new_followers = f.readlines()

            for old_follower in old_followers:
                if old_follower not in new_followers:
                    unfollowed.append(old_follower.strip())
            
            for new_follower in new_followers:
                if new_follower not in old_followers:
                    followed.append(new_follower.strip())

    os.remove(f'{target}-data/followers.txt')
    os.rename(f'{target}-data/new_followers.txt', f'{target}-data/followers.txt')

    if len(unfollowed) > 0:
        log(f"[+] Unfollowing {target}:  {unfollowed}")

    if len(followed) > 0:
        log(f"[+] Following {target}:  {followed}")

# enumerate followees function
def enum_followees(followees):
    print('[+] Enumerating Insta followees...')
    unfollowed = []
    followed = []
    
    with open(f'{target}-data/new_followees.txt', 'w') as f:
        for followee in followees:
            f.write(followee.username + '\n') 

    with open(f'{target}-data/followees.txt', 'r') as f:
        old_followees = f.readlines() 

        with open(f'{target}-data/new_followees.txt', 'r') as f:
            new_followees = f.readlines()

            for old_followee in old_followees:
                if old_followee not in new_followees:
                    unfollowed.append(old_followee.strip())
            
            for new_followee in new_followees:
                if new_followee not in old_followees:
                    followed.append(new_followee.strip())

    os.remove(f'{target}-data/followees.txt')
    os.rename(f'{target}-data/new_followees.txt', f'{target}-data/followees.txt')

    if len(unfollowed) > 0:
        log(f"[+] Unfollowed by {target}:  {unfollowed}")

    if len(followed) > 0:
        log(f"[+] Followed by {target}:  {followed}")

# update profile json
def update_profile(profile):
    if not os.path.exists(f'{target}-data/profile.json'):
        with open(f'{target}-data/profile.json', 'w') as f:
            f.write(json.dumps(profile_json_schema, indent=4))

    saved_profile = json.load(open(f'{target}-data/profile.json'))
    saved_profile['username'] = profile.username
    saved_profile['userid'] = profile.userid
    saved_profile['biography'] = profile.biography
    saved_profile['external_url'] = profile.external_url
    saved_profile['followees'] = profile.followees
    saved_profile['followers'] = profile.followers
    saved_profile['updated'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with open(f'{target}-data/profile.json', 'w') as f:
        f.write(json.dumps(saved_profile, indent=4))

# ping follows by comparing saved jsonf {target}-data with freshf {target}-data
def ping_follows(followers, followees):
    update = False
    profile = instaloader.Profile.from_username(L.context, target)

    if profile.followers != int(followers):
        log(f"[+] {target} follower activity: {profile.followers - followers}.")
        enum_followers(profile.get_followers())
        update = True

    if profile.followees != int(followees):
        log(f"[+] {target} followee activity: {profile.followees - followees}.")
        enum_followees(profile.get_followees())
        update = True
        
    if update:
        update_profile(profile) 

# ping posts by comparing saved post with freshf {target}-data
def ping_story():
    # user_id = json.load(open(f'{target}-data/profile.json'))['userid']
    profile = instaloader.Profile.from_username(L.context, target)
    saved_profile = json.loads(open(f'{target}-data/profile.json').read())
    stories = L.get_stories([profile.userid])

    if not stories:
        return

    
    for story in L.get_stories(userids=[profile.userid]):
        if story.latest_media_local > datetime.fromisoformat(saved_profile['last story']):
            for item in story.get_items():
                L.download_storyitem(item, f'stories')
                saved_profile['last story'] = str(story.latest_media_local)
                log(f"[+] New story from {target}: {story.latest_media_local}.")

        else:
            continue

    with open(f'{target}-data/profile.json', 'w') as f:
        f.write(json.dumps(saved_profile, indent=4))



def ping_profile():
    saved_profile = json.load(open(f'{target}-data/profile.json'))
    ping_follows(saved_profile['followers'], saved_profile['followees'])

# send imagef {target}-data into discord
def send_img(image, message):
    pass

# run instagram async
def run():
    login()
    while True:
        try:
            # ping_profile()
            # sleep(5)
            ping_story()
            sleep(5)
        except instaloader.exceptions.LoginRequiredException as e:
            print("[!] Error: ", e, "\n[!] Logging in... again.")
            login()
        except instaloader.exceptions.BadCredentialsException as e:
            print("[!] Error: ", e, "\n[!] Logging in... again.")
            login()
        except instaloader.exceptions.ConnectionException as e:
            print("[!] Error: ", e, "\n[!] Retrying...")
            login()