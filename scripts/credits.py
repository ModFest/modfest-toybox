#!/usr/bin/env python3
import json
import requests
import common


def main():
	repo_root = common.get_repo_root()
	constants = common.jsonc_at_home(common.read_file(repo_root / "constants.jsonc"))
	submissions_url = f"https://platform.modfest.net/event/{constants["event"]}/submissions"
	submissions = dict()
	users = dict()
	print(submissions_url)
	for submission in json.loads(requests.get(submissions_url).text):
		submissions[submission["id"]] = submission
		for user_id in submission["authors"]:
			if user_id not in users:
				user_url = f'https://platform.modfest.net/user/{user_id}'
				print(user_url)
				users[user_id] = json.loads(requests.get(user_url).text)

	creds = []
	for sub_id in submissions.keys():
		submission = submissions[sub_id]
		creds.append({
			"title": submission["name"],
			"names": [users[user_id]["name"] for user_id in submission["authors"]]
		})
	print(json.dumps(creds))


if __name__ == "__main__":
	main()
