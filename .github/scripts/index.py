import requests
import json
import os

REPO = "kishinight-production/explorateur-nexuria"
BRANCH = "main"

API_URL = f"https://api.github.com/repos/{REPO}/git/trees/{BRANCH}?recursive=1"

def main():
    try:
        headers = {}

        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"

        response = requests.get(API_URL, headers=headers)

        if response.status_code != 200:
            print(f"Erreur API GitHub: {response.status_code}")
            return

        data = response.json()

        if "tree" not in data:
            print("Réponse invalide API GitHub")
            return

        files = []

        for item in data["tree"]:
            if item["type"] == "blob":
                path = item["path"]

                if path.endswith(".md"):
                    print(f"Ajout de [{path}]")
                    files.append(path)

        files.sort()

        with open("index.json", "w", encoding="utf-8") as fichier:
            json.dump(files, fichier, indent=2, ensure_ascii=False)

        print(f"{len(files)} fichiers indexés")

    except Exception as erreur:
        print(f"Erreur script: {erreur}")


if __name__ == "__main__":
    main()