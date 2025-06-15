class_name PopUp

extends Node

@export var num_fields: Array[TextEdit]
@export var date_field: TextEdit
@export var text_field: TextEdit

var date: int

func show() -> void:
	var date_dct := Time.get_datetime_dict_from_system()
	date_field.text = str(date_dct["day"]) + "-" + str(date_dct["month"]) + "-" + str(date_dct["year"])
	date = Time.get_unix_time_from_datetime_dict(date_dct)
	date
	for field in num_fields:
		field.text = ""
	self.visible = true

func hide() -> void:
	self.visible = false

func add() -> void:
	var data: Dictionary[String, Variant]= {
		"sys": float(num_fields[0].text), 
		"dys": float(num_fields[1].text), 
		"pulse": float(num_fields[2].text), 
		"date": date - (date % 86400),
		"desc": text_field.text
		}
	var error := WebManager.add_data(data, is_success)
	if error:
		push_error(error)

func is_success(_res, code, _headers, _body) -> void:
	if code == 200:
		hide()
