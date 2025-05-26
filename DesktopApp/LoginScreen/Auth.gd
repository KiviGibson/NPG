extends Node

@export var login_input: TextEdit
@export var password_input: TextEdit
@export var info: Label
func login() -> void:
	var message: String = await WebManager.login(login_input.text,password_input.text)
	if message == "OK":
		self.visible = false
	info.text = message

func register() -> void:
	var message: String = await WebManager.register(login_input.text,password_input.text)
	if message == "OK":
		self.visible = false
	info.text = message
