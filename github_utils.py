import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

PROFILE_FIELDS = [
    'location',
    'company',
    'blog',
    'twitter_username',
    'email',
    'site_admin',
    'followers',
    'following',
]

def fetch_profile(user, token=None):
    """Fetch GitHub profile data for a user and return selected fields."""
    url = f'https://api.github.com/users/{user}'
    headers = {'Accept': 'application/vnd.github+json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=10) as resp:
            data = json.load(resp)
    except (HTTPError, URLError, OSError) as exc:
        print(f'Failed to fetch profile for {user}: {exc}')
        return None
    return {k: data.get(k) for k in PROFILE_FIELDS if data.get(k) is not None}
