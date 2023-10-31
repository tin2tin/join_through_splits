bl_info = {
    "name": "Join Through Splits",
    "author": "tintwotin",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Strip > Join Trough Strips",
    "description": "Join adjacent strips",
    "warning": "",
    "doc_url": "",
    "category": "Sequencer",
}

import bpy


def join(vse, current_strip, next_strip):
    # Calculate the duration of the next strip
    duration = next_strip.frame_final_end - next_strip.frame_final_start

    # Remove the next strip from the VSE
    vse.sequences.remove(next_strip)

    # Extend the current strip with the duration of the next strip
    current_strip.frame_final_end += duration


class SEQUENCER_OT_join_strips(bpy.types.Operator):
    """Join adjacent strips"""
    bl_idname = "sequencer.join_strips"
    bl_label = " Join Through Splits"

    @classmethod
    def poll(cls, context):
        return context.scene.sequence_editor and context.selected_sequences


    def execute(self, context):
        vse = context.scene.sequence_editor

        # Define a set of strip types that can be joined
        join_strip_types = {"MOVIE", "SOUND", "SCENE", "IMAGE"}

        # Iterate through the selected sequences
        for current_strip in context.selected_sequences:
            # Iterate through all sequences in the VSE
            for next_strip in context.selected_sequences:
                # Check if the strips are on the same channel and if they're the same type.
                if (
                    current_strip.channel == next_strip.channel
                    and current_strip.type == next_strip.type
                ):
                    # Check if the end frame of the current strip matches the start frame of the next strip.
                    if current_strip.frame_final_end == next_strip.frame_final_start:
                        # Check if both the current and next strip types are in the set of joinable strip types
                        if (
                            current_strip.type in join_strip_types
                            and next_strip.type in join_strip_types
                        ):
                            # If the start frame of the current strip matches the start frame of the next strip, join them
                            if current_strip.frame_start == next_strip.frame_start:
                                join(vse, current_strip, next_strip)
                        # If not within the joinable strip types, just join them.
                        else:
                            join(vse, current_strip, next_strip)
        return {"FINISHED"}


def draw_func(self, context):
    layout = self.layout
    layout.operator("sequencer.join_strips")


def register():
    bpy.utils.register_class(SEQUENCER_OT_join_strips)
    bpy.types.SEQUENCER_MT_strip.append(draw_func)


def unregister():
    bpy.utils.unregister_class(SEQUENCER_OT_join_strips)
    bpy.types.SEQUENCER_MT_strip.remove(draw_func)


if __name__ == "__main__":
    register()
