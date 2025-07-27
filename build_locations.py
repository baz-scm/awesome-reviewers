import json
import re
from pathlib import Path
import requests
import geonamescache

gc = geonamescache.GeonamesCache()

DATA_DIR = Path('_data')
ASSETS_DIR = Path('assets/data')

LEADERBOARD_PATH = DATA_DIR / 'leaderboard.json'
LOCATIONS_OUT = ASSETS_DIR / 'locations.json'
PROFILES_OUT = ASSETS_DIR / 'profiles.json'

API_URL = 'https://api.github.com/users/'
HEADERS = {'Accept': 'application/vnd.github+json'}


def best_city(name):
    results = gc.get_cities_by_name(name)
    if not results:
        return None
    result = max(results, key=lambda d: list(d.values())[0]['population'])
    city = list(result.values())[0]
    return city['latitude'], city['longitude']


def geocode(location):
    if not location:
        return None
    # split by comma or slash
    parts = [p.strip() for p in re.split('[,;/]', location)]
    for part in parts:
        if not part:
            continue
        coords = best_city(part)
        if coords:
            return coords
        coords = best_country(part)
        if coords:
            return coords
    return None

def best_country(name):
    match = gc.get_countries_by_names().get(name)
    if match:
        code = match['iso']
        info = gc.get_countries()[code]
        capital = info['capital']
        cities = gc.get_cities_by_name(capital)
        if cities:
            city = max(cities, key=lambda d: list(d.values())[0]['population'])
            data = list(city.values())[0]
            return data['latitude'], data['longitude']
    return None


def main():
    if not LEADERBOARD_PATH.exists():
        print('leaderboard not found')
        return
    users = [u['name'] for u in json.load(open(LEADERBOARD_PATH))]
    locations = {}
    profiles = {}
    for user in users:
        print('Fetching', user)
        r = requests.get(API_URL + user, headers=HEADERS)
        if r.status_code != 200:
            print('  failed', r.status_code)
            continue
        info = r.json()
        loc = info.get('location')
        coords = geocode(loc)
        if coords:
            lat, lon = coords
            locations[user] = {'location': loc, 'lat': lat, 'lon': lon}
        elif loc:
            locations[user] = {'location': loc}
        profile = {
            'location': info.get('location'),
            'company': info.get('company'),
            'blog': info.get('blog'),
            'twitter_username': info.get('twitter_username'),
            'email': info.get('email'),
            'site_admin': info.get('site_admin'),
            'followers': info.get('followers'),
            'following': info.get('following'),
        }
        profiles[user] = {k: v for k, v in profile.items() if v is not None}
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOCATIONS_OUT, 'w', encoding='utf-8') as f:
        json.dump(locations, f, indent=2)
    print('Wrote', len(locations), 'locations to', LOCATIONS_OUT)
    with open(PROFILES_OUT, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, indent=2)
    print('Wrote', len(profiles), 'profiles to', PROFILES_OUT)


if __name__ == '__main__':
    main()
