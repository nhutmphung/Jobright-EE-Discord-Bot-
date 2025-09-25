import hashlib
from fetch_jobs import fetch_jobs
import re
import json

#data setup
raw_data = fetch_jobs()

filename = "posted_jobs.json"

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


#*TODO: to filter the job, take from the title and look for "ELECTRICAL" in the job title and pull any jobsfrom it

#take in the dict list from parse_jobs, and take the dict and filter out for the TITLE 
def filter_jobs(jobs):
    for i in jobs:
        if "Electrical" in i['title']:
            filteredURL = i['url']
            print("Job position: ", i['title'], "| URL: ", i['url'])
            return filteredURL
        #if nothing matched
        return None

#create unique id from the filtered EE jobs
def job_id(string):
    url_bytes = string.encode('utf-8')
    job_id = hashlib.sha256(url_bytes).hexdigest()
    return job_id


#sends job_id posted to the json file
def posted_jobs(string):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        data = [ ]

    if string in data:
        return string
    else:
        data.append(string)

        with open("posted_jobs.json", "w") as file:
            json.dump(data, file, indent = 4)


            
def main():
    job = parse_jobs(raw_data)
    filteredJob = filter_jobs(job)

    if filteredJob is not None:
        testID = job_id(filteredJob)
        posted_jobs(testID)
        print("job-id:", testID)
    
    else:
        print("No EE jobs right now!")

main()
