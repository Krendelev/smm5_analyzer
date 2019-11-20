import itertools
import os
from collections import Counter

import requests
from dotenv import load_dotenv

from utils import compute_boundary, timestamp_from_time


def get_group_id(payload, user_id):
    url = f"https://graph.facebook.com/v5.0/{user_id}/groups"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    content = response.json()
    return content["data"][0]["id"]


def fetch_records(url, payload):
    while url:
        response = requests.get(url, params=payload)
        response.raise_for_status()
        content = response.json()
        yield from content["data"]
        url = content.get("paging", {}).get("next", None)


def get_publication_ids(payload, group_id):
    url = f"https://graph.facebook.com/v5.0/{group_id}/feed"
    return [rec["id"] for rec in fetch_records(url, payload)]


def get_commenter_ids(payload, publication_id, days):
    url = f"https://graph.facebook.com/v5.0/{publication_id}/comments"
    payload = {**payload, "filter": "toplevel"}
    boundary = compute_boundary(days)
    return (
        record["from"]["id"]
        for record in fetch_records(url, payload)
        if timestamp_from_time(record["created_time"]) > boundary
    )


def get_reactions(payload, publication_id):
    url = f"https://graph.facebook.com/v5.0/{publication_id}/reactions"
    return ((rec["id"], rec["type"]) for rec in fetch_records(url, payload))


def get_fb_audience(user_id, days):
    payload = {"access_token": os.environ["FB_MARKER"]}

    group_id = get_group_id(payload, user_id)
    publication_ids = get_publication_ids(payload, group_id)
    commenter_ids = (
        get_commenter_ids(payload, pub_id, days) for pub_id in publication_ids
    )
    commenters = set(itertools.chain.from_iterable(commenter_ids))

    reactions = (get_reactions(payload, pub_id) for pub_id in publication_ids)
    reactions_count = Counter(itertools.chain.from_iterable(reactions))

    result = {}
    for commenter in commenters:
        result[commenter] = {
            reaction: count
            for (user_id, reaction), count in reactions_count.items()
            if commenter == user_id
        }
    result.pop(user_id, None)

    return (result,)


if __name__ == "__main__":
    load_dotenv()
    print(get_fb_audience(os.environ["FB_USER_ID"], os.environ["FB_PERIOD"]))
