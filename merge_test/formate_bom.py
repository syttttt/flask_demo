import os
import json
import pdb

def formate_deps(deps):
	if not deps:
		return None

	# pdb.set_trace()
	ret_deps = {}
	ret_deps['artifact_id'] = deps["artifact_id"]
	ret_deps['group_id'] = deps["group_id"]
	try:
		ret_deps['version'] = deps["version"]
	except Exception as e:
		print(e, deps["artifact_id"])
	ret_deps['dependencies'] = []
	if 'dependencies' in deps:
		for content in deps["dependencies"]:
			subdep = formate_deps(content)
			if subdep:
				ret_deps['dependencies'].append(subdep)
	return ret_deps

def get_formated_bomdata(path):
	with open(path, "r") as fp:
		raw = json.load(fp)
	list = path.split(":")
	# pdb.set_trace()
	if(len(list)) == 4:
		vendor = "".join(list[1])
		name = "".join(list[2])
		version = "".join(list[3]).replace(".json","")
	else:
		vendor = ""
		name = "".join(list[1])
		version = "".join(list[2]).replace(".json","")
	if raw['projects']:
		raw['projects'][0]['artifact_id'] = name
		raw['projects'][0]['group_id'] = vendor
		raw['projects'][0]['version'] = version
		return formate_deps(raw['projects'][0])
	else:
		# return {}
		return {
			"artifact_id" : "",
			"group_id" : "",
			"version" : "",
			"dependencies": []
		}

# if __name__ == '__main__':
#     print(get_formated_bomdata("requests_2.22.0.json"))
