class_name CustomGraphElement

extends Node

@export var size: Array[TextureRect]
@export var date_label: Label

func set_node(value: Array, date: String) -> void:
	for i in range(3):
		size[i].custom_minimum_size[1] = value[i] * 3
	date_label.text = date
