extends Node
@export var Cookie: String = ""
@export var headers: Array[String] = [
	"User-Agent: App/1.0 (GODOT)",
	"Accept: JSON",
]
@export var host: Dictionary = {"ip":"localhost","port":5000}

func login(login: String, password: String) -> String:
	var http: HTTPClient = HTTPClient.new()
	var err: Error = http.connect_to_host(host["ip"], host["port"])
	if err != OK:
		return "Can't connect to host"
	while (http.get_status() == HTTPClient.STATUS_CONNECTING or
		http.get_status() == HTTPClient.STATUS_RESOLVING):
		http.poll()
		await get_tree().process_frame
	if http.get_status() != HTTPClient.STATUS_CONNECTED:
		return "Connection failed"
	var req_headers: Array[String] = generate_headers("{'login':"+login+"','password':'"+password+"'}")
	err = http.request(HTTPClient.METHOD_POST, "/login", headers)
	if err != OK:
		return "Something went wrong!"
	while http.get_status() == HTTPClient.STATUS_REQUESTING:
		http.poll()
		await get_tree().process_frame
	if not http.get_status() != HTTPClient.STATUS_BODY and not http.get_status() != HTTPClient.STATUS_CONNECTED:
		return "Bad Request"
	if http.has_response():
		if http.get_response_code() == 200:
			var h = http.get_response_headers_as_dictionary()
			Cookie = h["Set-Cookie"]
			return "OK"
		elif http.get_response_code() == 404:
			return "Endpoint not found"
	return "No response"

func register(login:String, password: String) -> String:
	var http: HTTPClient = HTTPClient.new()
	var err: Error = http.connect_to_host(host["ip"], host["port"])
	if err != OK:
		return "Can't connect to host"
	while (http.get_status() == HTTPClient.STATUS_CONNECTING or
		http.get_status() == HTTPClient.STATUS_RESOLVING):
		http.poll()
		await get_tree().process_frame
	if http.get_status() != HTTPClient.STATUS_CONNECTED:
		return "Connection failed"
	var req_headers: Array[String] = generate_headers("{'login':"+login+"','password':'"+password+"'}")
	err = http.request(HTTPClient.METHOD_POST, "/register", headers)
	if err != OK:
		return "Something went wrong!"
	while http.get_status() == HTTPClient.STATUS_REQUESTING:
		http.poll()
		await get_tree().process_frame
	if not http.get_status() != HTTPClient.STATUS_BODY and not http.get_status() != HTTPClient.STATUS_CONNECTED:
		return "Bad Request"
	if http.has_response():
		if http.get_response_code() == 200:
			var h = http.get_response_headers_as_dictionary()
			Cookie = h["Set-Cookie"]
			return "OK"
		elif http.get_response_code() == 404:
			return "Endpoint not found"
	return "No response"

func get_data() -> String:
	var http: HTTPClient = HTTPClient.new()
	var err: Error = http.connect_to_host(host["ip"], host["port"])
	if err != OK:
		return "Can't connect to host"
	while (http.get_status() == HTTPClient.STATUS_CONNECTING or
		http.get_status() == HTTPClient.STATUS_RESOLVING):
		http.poll()
		await get_tree().process_frame
	if http.get_status() != HTTPClient.STATUS_CONNECTED:
		return "Connection failed"
	var req_headers: Array[String] = generate_headers()
	err = http.request(HTTPClient.METHOD_POST, "/register", headers)
	if err != OK:
		return "Something went wrong!"
	while http.get_status() == HTTPClient.STATUS_REQUESTING:
		http.poll()
		await get_tree().process_frame
	if not http.get_status() != HTTPClient.STATUS_BODY and not http.get_status() != HTTPClient.STATUS_CONNECTED:
		return "Bad Request"
	if http.has_response():
		if http.get_response_code() == 200:
			var h = http.get_response_headers_as_dictionary()
			Cookie = h["Set-Cookie"]
			return "OK"
		elif http.get_response_code() == 404:
			return "Endpoint not found"
		elif http.get_response_code() == 418:
			return "Teapod"
	return "No response"

func add_data() -> Array[Data]:
	return []

func generate_headers(body: String = "") -> Array[String]:
	var res: Array[String] = []
	for e in headers:
		res.append(e)
	if Cookie != "":
		res.append("Cookie:"+Cookie)
	if body != "":
		res.append("Body:"+body)
	return res
