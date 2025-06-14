class_name LineElement

extends Node
@export var label:Label
func set_value(value: int) -> void:
	label.text = str(value)
