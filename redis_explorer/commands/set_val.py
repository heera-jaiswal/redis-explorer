def fetch_set_val(redis_hash,key):
	from redis_explorer.redis_manager import get_client	
	client=get_client(redis_hash)
	result = list(client.sscan(key))[1]
	return result
