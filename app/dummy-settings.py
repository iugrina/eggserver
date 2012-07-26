from tornado.options import define
define("engine", default="mysql", help="database engine (mysql, sqlite..)")
define("port", default=8888, help="run on the given port", type=int)
define("host", default="localhost", help="database host")
define("database", default="egg", help="database name")
define("user", default="user", help="database user")
define("password", default="password", help="database password")
