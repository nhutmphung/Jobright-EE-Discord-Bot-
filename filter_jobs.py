from fetch_jobs import fetch_jobs
import re


#takes the mark down text as a string and parses the text
def filter_jobs(string):
    jobs = []
    lines = string.split("\n")

    for line in lines:
        if line.startswith("| ** "):  # example: each job starts with '|"
            #uses regex to capture the position, company, location, url
            match = re.match(r"- \*\*(.*?)\*\* at (.*?) \((.*?)\) - \[.*?\]\((.*?)\)", line)
            if match:
                title, company, location, url = match.groups()
                jobs.append ({
                    "title": title,
                    "company": company, 
                    "location": location,
                    "url": url
                }


                )
    print(jobs)
    return jobs

# def filter_jobs(jobs, remote_only=False):
#     """
#     Optionally filter jobs (e.g., only remote positions).
#     """
#     if remote_only:
#         return [job for job in jobs if job["location"].lower() == "remote"]
#     return jobs