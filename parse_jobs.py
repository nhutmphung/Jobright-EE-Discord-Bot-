import hashlib
from fetch_jobs import fetch_jobs
import re

#data setup
raw_data = fetch_jobs()


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

def job_id(job):
    url_bytes = job['url'].encode('utf-8')
    job_id = hashlib.sha256(url_bytes).hexdigest()
    print(job_id)

    return job_id

def main():
    job = {"url": "https://example.com/job1"}
    job_hash = job_id(job)
    print(job_hash)



# def filter_jobs(jobs, remote_only=False):
#     """
#     Optionally filter jobs (e.g., only remote positions).
#     """
#     if remote_only:
#         return [job for job in jobs if job["location"].lower() == "remote"]
#     return jobs