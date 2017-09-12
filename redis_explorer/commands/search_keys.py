#import signal
from datetime import datetime,timedelta
class TimeoutException(Exception):
	"""docstring for TimeoutException"""
	def __init__(self):
		super(TimeoutException, self).__init__("operation timeout")


def timeout_handler(signum, frame):
	#signal.alarm(0)
	raise TimeoutException()

def search(pattern,redis_hash,max_keys,timeout):
	from redis_explorer.redis_manager import get_client	
	#signal.signal(signal.SIGALRM, timeout_handler)
	#signal.alarm(timeout)
	list_keys = []

	try:
		client = get_client(redis_hash)
		if client:
			print client.info()
			print pattern
			#itr=client.scan_iter(pattern)
			itr=my_scan(client,match=pattern,timeout=timeout)
			print itr

			counter=0
			
			for key in itr:
				list_keys.append(key)
				counter+=1
				if counter>=max_keys:
					break				
			#signal.alarm(0)
			return list_keys
		else:
			raise Exception("No Client found ! %s" % redis_hash)	
	except Exception as e:
		#signal.alarm(0)
		raise e
	else:
		pass
	finally:
		pass


def my_scan(client,match=None, count=None,timeout=30):
	d1=datetime.now()
	cursor = '0'
	delta_timeout=timedelta(seconds=timeout)
	while cursor != 0:					
		cursor, data = client.scan(cursor=cursor,match=match, count=count)
		for item in data:
			yield item

		d2=datetime.now()
		delta=d2-d1
		if(delta>=delta_timeout):
			break

		 
	