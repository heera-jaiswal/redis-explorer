from flask import Flask,request
from flask_restful import reqparse, abort, Api, Resource
import flask
from redis_explorer.commands import search_keys,key_info,hash_val,string_val,set_val
import json

def get_success_result(data):
	return {"success":True,"result":data}
def get_failed_result(e,trace=None):
	return {"success":False,"msg":str(e),"trace":trace}

class SearchKeys(Resource):
	"""docstring for SearchKeys"""
	def post(self):		
		try:			
			json_data=request.json
			pattern = json_data["pattern"]
			redis_hash = json_data["redis_hash"]
			max_keys = json_data.get("max_keys",1000)
			timeout = json_data.get("timeout",60)
			list_keys = search_keys.search(pattern=pattern,redis_hash=redis_hash,max_keys=max_keys,timeout=timeout)
			return get_success_result(list_keys)
		except Exception as e:
			return get_failed_result(e)	

class GetKeyEncoding(Resource):
	def post(self):
		try:
			import json				
			json_data=request.json
			key = json_data["key"]
			redis_hash = json_data["redis_hash"]
			encoding = key_info.get_key_encoding(key=key,redis_hash=redis_hash)
			key_type = key_info.get_key_type(key=key,redis_hash=redis_hash)
			data = {"key":key,"encoding":encoding,"type":key_type}
			return get_success_result(data)		
		except Exception as e:
			return get_failed_result(e)	

class ConnectClient(Resource):
	def post(self):
		try:
			from redis_explorer.redis_manager import connect_client
			import json				
			json_data=request.json
			redis_url=json_data["redis_url"]
			details = connect_client(redis_url)
			return get_success_result(data=details)
		except Exception as e:
			import traceback
			trace=traceback.format_exc()
			return get_failed_result(e,trace=trace)

class FetchValue(Resource):
	def post(self):
		try:
			from redis_explorer.redis_manager import connect_client
			import json		
			#string, list, set, zset and hash.		
			json_data=request.json
			key = json_data["key"]
			redis_hash = json_data["redis_hash"]
			val=None
			key_type = key_info.get_key_type(key=key,redis_hash=redis_hash)
			ttl = key_info.get_key_ttl(key=key,redis_hash=redis_hash)
			if key_type=="hash":
				val = hash_val.fetch_all_hash_values(redis_hash=redis_hash,key=key)
			elif key_type=="string":
				val = string_val.fetch_string_val(redis_hash=redis_hash,key=key)
			elif key_type=="list":
				pass
			elif key_type=="zset":
				pass
			elif key_type=="set":
				val = set_val.fetch_set_val(redis_hash=redis_hash,key=key)
			else:
				raise Exception("Invalid Key Type")
			return get_success_result(data={"val":val,"type":key_type,"ttl":ttl})
		except Exception as e:
			import traceback
			trace=traceback.format_exc()
			return get_failed_result(e,trace=trace)
class Test(Resource):
	def get(self):
		return {}		