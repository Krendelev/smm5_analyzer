import os
from collections import Counter
from itertools import chain

import instabot
from dotenv import load_dotenv

from utils import compute_boundary


def get_instagram_audience(user_name, days):
    bot = instabot.Bot()
    bot.login(username=os.environ["INSTA_LOGIN"], password=os.environ["INSTA_PASS"])

    user_id = int(bot.get_user_id_from_username(user_name))
    user_media = bot.get_total_user_medias(user_id)
    comments_by_post = (bot.get_media_comments_all(id_) for id_ in user_media)

    filtered_comments_by_post = filter(None, comments_by_post)
    boundary = compute_boundary(days)
    commenters_by_post = [
        [comment["user_id"] for comment in comments if comment["created_at"] > boundary]
        for comments in filtered_comments_by_post
    ]

    comments_leaved = Counter(chain.from_iterable(commenters_by_post))
    comments_leaved.pop(user_id, None)

    posts_commented = Counter()
    for commenters in commenters_by_post:
        posts_commented.update(set(commenters))
    posts_commented.pop(user_id, None)

    return comments_leaved.most_common(), posts_commented.most_common()


if __name__ == "__main__":
    load_dotenv()
    print(
        get_instagram_audience(os.environ["INSTA_ACCOUNT"], os.environ["INSTA_PERIOD"])
    )
