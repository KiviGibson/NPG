class_name DashBoard

extends Node

@export var graph: Graph
@export var filters: Filters


func update_graph() -> void:
	var error := WebManager.get_data(filters.get_filters(), response_update)
	if error:
		push_error(error)

func response_update(response, code, _headers, body) -> void:
	if response != HTTPRequest.RESULT_SUCCESS or code != 200:
		push_error("Couldn't retrive data")
		return
	var list: Dictionary[String, Array]
	var data = JSON.parse_string(body.get_string_from_utf8())["data"]
	print(data)
	for element in data:
		print(element)
		var date := Time.get_datetime_dict_from_unix_time(element["date"]) 
		list[date["day"] +"-"+ str(date["month"])] = [element["sys"], element["dys"], element["pulse"]]
	graph.update(list)
