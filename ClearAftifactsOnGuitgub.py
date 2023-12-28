import requests
import json
from tqdm import tqdm

config_file = "config.json"

def display_artifacts():
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/artifacts"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result_json = response.json()
        total_count = result_json.get("total_count", 0)
        artifacts = result_json.get("artifacts", [])

        print(f"List of artifacts (total {total_count}):")
        if total_count > 0:
            formatted_json = json.dumps(artifacts, indent=2)
            print(formatted_json)
        else:
            print("No available artifacts.")
    else:
        print(f"Request error. Status code: {response.status_code}")
        print(response.text)

def delete_all_artifacts():
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/artifacts"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        artifacts = response.json().get("artifacts", [])

        if not artifacts:
            print("No available artifacts for deletion.")
            return

        for artifact in tqdm(artifacts, desc="Deleting artifacts", unit="artifact"):
            artifact_id = artifact["id"]
            delete_url = f"https://api.github.com/repos/{owner}/{repo}/actions/artifacts/{artifact_id}"
            delete_response = requests.delete(delete_url, headers=headers)

            if delete_response.status_code == 204:
                print(f"Artifact with ID {artifact_id} deleted successfully.")
            else:
                print(f"Error deleting artifact with ID {artifact_id}. Status code: {delete_response.status_code}")
                print(delete_response.text)
    else:
        print(f"Request error. Status code: {response.status_code}")
        print(response.text)

try:
    with open(config_file, "r") as file:
        config_data = json.load(file)
except FileNotFoundError:
    config_data = {}

owner = input(f"Enter the repository owner's name (OWNER) [{config_data.get('owner', '')}]: ") or config_data.get('owner', '')
repo = input(f"Enter the repository name (REPO) [{config_data.get('repo', '')}]: ") or config_data.get('repo', '')
token = input(f"Enter your access token (YOUR-TOKEN) [{config_data.get('token', '')}]: ") or config_data.get('token', '')

# Save current data
config_data = {'owner': owner, 'repo': repo, 'token': token}
with open(config_file, "w") as file:
    json.dump(config_data, file)

choice = input("Choose an action:\n1 - Display all artifacts\n2 - Delete all artifacts\n")

if choice == "1":
    display_artifacts()
elif choice == "2":
    delete_all_artifacts()
else:
    print("Invalid choice.")
