import glob
import os
import random
import time
import toml
import praw
import requests
import win32api
import win32con
import win32gui

# for program
photo_count = 0
rename_count = 1
folder_path = r"D:\Coding\RandomWebPy\wallpapers"
bad_sites = ["c1.staticflickr.com", "wakpaper.com", "www.prairiemoon.com", "www.hdwallpapersinn.com",
             "hdwallphotos.com"]
wallpaper_count = 0

# user inputted
# number of photos to get from reddit initally and in subsequent refills, acceptable subreddits to scrape
num_images = 6
subreddits = ["EarthPorn", "ModernArt", "CityPorn", "SkyPorn", "WholesomeMemes"]
# enables if users wants to scrape reddit initially, rename the photos scraped and set them as wallpaper
get_from_reddit = True
to_rename = False
set_wallpaper = False
# enables if user wants to cycle through wallpapers
change_wallpaper = False
# enable if user wants to delete wallpaper after use and/or get from reddit when no photos are present
refill = True
delete_wallpaper = True
# delay if user wants to change wallpaper(in seconds)
delay = 1

# reddit variables
login_file = toml.load("login.toml")
reddit = praw.Reddit(client_id=login_file.get("reddit_id"), client_secret=login_file.get("reddit_secret"),
                user_agent=login_file.get("reddit_user_agent"))
selected_subreddit_num = random.randint(0, len(subreddits) - 1)
selected_subreddit = subreddits[selected_subreddit_num]
subreddit = reddit.subreddit(selected_subreddit)
posts = subreddit.hot(limit=min(num_images * 3, 1000))


# reddit scraper using random subreddit from pre-designated list. downloads preset amount of photos if variable is
# set to true
def reddit_download(source, path, badsites, counter, limit):
    for post in source:
        if not post.is_self:
            if counter < limit:
                try:
                    url = post.url
                    file_name = url.split("/")
                    req = requests.get(url)
                    for ele in file_name:
                        potential_extension = ele.split(".")
                        if "jpg" in potential_extension and file_name[2] not in badsites:
                            file_name = file_name[-1]
                            os.chdir(path)
                            with open(file_name, "wb") as f:
                                f.write(req.content)
                                counter += 1
                                print(f"{counter} images downloaded")

                except OSError:
                    print("Link post")
        elif post.is_self:
            print("Text Post")


if get_from_reddit:
    print(subreddit)
    reddit_download(source=posts, path=folder_path, badsites=bad_sites, counter=photo_count, limit=num_images)


# rename all images in folder if variable is set to true
def rename(path, counter):
    filelist = glob.glob(f'{path}\*.jpg')
    for oldname in filelist:
        try:
            if os.path.isfile(oldname):
                basepath = os.path.split(oldname)[0]
                newname = os.path.join(basepath, "{}.jpg".format(str(counter)))
                counter += 1
                print("Renaming {} to {}".format(oldname, newname))
                os.rename(oldname, newname)
        except FileExistsError:
            print(f"{counter} already exists")


if to_rename:
    rename(path=folder_path, counter=rename_count)


# set random file as wallpaper if variable is set true
def wallpaper(path):
    global wallpaper_count
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, 1 + 2)
    print(f"{wallpaper_count + 1} Wallpaper Set")


def photo_index(path, refill_var):
    global posts, folder_path, bad_sites, num_images
    file_num = len(os.listdir(path))
    refill_counter = 0
    if file_num == 0:
        print("No images found")
        if refill_var:
            selected_subreddit_num = random.randint(0, len(subreddits) - 1)
            selected_subreddit = subreddits[selected_subreddit_num]
            subreddit = reddit.subreddit(selected_subreddit)
            print(subreddit)
            posts = subreddit.hot(limit=num_images * 2)
            reddit_download(source=posts, path=folder_path, badsites=bad_sites, counter=refill_counter,
                            limit=num_images)
            if to_rename:
                rename_count2 = 1
                rename(path=folder_path, counter=rename_count2)
            if num_images == 1:
                return 0
            else:
                file_num = len(os.listdir(path))
                return random.randint(1, file_num - 1)
        elif not refill_var:
            exit()
    elif file_num == 1:
        return 0
    else:
        return random.randint(1, file_num - 1)


def to_delete(path, delete):
    if delete:
        os.remove(path)


if set_wallpaper:
    if change_wallpaper:
        while True:
            number = photo_index(folder_path, refill)
            photo_path = folder_path + chr(92) + os.listdir(folder_path)[number]
            wallpaper(photo_path)
            to_delete(photo_path, delete_wallpaper)
            wallpaper_count += 1
            time.sleep(delay)
    elif not change_wallpaper:
        number = photo_index(folder_path, refill)
        photo_path = folder_path + chr(92) + os.listdir(folder_path)[number]
        wallpaper(photo_path)
        to_delete(photo_path, delete_wallpaper)
