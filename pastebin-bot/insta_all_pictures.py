from instaloader import Instaloader,Profile
import threading
import shutil
import os
import time
import random
from dotenv import load_dotenv

load_dotenv()
status = ""
isLoggedIn = False

def get_status():
    return status

profile_instance = Instaloader()

def login():
    global profile_instance
    global isLoggedIn
    
    name = os.getenv("username")
    passw = os.getenv("password")
    profile_instance.login(name,passw)
    isLoggedIn = True
    

def fetch_posts(user):

    global status
    status = ""
    

    try:
        prof = Profile.from_username(profile_instance.context, user)
        print(prof)
        posts = prof.get_posts()
        if(posts.count > 100):
            status = "limit_exceeded"
            return
    except:
        raise FileNotFoundError
    

    for post in posts:
        try:
            time.sleep(random.randint(0,5)/10.0)
            task = threading.Thread(target=profile_instance.download_post, args=(post,user,))
            task.start()
        except:
            print("Skipping due to status code 401")


def profile_delete(username):
    shutil.rmtree(f"{username}")
