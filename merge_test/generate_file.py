import os
import requests
import random
import json

import pdb

def get_lib():
	url = "http://159.138.86.248:5000/get_library"
	header = {"Content-Type": "application/json"}
	platform = ['Maven','Pypi','NPM']
	pkm = platform[random.randint(0,2)]
	content = {
		"platform": pkm,
		"number": 1
	}
	response = requests.post(url,headers= header, data=json.dumps(content)).content
	# pdb.set_trace()
	dict = json.loads(response)
	buf = "".join(dict.keys())
	vendor = buf.split(":")[0]
	library = buf.split(":")[1]
	version = "".join(dict.values())
	print(pkm, vendor, library, version)
	generate(pkm, vendor, name=library, version=version)

def build_lib(name, version):
	HOME_PATH = os.getcwd()
	# os.chdir((HOME_PATH + "/tmp/"))
	file_list = os.listdir(HOME_PATH)

	cmd_line = ""
	if "pom.xml" in file_list:
		cmd_line = "mvn install"
	elif "requirements.txt" in file_list:
		cmd_line = "pip install -r requirements.txt"
	else:
		cmd_line = "npm install " + name + "@" + version
	os.system(cmd_line)

def bom_detect(pkm, vendor, name, version):
	os.system("java -jar ../scantist-bom-detect.jar --debug")
	# os.system("cat dependency-tree.json")
	if vendor:
		cmd = "mv dependency-tree.json /app/" +pkm+":"+vendor+":"+name+":"+version + ".json"
	else:
		cmd = "mv dependency-tree.json /app/" +pkm+":"+name+":"+version + ".json"
	os.system(cmd)

def generate(pkm, vendor, name, version):
	if not os.path.exists("temp"):
	# 	# os.makedirs("tmp/")
		os.system("mkdir temp")
	os.chdir("temp")
	maven_complete = [
		"<project>" + "\n",
		"<modelVersion>4.0.0</modelVersion>" + "\n",
		"<groupId> fake_id </groupId>"+ "\n",
		"<artifactId> fake_id </artifactId>"+ "\n",
		"<version>1.0.0</version>"+ "\n",
		"<dependencies>"+ "\n",
		"<dependency>"+ "\n",
		"<groupId>" + vendor + "</groupId>"+ "\n",
		"<artifactId>" + name + "</artifactId>"+ "\n",
		"<version>" + version + "</version>"+ "\n",
		"<scope></scope>"+ "\n",
		"</dependency>"+ "\n",
		"</dependencies>"+ "\n",
		"</project>"
	]
	pypi_setup_complete = [
		"from distutils.core import setup"+ "\n",
		"files = [\"things/*\"]"+ "\n",
		"setup(name=\""+name+"\",version=\""+version+"\")"
	]
	# pdb.set_trace()
	if pkm == "Maven":
		with open("pom.xml","w") as fp:
			fp.writelines(maven_complete)
		fp.close()
	if pkm == "Pypi":
		with open("requirements.txt","w") as fp:
			fp.write(name+ "=="+ version)
		fp.close()
		# with open("setup.py","w") as fp:
		# 	fp.writelines(pypi_setup_complete)
		# fp.close()
	if pkm == "NPM":
		# npm install name@version
		pass

	build_lib(name=name, version=version)
	bom_detect(pkm, vendor, name , version)

if __name__ == '__main__':
    # generate(
	# 	"Maven",
	# 	"org.apache.shiro.tools",
	# 	"shiro-tools-hasher",
	# 	"1.4.2"
	# )
	# generate("Pypi","","halogen","1.5.0")
	get_lib()

