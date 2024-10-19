import requests

def get_current_fires():
    r = requests.get('https://api.watchduty.org/api/v1/geo_events/?is_relevant=true&zyx=5,12,5&geo_event_types=*')
    if r.status_code != 200:
        return []

    return r.json()

def get_specific_information(geo_id: int):
    r = requests.get(f'https://api.watchduty.org/api/v1/reports/?geo_event_id={geo_id}&is_moderated=true&is_active=true&has_lat_lng=true')

    if r.status_code != 200:
        return []

    return r.json()

def get_reporter_information(geo_id: int):
    r = requests.get(f'https://api.watchduty.org/api/v1/reports/?geo_event_id={geo_id}&is_moderated=true&is_active=true&limit=100&offset=0')

    if r.status_code != 200:
        return []

    return r.json()