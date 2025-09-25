import hashlib
from fetch_jobs import fetch_jobs
import re
import json
import pprint

#data setup
raw_data = fetch_jobs()

postedFileName = "posted_jobs.json"
filteredFileName = "filteredJob.json"

#takes the mark down text as a string and parses the text
def parse_jobs(string):
    jobs = []
    lines = string.split("\n")

    for line in lines:
        # Only process lines that look like table rows
        if line.startswith("| **["):
            # Regex explanation:
            # \|\s\*\*\[(.*?)\]\((.*?)\)\*\*  => matches first cell: company name + link
            # \|\s\*\*\[(.*?)\]\((.*?)\)\*\*  => matches second cell: position + link
            # \|\s(.*?)\s\|  => matches third cell: location
            match = re.match(
                r"\|\s\*\*\[(.*?)\]\((.*?)\)\*\*\s\|\s\*\*\[(.*?)\]\((.*?)\)\*\*\s\|\s(.*?)\s\|",
                line
            )
            if match:
                company_name, company_url, position, position_url, location = match.groups()
                jobs.append(
                    {
                    "title": position,
                    "company": company_name,
                    "location": location,
                    "url": position_url  # usually the position link is what we want to apply to
                }
                )

    return jobs


#*TODO: take the filtered jobs and post it into a array/list to pull from and have the posted_jobs function pull from that 

#take in the dict list from parse_jobs, and take the dict and filter out for the TITLE 
def filter_jobs(jobs):
    for i in jobs:
        filtered = []
        if "Electrical" in i['title'] or "Mechatronic" in i['title'] or "Power" in i['title']:
            filteredURL = i['url']
            print("Job position: ", i['title'], "| URL: ", i['url'])
            filtered.append(i['url'])
        else: 
            print("No EE job right now")

#create unique id from the filtered EE jobs
def job_id(string):
    url_bytes = string.encode('utf-8')
    job_id = hashlib.sha256(url_bytes).hexdigest()
    return job_id


#sends job_id posted to the json file
def posted_jobs(string):
    try:
        with open(postedFileName, "r") as file:
            data = json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        data = [ ]

    if string in data:
        return string
    else:
        data.append(string)

        with open("posted_jobs.json", "w") as file:
            json.dump(data, file, indent = 4)


#testing to see if electrical position gets printed             
def main():
    job = parse_jobs(raw_data)
    job = job[:20]
    pprint.pprint(job[:20])
    filter_jobs(job)
   # filteredJob = filter_jobs(job)


main()
