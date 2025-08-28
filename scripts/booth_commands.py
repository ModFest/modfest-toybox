import json

import requests
from re import sub
from textwrap import wrap

dir_yaw = {
	"north": -180,
	"north_north_east": -150,
	"north_east": -135,
	"east_north_east": -120,
	"east": -90,
	"east_south_east": -60,
	"south_east": -45,
	"south_south_east": -30,
	"south": 0,
	"south_south_west": 30,
	"south_west": 45,
	"west_south_west": 60,
	"west": 90,
	"west_north_west": 120,
	"north_west": 135,
	"north_north_west": 150
}

def warps():
	event_id = "toybox"
	submissions_url = f"https://platform.modfest.net/event/{event_id}/submissions"
	
	for submission in json.loads(requests.get(submissions_url).text):
		booth = submission["booth_data"]
		if not booth:
			continue
		warp_id = sub(r"[^a-zA-Z0-9 ]", "", submission["name"].lower())
		safe_id = sub(r"[^a-zA-Z0-9_]", "", submission["id"])
		print(f"warps remove \"{warp_id}\"") # patbox pls
		print(f"warps create \"{warp_id}\" \"{submission["name"]}\" {booth["item_icon"] or "minecraft:gold_nugget"} {booth["warp"]["x"]} {booth["warp"]["y"]} {booth["warp"]["z"]} {dir_yaw[booth["warp"]["direction"]]} 0")
		print(f"landmarks new id modfest:booth/{safe_id} {booth["marker_pos"]["x"]} 240 {booth["marker_pos"]["z"]} {booth["item_icon"] or "minecraft:gold_nugget"} \"{submission["name"]}\" \"♦{booth["shards"] or "?"} ⧗{booth["minutes_to_complete"] or "?"}\\n{"\\n".join(wrap(submission["description"].replace("\"", "\\\""), width=40))}\"")


if __name__ == "__main__":
	warps()
