class_name Graph

extends Node
@export var graph_data: Control
@export var graph_element: PackedScene
@export var max_pressure_value: int
@export var line: PackedScene
@export var graph_line: Control

func _ready() -> void:
	for value in range(max_pressure_value,-1,-10):
		var tmp:LineElement = line.instantiate()
		tmp.set_value(value)
		graph_line.add_child(tmp)

func update(data:Dictionary[String,int]) -> void:
	for child in graph_data.get_children():
		graph_data.remove_child(child)
		child.queue_free()
	for entry in data:
		var temp: CustomGraphElement = graph_element.instantiate()
		temp.set_node(data[entry], entry)
		graph_data.add_child(temp)
