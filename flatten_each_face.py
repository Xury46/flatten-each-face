import bpy
from bpy.types import Mesh, Object, Operator
from bpy.props import BoolProperty, IntProperty
import bmesh
from bmesh.types import BMesh, BMFace
from mathutils import Matrix, Vector


def flatten_each_face(faces_to_flatten: list[BMFace]) -> None:
    """Iterates over each face and scales it flat along its normal"""
    for face in faces_to_flatten:
        face_center: Vector = face.calc_center_median()

        face.normal_update()  # Force the normal to be re-calculated
        flatten_matrix = Matrix.Scale(
            0,  # factor
            4,  # size
            face.normal,  # axis
        )

        for vert in face.verts:
            vert.co -= face_center
            vert.co = vert.co @ flatten_matrix
            vert.co += face_center


class MESH_OT_flatten_each_face(Operator):
    """Flatten each selected face"""

    bl_idname = "object.flatten_each_face"
    bl_label = "Flatten Each Face"
    bl_options = {"REGISTER", "UNDO"}

    iterations: IntProperty(
        name="Iterations",
        min=1,
        soft_max=25,
        default=10,
        description="How many times to flatten each face",
    )

    selected_only: BoolProperty(
        name="Selected Only",
        default=True,
        description="Flatten only the selected faces",
    )

    def execute(self, context):

        # Get the active mesh
        obj: Object = context.edit_object
        me: Mesh = obj.data

        # Get a BMesh representation
        bm: BMesh = bmesh.from_edit_mesh(me)

        faces_to_flatten: list[BMFace] = []

        for face in bm.faces:
            should_flatten_this_face: bool = True
            if self.selected_only:
                should_flatten_this_face = face.select

            if should_flatten_this_face:
                faces_to_flatten.append(face)

        for _ in range(0, self.iterations):
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
