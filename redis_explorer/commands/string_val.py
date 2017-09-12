def fetch_string_val(redis_hash,key):
	from redis_explorer.redis_manager import get_client	
	client=get_client(redis_hash)
	result = client.get(key)
	return result
