class_name Filters

extends Node

signal commit_changes
@export var max_value: Array[TextEdit]
@export var min_value: Array[TextEdit]
@export var date_min: Callendar
@export var date_max: Callendar

func _ready() -> void:
	date_min.set_date(date_min.get_date()-84600*14)
	for m in max_value:
		m.focus_exited.connect(update_max)
	for m in min_value:
		m.focus_exited.connect(update_min)
	date_min.changed.connect(update_min)
	date_max.changed.connect(update_max)

func update_min(_val: bool = false):
	print("MIN")
	if date_min.get_date() > date_max.get_date():
		date_min.set_date(date_max.get_date())
	for i in range(3):
		if int(min_value[i].text) > int(max_value[i].text):
			min_value[i].text = max_value[i].text

func update_max(_val: bool = false):
	print("MAX")
	if date_min.get_date() > date_max.get_date():
		date_max.set_date(date_min.get_date())
	for i in range(3):
		if int(min_value[i].text) > int(max_value[i].text):
			max_value[i].text = min_value[i].text

func get_filters() -> Dictionary:
	return {
		"sys": [int(min_value[0].text),int(max_value[0].text)],
		"dys": [int(min_value[1].text), int(max_value[1].text)],
		"pulse": [int(min_value[2].text), int(max_value[2].text)],
		"date": [date_min.get_date(), date_max.get_date()]
		}

func commit() -> void:
	commit_changes.emit()
