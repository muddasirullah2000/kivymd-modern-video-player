from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.metrics import sp
from kivy.uix.videoplayer import VideoPlayer, MDPiVideoPlayer
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.graphics.svg import Svg
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDIconButton, BaseButton
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.slider import MDSlider
from kivymd.uix.label import MDLabel
from kivy.uix.video import Video
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, StringProperty
from kivy.clock import Clock
from kivy.core.window import Window
from gradient import *

# registering our new custom fontstyle
LabelBase.register(name='SF-Pro', fn_regular='../Font/SF-Pro.ttf')

# Window.size = (350, 600)

Builder.load_file('piplayer.kv')

#----------- Custom Gradient -----------


#----------- ############## ------------

class PiPlayerContainer(MDBoxLayout):
    pass

class PiPlayerButtonBox(MDFloatLayout):
    video = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shader_widget = ShaderWidget(fs=GLSL_CODE)
        self.add_widget(self.shader_widget)

class PiControlsBox(MDGridLayout):
    video = ObjectProperty(None)

class PiSlideBox(MDBoxLayout):
    video = ObjectProperty(None)

class PiPlayerButtons(MDBoxLayout):
    video = ObjectProperty(None)

#----------- Custom Slider -----------

class PiProgressBarVideo(MDSlider):
    video = ObjectProperty(None)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        self._update_seek(touch.x)

    def _update_seek(self, x):
        if self.width == 0:
            return
        x = max(self.x, min(self.right, x)) - self.x
        self.video.seek(x / float(self.width))

#--------- Custom Control Buttons ---------

class PiBaseButtons(MDIconButton):
    video = ObjectProperty(None)
    theme_icon_color = "Custom"
    icon_color = "white"
    icon_size = sp(20)

class ButtonControlsLock(PiBaseButtons):
    locked = BooleanProperty(False)  # Define a Boolean property to track state

class ButtonControlsVolume(PiBaseButtons):
    volume = BooleanProperty(False)  # Define a Boolean property to track state

class ButtonRewindFiveSecondsBack(PiBaseButtons):
    pass

class ButtonRewindFiveSecondsForward(PiBaseButtons):
    pass

class ButtonRewindBack(PiBaseButtons):
    pass

class ButtonRewindForward(PiBaseButtons):
    pass

class ButtonVideoPlayPause(PiBaseButtons):
    def on_release(self, *args):
        if self.video.state == 'play':
            self.video.state = 'pause'
        else:
            self.video.state = 'play'

class ButtonDawnload(PiBaseButtons):
    pass

class ButtonExitAndFullScreen(PiBaseButtons):
    pass

class PiVideoPlayer(Video):
    '''Implement a custom video player.'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_time(self):
        '''Set the timeline of the current playback with start and end times'''
        
        seek = self.position / self.duration
        elapsed_time = self.duration * seek
        remaining_time = self.duration - elapsed_time

        # Calculate hours, minutes, seconds for elapsed (start) time
        start_hours = int(elapsed_time // 3600)
        start_minutes = int((elapsed_time % 3600) // 60)
        start_seconds = int(elapsed_time % 60)

        # Calculate hours, minutes, seconds for remaining (end) time
        end_hours = int(remaining_time // 3600)
        end_minutes = int((remaining_time % 3600) // 60)
        end_seconds = int(remaining_time % 60)

        # Update start_time and end_time labels
        self.ids.button_box.ids.start_time.text = "%02d:%02d:%02d" % (start_hours, start_minutes, start_seconds)
        self.ids.button_box.ids.end_time.text = "%02d:%02d:%02d" % (end_hours, end_minutes, end_seconds)

    def get_duration(self, *args):
        # get duration, not available until video is loaded
        duration = self.duration

    def rewind_5s(self):
        new_position = max((self.position - 5)/self.duration, 0)
        self.seek(new_position)

    def forward_5s(self):
        new_position = min((self.position + 5)/self.duration, 1)
        self.seek(new_position)


class MainApp(MDApp):
    title = "Pi Video Player"

    def build(self):
        # container = PiPlayerContainer()
        player = PiVideoPlayer(
            source="videos/Marvel_Studios_Doctor_Strange_Trailer.mp4",
            state='play',
            options={'allow_stretch': True},
            allow_stretch=True,
            volume=0.1,
            keep_ratio=False,
        )
        # container.add_widget(player)
        return player

if __name__ == '__main__':
    MainApp().run()














""" TypeError: Properties ['height_factor'] passed to __init__ may not be existing property names. Valid properties are ['_background_origin', '_background_x',
 '_background_y', '_md_bg_color', '_origin_line_color', '_origin_md_bg_color', 'adaptive_height', 'adaptive_size', 'adaptive_width', 'angle', 'background',
   'background_hue', 'background_origin', 'background_palette', 'center', 'center_x', 'center_y', 'children', 'cls', 'device_ios', 'disabled', 'height', 'id',
     'ids', 'line_color', 'line_width', 'md_bg_color', 'motion_filter', 'opacity', 'opposite_colors', 'parent', 'pos', 'pos_hint', 'radius', 'right', 'size',
       'size_hint', 'size_hint_max', 'size_hint_max_x', 'size_hint_max_y', 'size_hint_min', 'size_hint_min_x',
 'size_hint_min_y', 'size_hint_x', 'size_hint_y', 'specific_secondary_text_color', 'specific_text_color', 'theme_cls', 'top', 'widget_style', 'width', 'x', 'y']"""