import os

import instaloader

# user variables
PROFILE = ""
limit = 100
has_limit = True
photos_path = r"D:\Coding\RandomWebPy\photos"

# program variables
count = 0
L = instaloader.Instaloader(download_comments=False, download_videos=False, download_video_thumbnails=False,
                            save_metadata=False, download_geotags=False, post_metadata_txt_pattern="")
profile = instaloader.Profile.from_username(L.context, PROFILE)
posts = sorted(profile.get_posts(), key=lambda p: p.likes + p.comments,
               reverse=True)

for post in posts:
    os.chdir(photos_path)
    if has_limit:
        if count < limit:
            L.download_post(post, PROFILE)
            count += 1
            print(count)
    if not has_limit:
        L.download_post(post, PROFILE)
        count += 1
        print(count)
print(f"{count} images were downloaded")
