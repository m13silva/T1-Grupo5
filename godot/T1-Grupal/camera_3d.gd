extends Camera3D


# Called when the node enters the scene tree for the first time.
func _ready():
	var t = get_global_transform()
	print("basis y: ", t.basis.y)
	print("basis z: ", t.basis.z)
	print("origin: ", t.origin)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
