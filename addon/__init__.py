import bpy
import requests
import os


def btt_exists(name):
    for strip in bpy.context.scene.sequence_editor.sequences:
        if strip.name == name:
            return True
    return False

def btt_get_strip_active():
    scene = bpy.context.scene
    strip = scene.sequence_editor.active_strip
    if strip:
        if strip.type == "TEXT":
            return strip

def btt_from_text(types, strip):
    sequences = bpy.context.scene.sequence_editor.sequences
    name=f'{strip.name}-{types}'
    if types == 'speech':
        filepath=f'//{types}/{strip.name}.mp3'
        if btt_post(types, strip, filepath) and not btt_exists(name):
            sound = sequences.new_sound(
                name=name,
                filepath=filepath,
                channel=strip.channel + 1,
                frame_start=int(strip.frame_start)
            )
    elif types == 'image':
        filepath=f'//{types}/{strip.name}.png'
        if btt_post(types, strip, filepath) and not btt_exists(name):
            image = sequences.new_image(
                name=name,
                filepath=filepath,
                channel=strip.channel - 2,
                frame_start=int(strip.frame_start)
            )
            image.frame_final_end = strip.frame_final_end

def btt_post(types, strip, filepath):
    abspath = bpy.path.abspath(filepath)
    if os.path.exists(abspath):
        return True
    
    scene = bpy.context.scene
    
    ai_url = "http://localhost:8080/"
    if 'ai_url' in scene:
        ai_url = scene['ai_url']
    
    ai_token = ""
    if 'ai_token' in scene:
        ai_token = scene['ai_token']
    
    ai_query = ""
    if 'ai_query' in strip:
        ai_query = strip['ai_query']
    
    ai_text = strip.text.strip()
    if types == 'image' and 'ai_text' in strip:
        ai_text = strip['ai_text']
        
    data = {
        "type": types,
        "width": scene.render.resolution_x,
        "height": scene.render.resolution_y,
        "text": ai_text,
    }
    headers = {
        'Authorization': f'Bearer {ai_token}',
        'Content-Type': 'application/json'
    }
    url = ai_url.strip() + ai_query.strip()
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            dirs = os.path.dirname(abspath)
            os.makedirs(dirs, exist_ok=True)
            with open(abspath, 'wb') as f:
                f.write(response.content)
                return True
    except Exception as e:
        print(f'\nError:\n\t{e}')
        return False
    
    return False


class BTT_to_speech(bpy.types.Operator):
    bl_label = "To Speech"
    bl_idname = "btt.to_speech"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        strip = btt_get_strip_active()
        if strip:
            btt_from_text('speech', strip)
        return {"FINISHED"}


class BTT_to_image(bpy.types.Operator):
    bl_label = "To Image"
    bl_idname = "btt.to_image"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        strip = btt_get_strip_active()
        if strip:
            btt_from_text('image', strip)
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
    bpy.utils.register_class(BTT_menu)
    bpy.types.SEQUENCER_MT_editor_menus.append(menu_func)


def unregister():
    bpy.utils.unregister_class(BTT_to_speech)
    bpy.utils.unregister_class(BTT_to_image)
    bpy.utils.unregister_class(BTT_menu)
    bpy.types.SEQUENCER_MT_editor_menus.remove(menu_func)


if __name__ == "__main__":
    register()
