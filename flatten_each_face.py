import bpy
from bpy.types import Operator
import bmesh


def get_average_float(float_list):
    return sum(float_list) / len(float_list)


def flatten_each_face(faces_to_flatten):
    """Iterates over each face and scales it flat along its normal, for best results repeat 10 - 100 times"""
    for face in faces_to_flatten:

        average_x = []
        average_y = []
        average_z = []

        for vert in face.verts:
            average_x.append(vert.co[0])
            average_y.append(vert.co[1])
            average_z.append(vert.co[2])

        average_x = get_average_float(average_x)
        average_y = get_average_float(average_y)
        average_z = get_average_float(average_z)

        center = (average_x, average_y, average_z)

        bpy.ops.mesh.select_all(action="DESELECT")
        face.select = True
        bpy.ops.transform.resize(value=(1, 1, 0), orient_type="NORMAL", center_override=center)


class MESH_OT_flatten_each_face(Operator):
    """Flatten each selected face"""

    bl_idname = "object.flatten_each_face"
    bl_label = "Flatten Each Face"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        # Get the active mesh
        obj = context.edit_object
        me = obj.data

        # Get a BMesh representation
        bm = bmesh.from_edit_mesh(me)

        faces_to_flatten = []

        for face in bm.faces:
            if face.select:
                faces_to_flatten.append(face)

        iterations = 10
        for _ in range(0, iterations):
            flatten_each_face(faces_to_flatten)

        # Show the updates in the viewport
        # and recalculate n-gon tessellation.
        bmesh.update_edit_mesh(me, loop_triangles=True)

        return {"FINISHED"}


def draw(self, context):
    """Draw the operator as an option on a menu."""
    layout = self.layout
    layout.operator(MESH_OT_flatten_each_face.bl_idname)


def register():
    bpy.utils.register_class(MESH_OT_flatten_each_face)
    bpy.types.VIEW3D_MT_edit_mesh_clean.append(draw)


def unregister():
    bpy.utils.unregister_class(MESH_OT_flatten_each_face)
    bpy.types.VIEW3D_MT_edit_mesh_clean.remove(draw)
