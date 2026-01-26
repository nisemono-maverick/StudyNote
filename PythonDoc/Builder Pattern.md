use to create complex objects
```python
class DatabaseConnection:
	def __init__(self, host, port, username, password, max_connections=None, 	timeout=None, enable_ssl=False, ssl_cert=None, connection_pool=None, retry_attempts-None, compression=False, read_preference=None):
		self.host = host
		self.port = port
		self.username = username
		self.password = password
		self.max_connections = max_connections
		# validate timeout
		if timeout is not None and timeout <= 0:
			raise ValueError ("Connect timeout must be positive") self. timeout = timeout
		self.enable_ssl = enable_ssl
		self.ssl_cert = ssl_cert
		self.connection_pool = connection_pool
		self.retry_attempts = retry_attempts
		self.compression = compression
		self.read_preference = read_preference

def connect(self):
	return f"Connecting to database at {self.host): {self.port} with username '{self. username)'"
	
def client():
	connection = DatabaseConnection("localhost", 5432, "admin", "password", max_connections=100, timeout=30, enable_ssl=True, ssl_cert="/path/to/cert", connectIon_pool=20, retry_attempts=3, compression=True, read_preference="secondary"
	)
	print(connection. connect ())
	
client()
```
there are 2 problems
1. the contructors do 2 things, init attributes and validate 
2. because it need too many parameters, it's so complex to create a new instance

builder class
```python
class DatabaseConnectionBuilder:
```

