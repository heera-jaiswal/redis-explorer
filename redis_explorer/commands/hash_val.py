def fetch_all_hash_values(redis_hash,key):
	from redis_explorer.redis_manager import get_client	
	client=get_client(redis_hash)
	result = dict(client.hscan_iter(key))
	return result
