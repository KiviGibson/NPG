class_name Auth

extends Node

@export var ip: TextEdit
@export var login_input: TextEdit
@export var password_input: TextEdit
@export var info: Label
@export var board: DashBoard


func login() -> void:
	if not check(): return
	info.text = WebManager.login(login_input.text,password_input.text, login_response)

func login_response(response, code, headers, _body) -> void:
	if response != HTTPRequest.RESULT_SUCCESS:
		push_error("Couldn't retrive data")
	if code == 200:
		for header in headers:
			if -1 != header.find("Set-Cookie: "):
				WebManager.Cookie = header.split(": ")[1]
		login_success()
	else:
		info.text = "Login not successful."

func register() -> void:
	if not check(): return
	info.text = WebManager.register(login_input.text,password_input.text, register_response)
	
func register_response(response, code, headers: Array[String], _body) -> void:
	if response != HTTPRequest.RESULT_SUCCESS:
		push_error("Couldn't retrive data")
	if code == 200:
		for header in headers:
			if -1 != header.find("Set-Cookie: "):
				WebManager.Cookie = header.split(": ")[1]
		login_success()
	else:
		info.text = "Register not successful."

func check() -> bool:
	var args := ip.text.split(":")
	if len(args) != 2 and is_nan(int(args[1])):
		info.text = "przykład poprawnego adresu ip: 127.0.0.1:3000"
		return false
	WebManager.host = {"ip":args[0],"port":int(args[1])}
	if password_input.text == "" or login_input.text == "":
		info.text = "dane logowania nie zostały wypełnione"
		return false
	return true

func login_success() -> void:
	self.visible = false
	board.visible = true
	board.update_graph()
