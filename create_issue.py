import requests
import subprocess
import os
import tempfile

# Constants
GITLAB_URL = "https://gitlab.example.com"
API_TOKEN = "your_personal_access_token"
PROJECT_ID = "your_project_id"
ISSUE_TEMPLATE = """\
# Title: Your issue title here
# Description
Describe the issue here in detail.
"""

def get_issue_details_vim(template):
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tmpfile:
        tmpfile.write(template.encode())
        tmpfile.flush()
        editor = os.getenv('EDITOR', 'vim')
        subprocess.call([editor, tmpfile.name])
        tmpfile.seek(0)
        return tmpfile.read().decode()

def create_issue(gitlab_url, api_token, project_id, title, description):
    url = f"{gitlab_url}/api/v4/projects/{project_id}/issues"
    headers = {
        "PRIVATE-TOKEN": api_token,
        "Content-Type": "application/json"
    }
    data = {
        "title": title,
        "description": description
    }
    response = requests.post(url, headers=headers, json=data)
    return response

def main():
    print("Opening Vim to edit issue details...")
    issue_details = get_issue_details_vim(ISSUE_TEMPLATE)
    lines = issue_details.split('\n')
    title = lines[0].replace('# Title: ', '').strip()
    description = '\n'.join(lines[1:]).strip()

    print(f"Creating issue with title: {title}")
    response = create_issue(GITLAB_URL, API_TOKEN, PROJECT_ID, title, description)

    if response.status_code == 201:
        print("Issue created successfully.")
        print("Issue URL:", response.json().get('web_url'))
    else:
        print("Failed to create issue.")
        print("Response:", response.status_code, response.json())

if __name__ == "__main__":
    main()
