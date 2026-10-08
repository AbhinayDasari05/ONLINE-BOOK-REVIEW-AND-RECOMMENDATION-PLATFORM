import requests
import json
import csv
import sys
import base64

if len(sys.argv) < 3:
    print("Usage: python jira_sync.py <JIRA_DOMAIN_OR_URL> <JIRA_EMAIL> [API_KEY]")
    sys.exit(1)

jira_domain = sys.argv[1].strip()
if not jira_domain.startswith("http"):
    jira_domain = f"https://{jira_domain}.atlassian.net"

email = sys.argv[2].strip()
api_token = sys.argv[3].strip() if len(sys.argv) > 3 else "ATATT3xFfGF0FGMDF2rN2rxE3bjmN4FvMUQgPwk9SBeCkNk-f_u3nAv49B4sKmjl-fr4ZUUxhn8eCgSFqhP0JfXkhVx9V7wSh5EoqSCvLUJsRGfHQTCdVnpeZh51IcE7UMiJvq4-uCyYdwuna63MBJYPLLn7X11VBHjwCS4y18Dq6JqEivBLGvA=EAE6389F"

auth_str = f"{email}:{api_token}"
auth_bytes = auth_str.encode('ascii')
base64_auth = base64.b64encode(auth_bytes).decode('ascii')

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Basic {base64_auth}"
}

print(f"Connecting to {jira_domain} as {email}...")

# 1. Test authentication & find project
res = requests.get(f"{jira_domain}/rest/api/3/project", headers=headers)
if res.status_code != 200:
    print(f"Failed to authenticate or fetch projects. HTTP {res.status_code}: {res.text}")
    sys.exit(1)

projects = res.json()
print("Available Projects in Jira:")
target_project_key = None
for p in projects:
    print(f" - [{p['key']}] {p['name']}")
    if "book" in p['name'].lower() or "recommendation" in p['name'].lower():
        target_project_key = p['key']

if not target_project_key:
    if len(projects) > 0:
        target_project_key = projects[0]['key']
        print(f"Defaulting to first project: {target_project_key}")
    else:
        print("No projects found in Jira account.")
        sys.exit(1)

print(f"Using Project Key: {target_project_key}")

# 2. Read stories from CSV and create issues
csv_file = "/Users/abhinaydasari/Documents/sse/secure-book-review-platform/docs/phase-09-backlog/book_platform_jira_import.csv"

created_count = 0
with open(csv_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        summary = row['Summary']
        description = row['Description']
        priority = row.get('Priority', 'Medium')

        issue_payload = {
            "fields": {
                "project": {
                    "key": target_project_key
                },
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {
                    "name": "Story"
                }
            }
        }

        create_res = requests.post(f"{jira_domain}/rest/api/3/issue", headers=headers, json=issue_payload)
        if create_res.status_code in [200, 201]:
            issue_key = create_res.json().get('key')
            print(f"Created issue {issue_key}: {summary}")
            created_count += 1
        else:
            print(f"Failed to create issue '{summary}': {create_res.status_code} - {create_res.text}")

print(f"Done! Successfully created {created_count} issues in Jira project {target_project_key}.")
