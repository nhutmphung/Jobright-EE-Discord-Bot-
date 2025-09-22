#import the raw data from github and make it legible/readable 
import requests


def fetch_jobs():
    url = "https://raw.githubusercontent.com/jobright-ai/2025-Engineer-Internship/refs/heads/master/README.md"
    response = requests.get(url)

    if response.status_code == 200:
        #raw markdown text processed as a string
        raw_data = response.text 
        return raw_data
    else:
        print("Failed to get raw data")
        return None
    