import json

USERCACHE_PATH		= "./example_data/"
ADVANCEMENTS_PATH	= "./example_data/advancements/"

with open("advancement_ids.json","r") as f:
	ids = json.load(f)


def serverwide_advancements():
	with open(USERCACHE_PATH+"usercache.json","r") as f:
		usercache = json.load(f)

	all_advancements = {}

	for cache in usercache:
		name, uuid = cache["name"], cache["uuid"]
		all_advancements[name] = advancement_states(uuid)
	
	return all_advancements


def advancement_states(uuid):
	obtained = obtained_ids(uuid)
	return {
			advancement: namespace_id in obtained
			for advancement, namespace_id in ids.items()
			}


def obtained_ids(uuid):
	try:
		with open(ADVANCEMENTS_PATH+f"{uuid}.json","r") as f:
			content = json.load(f)
	except:
		return set()
	return set(
			i[i.index(":")+1:]
			for i in content
			if i!="DataVersion" and content[i]["done"])
