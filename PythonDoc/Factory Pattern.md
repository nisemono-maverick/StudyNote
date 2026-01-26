a database connect class
```python
class DatabaseConnection:
	def __init__(self, host, port, username, password) :
		self. host = host
		self. port = port
		self. username = username
		self. password = password
		
	def connect(self):
		return f"Connecting to database at {self. host}: {self.port} with username '{self. username) '"
		
	def client():
		main_db = DatabaseConnection('localhost', 3306, 'root', 'password123')
		analytics_db = DatabaseConnection('192.168.1.1', 5432, 'admin', "securepass')
		cache_db = DatabaseConnection('10.0.0.1', 27017, 'cacheuser', 'cachepass')
		
		print (main_db.connect())
		print (analytics_db.connect())
		print (cache_db.connect())
		
client()
```
there are 2 problems:
1. Difficult to maintain
if database connct params change, need to modify every where we create a client
2. code duplication

Factory pattern: separate create objects and use objects
use a factory function to create objects
```python
class DatabaseConnection:
...	
			
	def connection_factory(db_type):
		db_configs = {
			'main': {
				'host': 'localhost',
				'port': 3306,
				'username': 'root',
				'password': 'password123'
			},
			'analytics': {
				'host': '192.168.1.1',
				'port': 5432,
				'username': 'admin',
				'password': 'securepass'
			},
			'cache': {
				'host': '10.0.0.1',
				'port': 27017,
				'username': 'cacheuser',
				'password': 'cachepass'
			}
		}
		return DatabaseConnection(**db_configs[db_type])
		
	def client():
		main_db = connection_factory('main')
		analytics_db = connection_factory('analytics')
		cache_db = connection_factory('cache')
		
		print (main_db.connect())
		print (analytics_db.connect())
		print (cache_db.connect())
		
client()
```
put database configs in a config file
config.py
```python
db_configs = {
			'main': {
				'host': 'localhost',
				'port': 3306,
				'username': 'root',
				'password': 'password123'
			},
			'analytics': {
				'host': '192.168.1.1',
				'port': 5432,
				'username': 'admin',
				'password': 'securepass'
			},
			'cache': {
				'host': '10.0.0.1',
				'port': 27017,
				'username': 'cacheuser',
				'password': 'cachepass'
			}
		}
```

```python
class DatabaseConnection:
...
	def connection_factory(db_type):
		from config import configs
		return DatabaseConnection(**db_configs[db_type])
...
```