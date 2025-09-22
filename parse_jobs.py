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

def job_id(string):
    url_bytes = string['url'].encode('utf-8')
    job_id = hashlib.sha256(url_bytes).hexdigest()
    return job_id

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
    job = {"url": "https://jobright.ai/jobs/info/68cfdc3fdbd9fb154edeb617?utm_source=1099&utm_campaign=Software%20Engineer"}
    job_hash = job_id(job)

    posted_jobs(job_hash)

main()




# def filter_jobs(jobs, remote_only=False):
#     """
#     Optionally filter jobs (e.g., only remote positions).
#     """
#     if remote_only:
#         return [job for job in jobs if job["location"].lower() == "remote"]
#     return jobs