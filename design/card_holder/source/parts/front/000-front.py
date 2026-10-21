# Legacy target "front" is the user-marked bottom cover.
card_width = param("card_width", 65.0)
card_height = param("card_height", 100.0)
card_thickness = param("card_thickness", 1.0)
plan_clearance = param("card_side_clearance", 0.3)
depth_clearance = param("card_depth_clearance", 0.4)
rim_width = param("bond_rim_width", 2.4)
outer_radius = param("outer_corner_radius", 2.0)
front_thickness = param("front_thickness", 1.6)
extension = param("front_top_extension", 15.0)
hole_width = param("front_lanyard_width", 18.0)
hole_height = param("front_lanyard_height", 5.0)
hole_x = param("front_lanyard_center_x", 0.0)
locating_wall = param("front_locating_wall", 1.6)
recess_depth = param("front_lid_recess_depth", 1.6)
lid_clearance = param("front_lid_side_clearance", 0.07)
thumb_width = param("front_thumb_width", 18.0)
thumb_height = param("front_thumb_height", 32.0)
thumb_x = param("front_thumb_center_x", 0.0)
thumb_y = param("front_thumb_center_y", 5.5)
cavity_width = card_width + 2 * plan_clearance
cavity_height = card_height + 2 * plan_clearance
cavity_depth = card_thickness + depth_clearance
pocket_width = cavity_width + 2 * rim_width
pocket_bottom_y = -cavity_height / 2 - rim_width
pocket_radius = outer_radius + lid_clearance
outer_width = pocket_width + 2 * locating_wall
mouth_y = cavity_height / 2
bottom_y = pocket_bottom_y - locating_wall
top_y = mouth_y + extension
outer_height = top_y - bottom_y
hole_y = mouth_y + extension / 2
floor_z = -cavity_depth - front_thickness
# The full base floor connects the lanyard header and thumb region.
floor_profile = Pos(0, (top_y + bottom_y) / 2) * RectangleRounded(outer_width, outer_height, outer_radius)
base_shape = Pos(0, 0, floor_z) * extrude(floor_profile, amount=front_thickness)
# Raised lower body, stopped at card mouth, creates a U-shaped rim.
rim_profile = Pos(0, (mouth_y + bottom_y) / 2) * RectangleRounded(outer_width, mouth_y - bottom_y, outer_radius)
rim_shape = Pos(0, 0, -cavity_depth) * extrude(rim_profile, amount=cavity_depth + recess_depth)
base_shape = base_shape + rim_shape
# Deeper card cavity: square lower inside corners accept the stated card.
cut_top = top_y + outer_radius
cut_bottom = -cavity_height / 2
card_profile = Pos(0, (cut_top + cut_bottom) / 2) * Rectangle(cavity_width, cut_top - cut_bottom)
base_shape = base_shape - Pos(0, 0, -cavity_depth) * extrude(card_profile, amount=cavity_depth + recess_depth + front_thickness)
# Shallower front-lid pocket; rounded bottom corresponds to lid plus clearance.
seat_top = mouth_y + 2 * pocket_radius
seat_profile = Pos(0, (seat_top + pocket_bottom_y) / 2) * RectangleRounded(pocket_width, seat_top - pocket_bottom_y, pocket_radius)
base_shape = base_shape - extrude(seat_profile, amount=recess_depth + front_thickness)
# Both holes are in this same user-marked base.
hole_profile = Pos(hole_x, hole_y) * SlotOverall(hole_width, hole_height)
thumb_profile = Pos(thumb_x, thumb_y) * SlotOverall(thumb_height, thumb_width, rotation=90)
tool_z = floor_z - front_thickness
tool_depth = 3 * (front_thickness + cavity_depth + recess_depth)
base_shape = base_shape - Pos(0, 0, tool_z) * extrude(hole_profile, amount=tool_depth)
base_shape = base_shape - Pos(0, 0, tool_z) * extrude(thumb_profile, amount=tool_depth)
# Adhesive lands are continuous and coplanar at z=0, without a reservoir.
assert rim_width > lid_clearance
assert locating_wall >= 1.2 and recess_depth > 0
assert thumb_height >= thumb_width > 0
assert abs(thumb_x) + thumb_width / 2 < cavity_width / 2
assert thumb_y + thumb_height / 2 < mouth_y
assert thumb_y - thumb_height / 2 > -cavity_height / 2
assert extension > hole_height + 2 * outer_radius
assert hole_width >= hole_height > 0
assert abs(hole_x) + hole_width / 2 < outer_width / 2 - outer_radius
assert len(base_shape.solids()) == 1
print(f"Base {outer_width:.3f} x {outer_height:.3f} x {front_thickness+cavity_depth+recess_depth:.3f}; lid seat depth {recess_depth}; pocket width {pocket_width}; cavity {cavity_width} x {cavity_height} x {cavity_depth}; both holes on base")
base_shape.color = srgb("#457a88")
publish("front_panel", base_shape, "底盖 · 沉台与推卡孔", material="pla")