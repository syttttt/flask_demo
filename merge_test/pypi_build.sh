python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python setup.py install
pip -V
pwd
java -jar ../scantist-bom-detect.jar --debug
deactivate
mv dependency-tree.json ../$1
cd ..
pwd
#python3 cmp_json.py
