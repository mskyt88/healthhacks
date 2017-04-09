# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, jsonify, render_template, request
import json
import pprint


app = Flask(__name__)

rest_infos = []
fd = open("restaurants_sample.json")
for line in fd:
	rest_infos.append( json.loads(line) )
fd.close()

def getKey(rest):
	return rest["rating"]

# For Android app
def pass_rest(x1, y1, x2, y2):
	rest_inarea=[]

	for rest_info in rest_infos:
		if (rest_info["coordinates"]["longitude"] > y1 and rest_info["coordinates"]["longitude"] < y2) :
			if (rest_info["coordinates"]["latitude"] > x1 and rest_info["coordinates"]["latitude"] < x2) :
				rest_inarea.append( rest_info )
	print rest_inarea
	rest_sort = sorted( rest_inarea, key=getKey, reverse=True)
	if len(rest_sort) > 30:
		return jsonify( results=rest_sort[0:29] );
	else:
		return jsonify( results=rest_sort );


# For Web UI
def get_rest(lat,long):
	rest_inarea=[]

	for rest_info in rest_infos:
		if (rest_info["coordinates"]["longitude"] > long-0.005 and rest_info["coordinates"]["longitude"] < long+0.005) :
			if (rest_info["coordinates"]["latitude"] > lat-0.005 and rest_info["coordinates"]["latitude"] < lat+0.005) :
				rest_inarea.append( rest_info )

	rest_sort = sorted( rest_inarea, key=getKey, reverse=True)
	if len(rest_sort) > 10:
		return jsonify( results=rest_sort[0:9] );
	else:
		return jsonify( results=rest_sort );
	
	
@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/hello')
@app.route('/hello/<name>')
def Hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/map')
def Map():
	return app.send_static_file('map_view.html')
	
@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

@app.route('/pass', methods=["GET"])
def Pass():
	x1 = float(request.args.get('x1'))
	x2 = float(request.args.get('x2'))
	y1 = float(request.args.get('y1'))
	y2 = float(request.args.get('y2'))

	return pass_rest(x1, y1, x2, y2)

@app.route('/get', methods=["GET"])
def Rest():
	x_center = float(request.args.get('x'))
	y_center = float(request.args.get('y'))
	return get_rest(x_center, y_center)
	
@app.route('/gtest', methods=['GET'])
def GetTest():
	return request.args.get('lang')
	
@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)

@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug=True)
