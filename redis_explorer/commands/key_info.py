def get_key_encoding(key,redis_hash):	
	from redis_explorer.redis_manager import get_client	
	client = get_client(redis_hash)
	return client.object("ENCODING",key)

def get_key_type(key,redis_hash):
	from redis_explorer.redis_manager import get_client	
	client = get_client(redis_hash)
	return client.type(key)

def get_key_ttl(key,redis_hash):
	from redis_explorer.redis_manager import get_client	
	client = get_client(redis_hash)
	return client.ttl(key)