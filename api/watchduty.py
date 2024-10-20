import requests

def get_current_fires():
    r = requests.get('https://api.watchduty.org/api/v1/geo_events/?is_relevant=true&zyx=5,12,5&geo_event_types=wildfire')
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

    def get_geo_data(self):
        r = requests.get(f'https://cache.watchduty.org/api/v1/geo_events/{self.geo_id}')
        if r.status_code != 200:
            return {}

        return r.json()

    def return_summary(self):
        summary = {
            "description": "An update to date summary of wildfire information from Watch Duty. This is context for your chat session.",
            "messages": {
                "summary": [],
                "geo_events": []
            }
        }

        data = self.get_reporter_information()
        geo_data = self.get_geo_data()

        if not data:
            summary["messages"]["summary"].append({
                "no current data"
            })
        else:
            for result in data["results"]:
                try:
                    author = result["user_created"]["display_name"]
                except TypeError:
                    author = "staff"
                summary["messages"]["summary"].append({
                    "author": author,
                    "timestamp": result["date_created"],
                    "message": result["message"]
                })

        if not geo_data:
            summary["messages"]["geo_events"].append({
                "no current data"
            })
        else:
            summary["messages"]["geo_events"].append(geo_data)

        return summary