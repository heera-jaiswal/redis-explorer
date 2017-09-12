from flask import render_template,make_response,send_from_directory
STATIC_FOLDER="/home/ec2-user/redis-explorer/src/redis_explorer/static"
def index():
	response = make_response(render_template('index.html'))
	#response = make_response(render_template('index.html', foo=42))
	#response.headers['X-Parachutes'] = 'parachutes are cool'
	return response

def static_files(path):
	return send_from_directory(STATIC_FOLDER,path)
