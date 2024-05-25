bl_info = {
    "name": "Flatten Each Face",
    "author": "Xury Greer",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "3D View > Mesh > Clean Up",
    "description": "Flatten each selected face of a mesh",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}

# Import / reload local modules (Required when using the "Reload Scripts" (bpy.ops.scripts.reload()) operator in Blender
if "bpy" in locals():
    import importlib

    importlib.reload(flatten_each_face)
else:
    from . import flatten_each_face

import bpy


def register():
    flatten_each_face.register()


def unregister():
    flatten_each_face.unregister()
