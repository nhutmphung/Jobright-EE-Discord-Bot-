from fetch_jobs import fetch_jobs
import re


#takes the mark down text as a string and parses the text
def filter_jobs(string):
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

def main():
    raw_data = fetch_jobs()
    jobs = filter_jobs(raw_data)

    for job in (jobs[:2]):
        print(f"{job['title']} at {job['company']} ({job['location']}): {job['url']}")


main()

# def filter_jobs(jobs, remote_only=False):
#     """
#     Optionally filter jobs (e.g., only remote positions).
#     """
#     if remote_only:
#         return [job for job in jobs if job["location"].lower() == "remote"]
#     return jobs