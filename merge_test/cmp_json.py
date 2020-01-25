import os
import shutil
# HOME_PATH = os.getcwd()
# os.chdir(HOME_PATH + "/tmp/")

# os.system("java -jar ../scantist-bom-detect.jar --debug")


from merge_test import formate_bom
from merge_test import formate_graph

def compare(a, b, root, record):
	if a['version'] != b['version']:
		print('version_mismatch:', root + '/' + a['artifact_id'], a['version'], b['version'])
		record['version_mismatch'].append(
			{'path': root + '/' + a['artifact_id'], 'pkg-mgr-ver': a['version'], 'graph-ver': b['version']}
		)
	elif a['group_id'] != b['group_id']:
		print('vendor_mismatch:', root + '/' + a['artifact_id'], a['group_id'], b['group_id'])
		record['vendor_mismatch'].append(
			{'path': root + '/' + a['artifact_id'], 'pkm-vendor': a['group_id'], 'graph-vendor': b['group_id']}
		)
	else:
		deps_a = []
	deps_b = []
	if 'dependencies' in a:
		deps_a = a['dependencies']
	if 'dependencies' in b:
		deps_b = b['dependencies']
	match_count = 0
	for x in deps_a:
		flag = False
		for y in deps_b:
			if x['artifact_id'] == y['artifact_id']:
				compare(x, y, root + '/' + a['artifact_id'], record)
				flag = True
				break
		if flag == True:
			match_count += 1
		else:
			print('artifact from A not_found in B:', root + '/' + a['artifact_id'], x['artifact_id'], x['version'])
			record['missed_in_graph'].append(
				{'path': root + '/' + a['artifact_id'], 'artifact_id': x['artifact_id'], 'version': x['version']})
	for y in deps_b:
		flag = False
		for x in deps_a:
			if x['artifact_id'] == y['artifact_id']:
				flag = True
				break
		if flag == False:
			print('artifact from B not_found in A:', root + '/' + a['artifact_id'], y['artifact_id'], y['version'])
			record['added_in_graph'].append(
				{'path': root + '/' + a['artifact_id'], 'artifact_id': y['artifact_id'], 'version': y['version']})

def json_cmp():
	os.chdir("merge_test")
	list = os.listdir()
	print(os.getcwd())
	for file in list:
		if ".json" in file:
			res1 = formate_bom.get_formated_bomdata(file)
			list = file.split(":")
			break

	# pdb.set_trace()
	if len(list) == 4:
		res2 = formate_graph.get_formated_graphdata(list[0], list[1], list[2], list[3].replace(".json", ""))
	else:
		res2 = formate_graph.get_formated_graphdata(list[0], "", list[1], list[2].replace(".json", ""))
	record = {'added_in_graph': [], 'missed_in_graph': [], 'version_mismatch': [], 'vendor_mismatch': []}
	compare(res1, res2, "", record=record)

	os.remove(file)
	shutil.rmtree("temp")
	os.chdir("record")
	# os.chdir('/app/record')
	with open(file.replace(".json", ""), "w+") as fp:
		fp.write('added_in_graph : ' + str(record['added_in_graph']) + '\n')
		fp.write('missed_in_graph : ' + str(record['missed_in_graph']) + '\n')
		fp.write('version_mismatch : ' + str(record['version_mismatch']) + '\n')
		fp.write('vendor_mismatch : ' + str(record['vendor_mismatch']) + '\n')
	fp.close()

	print(record)
	return record


if __name__ == '__main__':
	# os.system("cd ..")
	json_cmp()
