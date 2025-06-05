class_name Filters

extends Node

signal commit_changes
@export var max_value: HSlider
@export var min_value: HSlider
@export var maxl:Label
@export var minl: Label
@export var date_min: Callendar
@export var date_max: Callendar

func update(_val: bool = false):
	if date_min.get_date() > date_max.get_date():
		date_max.set_date(date_min.get_date())
	if max_value.value < min_value.value:
		max_value.set_value_no_signal(min_value.value)
	maxl.text = str(int(max_value.value))
	minl.text = str(int(min_value.value))

func get_filters() -> Dictionary:
	return {
		"value": [int(min_value.value), int(max_value.value)], 
		"date": [date_min.get_date(), date_max.get_date()]
		}

func commit() -> void:
	commit_changes.emit()
