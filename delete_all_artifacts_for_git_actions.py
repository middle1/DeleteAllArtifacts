import sys
import requests
from tqdm import tqdm

def delete_all_artifacts(owner, repo, token):
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
            print("No artifacts available for deletion.")
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

if len(sys.argv) != 4:
    print("Usage: python script.py <owner> <repo> <token>")
    sys.exit(1)

owner, repo, token = sys.argv[1], sys.argv[2], sys.argv[3]

delete_all_artifacts(owner, repo, token)
