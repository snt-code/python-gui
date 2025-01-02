import dearpygui.dearpygui as dpg
import numpy as np

# Function to load an OBJ file
def load_obj(filepath):
    vertices = []
    faces = []

    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Vertex
                _, x, y, z = line.split()
                vertices.append([float(x), float(y), float(z)])
            elif line.startswith('f '):  # Face
                _, *face = line.split()
                faces.append([int(f.split('/')[0]) - 1 for f in face])  # OBJ is 1-indexed

    return np.array(vertices), np.array(faces)

# Simple orthographic projection
def project_vertex(vertex, width, height, scale=100):
    x, y, _ = vertex  # Ignore Z for orthographic projection
    return (width // 2 + x * scale, height // 2 - y * scale)

# Apply rotation matrices
def rotate_vertices(vertices, angles):
    rx, ry, rz = np.radians(angles)
    # Rotation matrix around X axis
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(rx), -np.sin(rx)],
        [0, np.sin(rx), np.cos(rx)]
    ])
    # Rotation matrix around Y axis
    Ry = np.array([
        [np.cos(ry), 0, np.sin(ry)],
        [0, 1, 0],
        [-np.sin(ry), 0, np.cos(ry)]
    ])
    # Rotation matrix around Z axis
    Rz = np.array([
        [np.cos(rz), -np.sin(rz), 0],
        [np.sin(rz), np.cos(rz), 0],
        [0, 0, 1]
    ])
    # Combine rotations
    R = Rz @ Ry @ Rx
    return vertices @ R.T

# Render the OBJ in Dear PyGui
def render_obj(vertices, faces, width, height, angles):
    dpg.delete_item("canvas", children_only=True)  # Clear previous drawings

    # Rotate vertices
    rotated_vertices = rotate_vertices(vertices, angles)

    # Draw faces as triangles
    for face in faces:
        points_2d = [project_vertex(rotated_vertices[idx], width, height) for idx in face]
        if len(points_2d) == 3:  # Triangular face
            dpg.draw_triangle(points_2d[0], points_2d[1], points_2d[2], color=(200, 200, 200, 255), fill=(200, 200, 200, 150), parent="canvas")
        elif len(points_2d) > 3:  # Handle quads or other polygons
            for i in range(1, len(points_2d) - 1):
                dpg.draw_triangle(points_2d[0], points_2d[i], points_2d[i + 1], color=(200, 200, 200, 255), fill=(200, 200, 200, 150),parent="canvas")

# Callback for updating rotation
def update_rotation(sender, app_data, user_data):
    angles = user_data["angles"]
    angles[0] = dpg.get_value("rotation_x")
    angles[1] = dpg.get_value("rotation_y")
    angles[2] = dpg.get_value("rotation_z")
    render_obj(user_data["vertices"], user_data["faces"], 800, 600, angles)

# Main application
def main():
    obj_file = "cube.obj"  # Replace with your OBJ file path
    vertices, faces = load_obj(obj_file)

    # Initial rotation angles
    angles = [0, 0, 0]

    dpg.create_context()

    with dpg.window(label="3D Object Viewer", width=800, height=700):
        dpg.add_slider_float(label="Rotation X", tag="rotation_x", default_value=0, min_value=0, max_value=360,
                             callback=update_rotation, user_data={"angles": angles, "vertices": vertices, "faces": faces})
        dpg.add_slider_float(label="Rotation Y", tag="rotation_y", default_value=0, min_value=0, max_value=360,
                             callback=update_rotation, user_data={"angles": angles, "vertices": vertices, "faces": faces})
        dpg.add_slider_float(label="Rotation Z", tag="rotation_z", default_value=0, min_value=0, max_value=360,
                             callback=update_rotation, user_data={"angles": angles, "vertices": vertices, "faces": faces})
        dpg.add_drawlist(tag="canvas", width=800, height=600)

    render_obj(vertices, faces, 800, 600, angles)

    dpg.create_viewport(title="OBJ Viewer", width=800, height=700)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()
