from flask import Flask,request
from flask_restful import reqparse, abort, Api, Resource
MAIN_PATH='/explorer/'
def register_views(app):
	from redis_explorer import views
	app.add_url_rule(MAIN_PATH, endpoint='index', view_func=views.index)
	app.add_url_rule(MAIN_PATH+'static/<path:path>',endpoint='static_files',view_func=views.static_files)	
	#return "OK"		
	


def register_apis(api):
	from redis_explorer.APIs import SearchKeys,GetKeyEncoding,ConnectClient,FetchValue,Test
	api.add_resource(SearchKeys,MAIN_PATH+'search/',endpoint='SearchKeys')		
	api.add_resource(GetKeyEncoding,MAIN_PATH+'key/',endpoint='GetKeyEncoding')		
	api.add_resource(FetchValue,MAIN_PATH+'val/',endpoint='FetchValue')		
	api.add_resource(ConnectClient,MAIN_PATH+'connect/',endpoint='ConnectClient')		
	api.add_resource(Test,MAIN_PATH+'test/',endpoint='Test')		

def init_app():	
	app = Flask(__name__)
	##RESTful api on flask app
	api = Api(app)
	
	register_apis(api)
	register_views(app)
	return app

def start():
	import sys
	ip="0.0.0.0"
	if len(sys.argv)>1:
		 ip = sys.argv[1]
	## Load config	
	#app.run(debug=True)
	#app.run(host="0.0.0.0",port=5000)
	app=init_app()
	app.run(host=ip,port=5252,debug=False)	

if __name__ == '__main__':		
	## Used for debubing or local development
	start()
	pass