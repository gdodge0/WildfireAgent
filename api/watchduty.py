import requests

def get_current_fires():
    r = requests.get('https://api.watchduty.org/api/v1/geo_events/?is_relevant=true&zyx=5,12,5&geo_event_types=*')
    if r.status_code != 200:
        return []

    return r.json()

def get_fire_summary(geo_id):
    fire = Fire(geo_id)
    return fire.return_summary()


class Fire:
    def __init__(self, geo_id):
        self.geo_id = geo_id

    def get_reporter_information(self):
        r = requests.get(f'https://api.watchduty.org/api/v1/reports/?geo_event_id={self.geo_id}&is_moderated=true&is_active=true&limit=100&offset=0')

        if r.status_code != 200:
            return {}

        return r.json()

    def return_summary(self):
        summary = {
            "description": "An update to date summary of wildfire information from Watch Duty",
            "messages": []
        }

        data = self.get_reporter_information()

        if not data:
            summary["messages"].append({
                "no current data"
            })

        for result in data["results"]:
            summary["messages"].append({
                "author": result["user_created"]["display_name"],
                "timestamp": result["date_created"],
                "message": result["message"]
            })

        return summary