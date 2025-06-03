extends Node

@export var ip: TextEdit
@export var login_input: TextEdit
@export var password_input: TextEdit
@export var info: Label
func login() -> void:
	if not check(): return
	var message: String = await WebManager.login(login_input.text,password_input.text)
	if message == "OK":
		self.visible = false
	info.text = message

func register() -> void:
	if not check(): return
	var message: String = await WebManager.register(login_input.text,password_input.text)
	if message == "OK":
		self.visible = false
	info.text = message


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
