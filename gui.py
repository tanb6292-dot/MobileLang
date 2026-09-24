import sys
import io
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from main import MobileLangV3

class MobileLangIDE(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        # Header Title
        self.add_widget(Label(text="📱 MobileLang Engine IDE V3", size_hint_y=None, height=40, font_size='20sp', bold=True))

        # Code Editor Input
        self.code_input = TextInput(
            text='set name = "Mobile Developer"\nprint "Hello, " + name\nnotify "Welcome to MobileLang App!"\nvibrate 200',
            multiline=True,
            size_hint_y=0.5,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1),
            font_size='16sp'
        )
        self.add_widget(self.code_input)

        # Run Button
        self.run_btn = Button(text="▶ RUN SCRIPT", size_hint_y=None, height=50, background_color=(0.2, 0.7, 0.3, 1), bold=True)
        self.run_btn.bind(on_press=self.run_code)
        self.add_widget(self.run_btn)

        # Terminal Output Area
        self.output_label = Label(text="Output will appear here...", size_hint_y=None, font_size='14sp', color=(0.8, 0.8, 0.8, 1))
        self.output_label.bind(texture_size=self.output_label.setter('size'))

        scroll = ScrollView(size_hint_y=0.4)
        scroll.add_widget(self.output_label)
        self.add_widget(scroll)

    def run_code(self, instance):
        code = self.code_input.text
        engine = MobileLangV3()

        # Capture print outputs
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        try:
            engine.execute(code)
            sys.stdout = old_stdout
            self.output_label.text = redirected_output.getvalue()
        except Exception as e:
            sys.stdout = old_stdout
            self.output_label.text = f"❌ Execution Error: {e}"

class MobileLangApp(App):
    def build(self):
        return MobileLangIDE()

if __name__ == '__main__':
    MobileLangApp().run()
