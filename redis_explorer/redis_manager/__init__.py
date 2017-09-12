import redis
import re
import hashlib
import base64

_redis_clients={}
class RedisClient(object):
	def __init__(self,redis_password="",redis_host="127.0.0.1",redis_port=6379,redis_db=0,redis_url=None,refresh=False):		
		"""
			Init redis client if it has not been initialized or if it is to refresh on purpose
		"""

		global _redis_clients		
		#acbdef@e127.0.0.1:6379/1
		if not redis_url:
			if redis_password:
				redis_url=redis_password+"@"+redis_host+":"+str(redis_port)+"/"+str(redis_db)
			else:
				redis_url=redis_host+":"+str(redis_port)+"/"+str(redis_db)
		else:
			match=re.match(r'((?P<pwd>[^@]*)@)?(?P<host>[^:]*)(:(?P<port>\d+))?(/(?P<db>\d+))?',redis_url)
			if match:
				redis_password = match.group("pwd")
				redis_host = match.group("host")
				redis_port = match.group("port")
				redis_db = match.group("db")
				if not redis_db:
					redis_db=0
				if not redis_port:
					redis_port=6379
				if not redis_host:
					redis_host="127.0.0.1"
				print redis_password,redis_host,redis_port
			else:
				raise Exception("Invalid Redis URL")
		redis_hash = self.calculate_hash_base64(redis_url)
		redis_client = _redis_clients.get(redis_hash,None)
		if not redis_client or refresh:			
			redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, password=redis_password, socket_connect_timeout=1,socket_timeout=1, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)				
			print redis_client				
			_redis_clients[redis_hash]=redis_client
		self._redis_client = redis_client
		self._redis_hash = redis_hash

	def get_client(self):
		return self._redis_client

	def get_hash(self):
		return self._redis_hash

	def calculate_hash_base64(self,payload):
		try:			
			digest = hashlib.md5(payload).digest()
			return base64.urlsafe_b64encode(digest)			
		except Exception as e:
			raise Exception(str(payload)+"|"+str(e))

def get_client(redis_hash):
	global _redis_clients
	if redis_hash in _redis_clients:
		return _redis_clients[redis_hash]
	else:
		return None

def connect_client(redis_url):
	objRedisClient = RedisClient(redis_url=redis_url)
	client = objRedisClient.get_client()
	redis_hash=objRedisClient.get_hash()
	info=client.info()
	print redis_hash
	return {"redis_hash":redis_hash,"info":info}