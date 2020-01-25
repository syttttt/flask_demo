import os
# from cmp_json import json_cmp
from merge_test import cmp_json

# import cmp_json
def generate(pkm, vendor, name, version):
	if not os.path.exists("temp"):
		# 	# os.makedirs("tmp/")
		os.system("mkdir temp")
	os.chdir("temp")
	maven_complete = [
		"<project>" + "\n",
		"<modelVersion>4.0.0</modelVersion>" + "\n",
		"<groupId> fake_id </groupId>" + "\n",
		"<artifactId> fake_id </artifactId>" + "\n",
		"<version>1.0.0</version>" + "\n",
		"<dependencies>" + "\n",
		"<dependency>" + "\n",
		"<groupId>" + vendor + "</groupId>" + "\n",
		"<artifactId>" + name + "</artifactId>" + "\n",
		"<version>" + version + "</version>" + "\n",
		"<scope></scope>" + "\n",
		"</dependency>" + "\n",
		"</dependencies>" + "\n",
		"</project>"
	]
	pypi_setup_complete = [
		"from distutils.core import setup" + "\n",
		"files = [\"things/*\"]" + "\n",
		"setup(name=\"" + name + "\",version=\"" + version + "\")"
	]
	# pdb.set_trace()
	if pkm == "Maven":
		with open("pom.xml", "w") as fp:
			fp.writelines(maven_complete)
		fp.close()
	if pkm == "Pypi":
		with open("requirements.txt", "w") as fp:
			fp.write(name + "==" + version)
		fp.close()
		# os.system("python3 -m venv venv")
		with open("setup.py", "w") as fp:
			fp.writelines(pypi_setup_complete)
		fp.close()
		with open("run.py", "w") as fp:
			fp.write("import " + name)
		fp.close()
	if pkm == "NPM":
		# npm install name@version
		pass

	build_lib(platform=pkm, vendor=vendor, name=name, version=version)


# bom_detect(pkm, vendor, name , version)

def build_lib(platform, vendor, name, version):
	if platform == "Pypi":
		string = platform + ":" + name + ":" + version
		os.system("bash ../pypi_build.sh " + string + ".json")
	else:
		HOME_PATH = os.getcwd()
		print("---build---" + HOME_PATH)
		# os.chdir((HOME_PATH + "/tmp/"))
		file_list = os.listdir(HOME_PATH)

		cmd_line = ""
		if "pom.xml" in file_list:
			cmd_line = "mvn install"
		else:
			# cmd_line = "npm install " + name + "@" + version
			cmd_line = "cnpm install " + name + "@" + version
		os.system(cmd_line)
		os.system("java -jar ../scantist-bom-detect.jar --debug")
		if vendor:
			cmd = "mv dependency-tree.json ../" + platform + ":" + vendor + ":" + name + ":" + version + ".json"
		else:
			cmd = "mv dependency-tree.json ../" + platform + ":" + name + ":" + version + ".json"
		os.system(cmd)


def start(platform, vendor, name, number):
	print(platform, vendor, name, number)
	home = os.getcwd()
	print(home)
	os.chdir("merge_test")
	generate(platform, vendor, name, number)
	os.chdir(home)
	return (cmp_json.json_cmp())


# generate("Pypi","","products.simplecalendarportlet","1.0b")
# start("Pypi","","django_cacheops_with_stats","1.3.1")
# start("Pypi", "", "requests", "2.22.0")
