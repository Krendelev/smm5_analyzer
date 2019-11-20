import argparse

from dotenv import load_dotenv
from requests import HTTPError

from fb import get_fb_audience
from insta import get_instagram_audience
from vk import get_vk_audience

load_dotenv()

evaluate = {
    "instagram": get_instagram_audience,
    "vk": get_vk_audience,
    "facebook": get_fb_audience,
}

output = {
    "instagram": "Top commenters: {0}\nMost frequent: {1}",
    "vk": "Most active: {0}",
    "facebook": "Most active: {0}",
}

parser = argparse.ArgumentParser(description="Quantify social media audience")
parser.add_argument(
    "media",
    choices=["instagram", "vk", "facebook"],
    help="Social media (Instagram, VK, Facebook)",
)
parser.add_argument("account", help="Account name to evaluate")
parser.add_argument("period", help="Evaluation period in days")

args = parser.parse_args()

try:
    result = evaluate[args.media](args.account, args.period)
except HTTPError as error:
    exit(error)

print(output[args.media].format(*result))
