rm -rf lambda-layer/
mkdir lambda-layer
mkdir lambda-layer/python
pip3 install -r requirements.txt --target lambda-layer/python
