extends TextEdit

func update() -> void:
	if not self.text.is_valid_float():
		self.text = "0"
