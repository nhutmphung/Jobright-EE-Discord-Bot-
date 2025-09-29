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


#take in the dict list from parse_jobs, and take the dict and filter out for the TITLE 
def filter_jobs(jobs):
    filtered = []
    for i in jobs:
        if "Electrical" in i['title'] or "Mechatronic" in i['title'] or "Power" in i['title']:
            filteredURL = i['url']
            print( "URL: ", i['url'])
            filtered.append(i['url'])
    
    return filtered

#create unique id from the filtered EE jobs
def job_id(string):
    url_bytes = string.encode('utf-8')
    job_id = hashlib.sha256(url_bytes).hexdigest()
    return job_id

#sends the filtered URL to the function to append in the list of filteredJob. After, have the job_id function pull from the list?
def filteredJobsJSON(string):
    try:
        with open(filteredFileName, "r") as file:
            data = json.load(file)

    except(FileNotFoundError, json.JSONDecodeError):
        data = []
    #if the string is already in there, just return and do nothing 
    if string in data:
        return string
    else:
        data.append(string)
        with open("filteredJob.json", "w") as file:
            json.dump(data, file, indent = 4 )

def filteredJob_ids(_):
    try:
        with open(filteredFileName, "r") as file:
            data = json.load(file)   # list of job URLs
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    try:
        with open(postedFileName, "r") as file2: 
            data2 = json.load(file2)   # list of job IDs
    except (FileNotFoundError, json.JSONDecodeError):
        data2 = []

    for url in data:
        url_bytes = url.encode("utf-8")
        job_id = hashlib.sha256(url_bytes).hexdigest()
        if job_id not in data2:   # avoid duplicates
            data2.append(job_id)

    # write once after loop
    with open(postedFileName, "w") as file2:
        json.dump(data2, file2, indent=4)



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


#TODO fix the filteredJob_ids to make it properly make the ids, was too tired to finish zzzz
#testing to see if electrical position gets printed             
def main():
    job = parse_jobs(raw_data)
    #pprint.pprint(job[:5])
    filter_jobs(job[:500])
    filteredURL = filter_jobs(job[:500])

    for url in filteredURL:
        filteredJobsJSON(url)
    filteredJob_ids(filteredURL)
   # filteredJob = filter_jobs(job)


main()
