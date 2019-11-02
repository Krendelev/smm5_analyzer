import argparse

from dotenv import load_dotenv

from insta import get_instagram_audience
from vk import get_vk_audience
from fb import get_fb_audience

load_dotenv()

evaluate = {
    "instagram": get_instagram_audience,
    "vk": get_vk_audience,
    "facebook": get_fb_audience,
}

parser = argparse.ArgumentParser(description="Quantify social media audience")
parser.add_argument("media", help="Social media (Instagram, VK, Facebook)")
parser.add_argument("account", help="Account name to evaluate")
parser.add_argument("period", help="Evaluation period in days")

media = parser.parse_args().media
account = parser.parse_args().account
period = parser.parse_args().period

print(evaluate[media](account, period))
