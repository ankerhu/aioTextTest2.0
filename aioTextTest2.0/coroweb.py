import asyncio,os,inspect,logging,functools

#Define decorator @get('/path')
def get(path):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args,**kw):
			return func(*args,**kw)
		wrapper.__method__ = 'GET'
		wrapper.__route__ = path
		return wrapper
	return decorator

#Define decorator @post('/path')
def post(path):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args,**kw):
			return func(*args,**kw)
		wrapper.__method__ = 'POST'
		wrapper.__route__ = path
		return wrapper
	return decorator

class RequestHandler(object):
	def __init__(self,app,fn):
