import requests
import os
import json

# base_url = "http://159.138.86.248:8085/dependencies"
base_url = "http://localhost:8085/dependencies"
base_dict = {
	"platform": "",
	"vendor": "",
	"name": "",
	"version": ""
}
header = {"Content-Type": "application/json"}

def formate_deps(deps):
	if not deps:
		return None
	# pdb.set_trace()
	ret_deps = {}
	ret_deps['artifact_id'] = deps["libraryName"]
	ret_deps['group_id'] = deps["libraryVendor"]
	try:
		ret_deps['version'] = deps["version"]
	except Exception as e:
		print(e, deps["libraryName"])
	ret_deps['dependencies'] = []
	if 'dependenciesList' in deps:
		for content in deps["dependenciesList"]:
			subdep = formate_deps(content)
			if subdep:
				ret_deps['dependencies'].append(subdep)
	return ret_deps

def get_json(platform, vendor, name, version):
	d = base_dict
	d['platform'] = platform
	d['vendor'] = vendor
	d["name"] = name
	d["version"] = version

	data = json.dumps(d)
	# print(data)

	response = requests.post(base_url, headers=header, data=data).content
	return json.loads(response.decode())

def get_formated_graphdata(platform,vendor,name,version):
# print(get_json("npm","","nunjucks","3.1.7"))
	response = get_json(platform,vendor,name,version)
# response = get_json("pypi","","envault","0.2.1")
	if not "status" in response.keys():
		r = response['root']
	else:
		r = {
			"libraryName" : "",
			"libraryVendor" : "",
			"version" : "",
			"dependenciesList": []
		}
	return formate_deps(r)

# if __name__ == '__main__':
# 	print(get_formated_graphdata("pypi", "", "requests", "2.22.0"))
