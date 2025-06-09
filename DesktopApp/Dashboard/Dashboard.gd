class_name DashBoard

extends Node

@export var graph: Graph
@export var filters: Filters


func update_graph() -> void:
	var filter_settings := filters.get_filters()
	var list: Dictionary[String, Array]
	# do usunięcia -----------------------
	for value in range(filter_settings["date"][0], filter_settings["date"][1]+1, 86400):
		var dict := Time.get_datetime_dict_from_unix_time(value)
		var napis: String = str(dict["day"]) +"-"+str(dict["month"])
		var num := randi_range(filter_settings["value"][0], filter_settings["value"][1])
		@warning_ignore("integer_division")
		list[napis] = [num, num-20, num/2]
	# ------------------------------------
	var data :=  list # await WebManager.get_data(filter_settings)
	# check if data is correct then
	graph.update(data)
