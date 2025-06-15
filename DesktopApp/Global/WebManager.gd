extends Node
@export var Cookie: String = ""
@export var headers: Array[String] = [
	"User-Agent: App/1.0 (GODOT)",
	"Accept: JSON",
]
var host: Dictionary = {"ip":"localhost","port":5000}

func login(login_str: String, password: String, subscriber: Callable) -> String:
	return post_request(subscriber, {"login":login_str, "password": password}, "/login")

func register(login_str:String, password: String, subscriber) -> String:
	return post_request(subscriber, {"login":login_str, "password": password}, "/register")

func get_data(filters:Dictionary, subscriber) -> String:
	return post_request(subscriber, {"filters": filters}, "/get_data")

func add_data(data: Dictionary[String, Variant], subscriber) -> String:
	return post_request(subscriber, {"data": data}, "/add_data")

func generate_headers() -> Array[String]:
	var res: Array[String] = []
	for e in headers:
		res.append(e)
	if Cookie != "":
		res.append("Cookie:"+Cookie)
	return res

func post_request(subscriber, body, endpoint) -> String:
	var head := generate_headers()
	var req := HTTPRequest.new()
	self.add_child(req)
	req.request_completed.connect(subscriber)
	var error := req.request("http://"+host["ip"]+":"+str(host["port"])+endpoint, head, HTTPClient.METHOD_POST, JSON.stringify(body))
	if error != OK: return "An error occurred in the HTTP request."
	else: return ""
