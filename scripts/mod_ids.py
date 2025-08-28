import json
import os
from pathlib import Path

import requests
from re import sub
from urllib.request import urlretrieve
from zipfile import ZipFile
import tempfile

from scripts import common


def mod_ids():
	edit_files = False
	event_id = "toybox"
	submissions_url = f"https://platform.modfest.net/event/{event_id}/submissions"

	with tempfile.TemporaryDirectory() as tmpdir_name:
		os.chdir(Path(tmpdir_name))
		submissions_ids = dict()
		print(submissions_url)
		for submission in json.loads(requests.get(submissions_url).text):
			safe_id = sub(r"[^a-zA-Z0-9_]", "", submission["id"])
			version_url = f"https://api.modrinth.com/v3/project/{submission["platform"]["project_id"]}/version/{submission["platform"]["version_id"]}"
			print(version_url)
			version = json.loads(requests.get(version_url).text)
			if "files" in version:
				for file in version["files"]:
					if file["primary"]:
						print(file["url"])
						local_filename, headers = urlretrieve(file["url"], file["filename"])
						with ZipFile(local_filename, 'r') as archive:
							fmj = json.loads(archive.read("fabric.mod.json"))
							submissions_ids[submission["id"]] = fmj["id"]
							break
			if submission["id"] not in submissions_ids:
				submissions_ids[submission["id"]] = f"not found! try \"{safe_id}\""
		os.chdir(common.get_repo_root())

		for sub_id in sorted(submissions_ids.keys()):
			mod_id = submissions_ids[sub_id]
			print(f"\"{sub_id}\": \"{mod_id}\"")
			if edit_files:
				sub_file = common.get_repo_root() / f"scripts/data/{sub_id}.json"
				sub_json = json.loads(common.read_file(sub_file))
				sub_json["mod_id"] = mod_id
				with open(sub_file, "w") as f:
					f.write(json.dumps(sub_json, indent=2))

if __name__ == "__main__":
	mod_ids()
