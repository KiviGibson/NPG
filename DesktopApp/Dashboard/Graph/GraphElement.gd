class_name CustomGraphElement

extends Node

@export var size: Control
@export var value_label: Label
@export var date_label: Label

func set_node(value: int, date: String) -> void:
	size.custom_minimum_size[1] = value*3
	value_label.text = str(value)
	date_label.text = date
