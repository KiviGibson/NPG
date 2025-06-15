class_name CustomGraphElement

extends Node

signal update_desc(text: String)

@export var size: Array[TextureRect]
@export var date_label: Label
var desc: String

func set_node(value: Array, date: String) -> void:
	for i in range(3):
		size[i].custom_minimum_size[1] = value[i] * 3
	date_label.text = date
	self.desc = value[3]

func _on_mouse_enter() -> void:
	update_desc.emit(desc)


func _on_mouse_exited() -> void:
	update_desc.emit("")
