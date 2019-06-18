class BasicHTTPHandler():
	'''
	This class is a basic HTTP parser for validating the request
	'''

	def __init__(self, raw_request):
		self.raw_request = raw_request.decode()
		self.command, self.path, self.protocol, self.protocol_version, self.headers = self.parse_request()
	
	def parse_request(self):
		"Turn basic request headers in something we can use"
		requestlines = [i.strip() for i in self.raw_request.splitlines()]

		# Get the method, path, and which version of HTTP is used from the request
		command, path, request_version = [i.strip() for i in requestlines[0].split()]

		protocol, protocol_version = [i.strip() for i in request_version.split('/')]
		
		
		if command != 'GET':
			raise InvalidRequest('This protocol supports only GET requests')
		
		if protocol != 'HTTP':
			raise InvalidRequest('Incorrect HTTP protocol provided')
		
		if protocol_version != '1.1':
			raise InvalidRequest('HTTP version unsupported')
		
		# Get the request headers
		headers = {}
		for k, v in [i.split(':', 1) for i in requestlines[1:-1]]:
			headers[k.strip()] = v.strip()
		
		return command, path, protocol, protocol_version, headers

	
	def __repr__(self):
		return repr({'method': self.command, 'path': self.path, 'protocol': self.protocol, 'protocol_version': self.protocol_version , 'headers': self.headers})
		
class InvalidRequest(Exception):
	pass
