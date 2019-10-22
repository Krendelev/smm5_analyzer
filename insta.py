import json
import os
from collections import Counter
from datetime import datetime, timedelta
from itertools import chain

import instabot
from dotenv import load_dotenv


ACCOUNT = "cocacolarus"
DAYS = 90

load_dotenv()

bot = instabot.Bot()
bot.login(username=os.environ["INSTA_LOGIN"], password=os.environ["INSTA_PASS"])

owner_id = bot.get_user_id_from_username(ACCOUNT)
owner_media = bot.get_total_user_medias(owner_id)
comments = [bot.get_media_comments_all(id_) for id_ in owner_media]

boundary = (datetime.today() - timedelta(days=DAYS)).timestamp()
commenters_by_post = [
    [
        c["user_id"]
        for c in comment
        if c["created_at"] > boundary and c["user_id"] != int(owner_id)
    ]
    for comment in comments
    if comment
]
comments_leaved = Counter(chain.from_iterable(commenters_by_post))
posts_commented = Counter()
for commenters in commenters_by_post:
    posts_commented.update(set(commenters))

print(comments_leaved.most_common(5), posts_commented.most_common(5), sep="\n")
