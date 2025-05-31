class_name Callendar
extends Node

signal changed
@export var title: Label
@export var current: Dictionary
@export var date: Dictionary
@export var container: Node
func _ready() -> void:
	date = Time.get_datetime_dict_from_system()
	date["minute"] = 0
	date["second"] = 0
	date["hour"] = 0
	update_callendar()
	var counter := 1
	for child in container.get_children():
		var button : Button = child.get_child(0)
		button.text = str(counter)
		button.pressed.connect(update_date(counter))
		counter += 1

func update_date(num: int) -> Callable:
	return func ():
		container.get_child(date["day"]-1).get_child(0).self_modulate = Color(1,1,1)
		date["day"] = num
		update_callendar()

func reduce_month() -> void:
	var m:int = int(date["month"])
	if m == 1: 
		m = 12
		date["year"] -= 1
	else: m -= 1
	change_daycount(m)

func increase_month() -> void:
	var m:int = int(date["month"])
	if m == 12: 
		m = 1
		date["year"] += 1
	else: m += 1
	change_daycount(m)

func change_daycount(m: int) -> void:
	container.get_child(date["day"]-1).get_child(0).self_modulate = Color(1,1,1)
	match m:
		1, 3, 5, 7, 8, 10, 12:
			for child in container.get_children():
				child.visible = true
		2:
			var a := 28
			if date["year"] % 4 == 0 and (date["year"] % 100 != 0 or date["year"] % 400 == 0): a+=1
			for num in range(a, 31):
				container.get_child(num).visible = false
		_:
			container.get_child(30).visible = false
	date["month"] = m
	date["day"] = 1
	update_callendar()

func  update_callendar():
	title.text = str(date["month"]) + " - " + str(date["year"])
	container.get_child(date["day"]-1).get_child(0).self_modulate = Color(0.4,0.7,1)
	changed.emit()

func get_date() -> int:
	return Time.get_unix_time_from_datetime_dict(date)
	
func set_date(unix: int):
	if "day" in date:
		container.get_child(date["day"]-1).get_child(0).self_modulate = Color(1,1,1)
	date = Time.get_date_dict_from_unix_time(unix)
	update_callendar()
