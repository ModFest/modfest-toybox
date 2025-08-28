import json

import requests


def ballotbox_options():
	event_id = "toybox"
	options = []
	submissions_url = f"https://platform.modfest.net/event/{event_id}/submissions"
	print(submissions_url)
	for submission in json.loads(requests.get(submissions_url).text):
		option = {
			"id": submission["id"],
			"mod_id": submission["mod_id"],
			"name": submission["name"],
			"description": submission["description"],
			"platform": {
				"type": submission["platform"]["type"]
			}
		}
		if "project_id" in submission["platform"]:
			option["platform"]["project_id"] = submission["platform"]["project_id"]
		if "homepage_url" in submission["platform"]:
			option["platform"]["homepage_url"] = submission["platform"]["homepage_url"]
		options.append(option)

	print(f"Writing {len(options)} submissions to options.json")
	with open(f"../pack/resources/datapack/required/mf_ballotbox/data/ballotbox/ballot/options.json", 'w', encoding="utf8") as out_file:
		json.dump(options, out_file, indent='\t')
	print("done!")


if __name__ == "__main__":
	ballotbox_options()
