from flask import Flask,request
import os
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'
from utils.utils import (
    InvalidInputException,
    GenericAPIException,
	get_start
    # get_library_and_version,
	# get_library_and_version_M
)

@app.route('/test',methods=['POST'])
def test():
	'''
	Get the randome library version
	in the input data.
	:raises InvalidInputException: In case of bad input data
	'''
	try:
		if request.headers['Content-Type'] == 'application/json':
			input_data = request.json
			# Validate input and call the Core API
			res = get_start(input_data['platform'], input_data['vendor'],
							 input_data['name'], input_data['version'])
		else:
			raise InvalidInputException('Unsupported input format')
	except Exception as e:
		raise GenericAPIException(str(e))
	# os.chdir("./merge_test/record")
	# file = os.listdir()[0]
	# with open(file) as fp:
	# 	lines = fp.readlines()
	# os.remove(file)
	return res


if __name__ == '__main__':
    app.run(host='0.0.0.0')

