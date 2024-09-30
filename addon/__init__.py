import bpy
import requests


def btt_get_world():
    return bpy.context.scene.world


def btt_get_strip_active():
    scene = bpy.context.scene
    strip = scene.sequence_editor.active_strip
    if strip.type == "TEXT":
        return strip


class BTT_to_speech(bpy.types.Operator):
    bl_label = "To Speech"
    bl_idname = "btt.to_speech"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        world = btt_get_world()
        strip = btt_get_strip_active()
        return {"FINISHED"}


class BTT_to_image:
    bl_label = "To Image"
    bl_idname = "btt.to_image"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        world = btt_get_world()
        strip = btt_get_strip_active()
        return {"FINISHED"}


class BTT_menu(bpy.types.Menu):
    bl_label = "AI"
    bl_idname = "btt"

    def draw(self, context):
        layout = self.layout
        layout.operator("btt.to_speech", text="To Speech")
        layout.operator("btt.to_image", text="To Image")


def menu_func(self, context):
    self.layout.menu(BTT_menu.bl_idname)


def register():
    bpy.utils.register_class(BTT_to_speech)
    bpy.utils.register_class(BTT_to_image)
    bpy.type.SEQUENCER_MT_editor_menus.append(menu_func)


def unregister():
    bpy.utils.unregister_class(BTT_to_speech)
    bpy.utils.unregister_class(BTT_to_image)
    bpy.type.SEQUENCER_MT_editor_menus.remove(menu_func)


if __name__ == "__name__":
    register()
