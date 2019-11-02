# Social media analyzer

Analyze audience of [Instagram](https://instagram.com/), [VKontakte](https://vk.com) and [Facebook](https://facebook.com) accounts.

## How to install

Python3 should be already installed.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Put credentials from your Instagram, VK and FB accounts into the `.env` file in the working directory like this:

```bash
INSTA_LOGIN=replace_with_login
INSTA_PASS=replace_with_password
VK_ACCESS_TOKEN=replace_with_token
FB_MARKER=replace_with_marker
```

Run `main.py` with the following arguments: social media name, user name (user id for FB) and time period in days to evaluate.

```bash
$ python main.py instagram cocacolarus 90
Top commenters: {"123974769": 25, "123974241": 5, "179539894": 40, ...}
Most frequent: {"123974769": 5, "123974241": 1, "179539894": 3, ...}
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
