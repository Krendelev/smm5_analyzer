import os
import itertools

import requests
from dotenv import load_dotenv

from utils import compute_boundary

ACCOUNT = "cocacola"
DAYS = 14


def check_vk_response(response):
    if "error" in response:
        raise requests.HTTPError(response["error"]["error_msg"])
    return None


def get_group_id(payload, name):
    url = "https://api.vk.com/method/groups.getById"
    response = requests.get(url, params={**payload, "group_id": name}).json()
    check_vk_response(response)
    return response["response"][0]["id"]


def fetch_records(url, payload):
    MAX_COUNT = 100
    for req in itertools.count():
        params = {**payload, "count": MAX_COUNT, "offset": req * MAX_COUNT}
        response = requests.get(url, params=params).json()
        check_vk_response(response)
        records = response.get("response", {}).get("items", None)
        if not records:
            break
        yield from records


def get_post_ids(payload):
    url = "https://api.vk.com/method/wall.get"
    payload = {**payload, "filter": "owner"}
    return [record["id"] for record in fetch_records(url, payload)]


def get_commenter_ids(payload, post_id, days):
    url = "https://api.vk.com/method/wall.getComments"
    payload = {**payload, "post_id": post_id}
    boundary = compute_boundary(days)
    return (
        record["from_id"]
        for record in fetch_records(url, payload)
        if not record.get("deleted", False)
        and record["from_id"] > 0
        and record["date"] > boundary
    )


def get_liker_ids(payload, post_id):
    url = "https://api.vk.com/method/likes.getList"
    payload = {**payload, "type": "post", "item_id": post_id}
    return (record for record in fetch_records(url, payload))


def get_vk_audience(user_name, days):
    payload = {"access_token": os.environ["VK_ACCESS_TOKEN"], "v": 5.102}
    try:
        group_id = -int(get_group_id(payload, user_name))
    except requests.HTTPError as error:
        exit(error)

    payload.update({"owner_id": group_id})
    try:
        post_ids = get_post_ids(payload)
        commenter_ids = (get_commenter_ids(payload, id_, days) for id_ in post_ids)
        liker_ids = (get_liker_ids(payload, id_) for id_ in post_ids)
    except requests.HTTPError as error:
        exit(error)

    commenters = set(itertools.chain.from_iterable(commenter_ids))
    likers = set(itertools.chain.from_iterable(liker_ids))

    return f"Most active: {commenters & likers}"


if __name__ == "__main__":
    load_dotenv()
    print(get_vk_audience(ACCOUNT, DAYS))
