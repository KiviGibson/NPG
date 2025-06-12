class_name DashBoard

extends Node

@export var graph: Graph
@export var filters: Filters


func update_graph() -> void:
	var error := WebManager.get_data(filters.get_filters(), response_update)
	push_error(error)

func response_update(response, code, _headers, body) -> void:
	if response != HTTPRequest.RESULT_SUCCESS or code != 200:
		push_error("Couldn't retrive data")
		return
	var list: Dictionary[String, Array]
	for element in body["data"]:
		var date := Time.get_datetime_dict_from_unix_time(element["date"]) 
		list[date["day"] +"-"+ str(date["month"])] = [element["sys"], element["dys"], element["pulse"]]
	graph.update(list)
