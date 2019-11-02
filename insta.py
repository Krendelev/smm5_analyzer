import os
from collections import Counter
from datetime import datetime, timedelta
from itertools import chain

import instabot
from dotenv import load_dotenv

import utils

ACCOUNT = "cocacolarus"
DAYS = 90


def get_instagram_audience(user_name, days):
    bot = instabot.Bot()
    bot.login(username=os.environ["INSTA_LOGIN"], password=os.environ["INSTA_PASS"])

    user_id = int(bot.get_user_id_from_username(user_name))
    user_media = bot.get_total_user_medias(user_id)
    comments = [bot.get_media_comments_all(id_) for id_ in user_media]

    boundary = utils.compute_boundary(days)
    commenters_by_post = [
        [c["user_id"] for c in comment if c["created_at"] > boundary]
        for comment in comments
        if comment
    ]
    comments_leaved = Counter(chain.from_iterable(commenters_by_post))
    comments_leaved.pop(user_id)

    posts_commented = Counter()
    for commenters in commenters_by_post:
        posts_commented.update(set(commenters))
    posts_commented.pop(user_id)

    return f"""Top commenters: {comments_leaved.most_common()}\nMost frequent: {posts_commented.most_common()}"""


if __name__ == "__main__":
    load_dotenv()
    print(get_instagram_audience(ACCOUNT, DAYS))
