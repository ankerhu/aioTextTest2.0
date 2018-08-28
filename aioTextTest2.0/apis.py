'''
JSON API definition
'''
import json,logging,inspect,functools

#base APIError which contains error(required),data(optional) and message(optional).
class APIError(Exception):
	def __init__(self,error,data='',message=''):
		super(APIError,self).__init__(message)
		self.error = error
		self.data = data
		self.message = message
