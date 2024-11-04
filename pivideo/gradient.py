from kivy.app import runTouchApp
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.graphics import RenderContext
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

Builder.load_string(r'''
<ShaderWidget>:
    canvas:
        Rectangle:
            pos: self.pos
            size: self.size
''')

class ShaderWidget(MDBoxLayout):
    fs = StringProperty(None)

    def __init__(self, **kwargs):
        self.canvas = RenderContext(
            use_parent_projection=True,
            use_parent_modelview=True,
            use_parent_frag_modelview=True)
        super().__init__(**kwargs)
        self.md_bg_color = (0, 0, 0, 0)  # Set background color to transparent

    def on_fs(self, _, value):
        shader = self.canvas.shader
        old_value = shader.fs
        shader.fs = value
        if not shader.success:
            shader.fs = old_value
            raise Exception('Failed to compile GLSL.')

    def on_size(self, _, size):
        self.canvas['resolution'] = [float(size[0]), float(size[1])]

# GLSL code for a vertical gradient from top (alpha=0) to bottom (alpha=0.3)
GLSL_CODE = '''
uniform vec2 resolution;
void main(void)
{
    float sy = gl_FragCoord.y / resolution.y;
    float alpha = mix(0.7, 0.0, sy);  // Interpolates alpha from 0 to 0.3
    gl_FragColor = vec4(0.0, 0.0, 0.0, alpha);  // Green color with varying alpha
}
'''

class MyApp(MDApp):
    def build(self):
        root = ShaderWidget(fs=GLSL_CODE)
        return root

if __name__ == '__main__':
    MyApp().run()