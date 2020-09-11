import os
import toml
import praw
import requests

# for program
photos_path = r"D:\Coding\RandomWebPy\photos"
count = 0
bad_sites = ["c1.staticflickr.com", "wakpaper.com", "www.prairiemoon.com", "www.hdwallpapersinn.com",
             "hdwallphotos.com"]
good_sites = ["i.reddit.it", "i.imgur.com"]

# user inputted
limit = 5
topic = "ModernArt"

size_limit = False
max_size = 10

# reddit variables
login_file = toml.load("login.toml")
r = praw.Reddit(client_id=login_file.get("reddit_id"), client_secret=login_file.get("reddit_secret"),
                user_agent=login_file.get("reddit_user_agent"))
subreddit = r.subreddit(topic)
grab_limit = min(limit * 2, 1000)
posts = subreddit.top(limit=grab_limit)

for post in posts:
    if count < limit:
        if not post.is_self:
            try:
                url = post.url
                file_name = url.split("/")
                r = requests.get(url)
                for ele in file_name:
                    potential_extension = ele.split(".")
                    if "jpg" in potential_extension and file_name[2] not in bad_sites:
                        file_name = file_name[-1]
                        os.chdir(photos_path)
                        if size_limit:
                            if r.content.__sizeof__() < max_size * 1000000:
                                with open(file_name, "wb") as f:
                                    f.write(r.content)
                                    count += 1
                                    print(f"{count} Downloaded")
                        elif not size_limit:
                            with open(file_name, "wb") as f:
                                f.write(r.content)
                                count += 1
                                print(f"{count} Downloaded")
            except OSError:
                print("Link post")
        elif post.is_self:
            print("Text Post")
    elif count < limit:
        print("End")
        print(f"{count} images were downloaded")
        exit()
print(f"{count} images were downloaded")
