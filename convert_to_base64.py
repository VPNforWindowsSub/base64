import base64
import requests
import os
from github import Github

def convert_to_base64(url, github_token):
    # Download text file from the URL
    response = requests.get(url)
    if response.status_code == 200:
        text = response.text
        # Encode text to base64
        encoded_bytes = base64.b64encode(text.encode('utf-8'))
        encoded_text = encoded_bytes.decode('utf-8')
        # Save base64-encoded text to base64.txt
        file_path = 'base64.txt'
        with open(file_path, 'w') as f:
            f.write(encoded_text)
        print(f"Conversion complete. File saved to: {file_path}")
        print(f"Current working directory: {os.getcwd()}")

        # Authenticate with GitHub using personal access token
        g = Github(github_token)
        repo = g.get_repo("VPNforWindowsSub/base64")

        # Get main branch
        branch = repo.get_branch("main")

        # Create a new file in the repository
        commit_message = "Add base64.txt"
        repo.create_file("base64.txt", commit_message, encoded_text, branch="main")
    else:
        print("Failed to fetch data from URL.")

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/dimzon/scaling-sniffle/main/all-sort.txt"
    github_token = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"  # Replace with your GitHub personal access token
    convert_to_base64(url, github_token)
