from kivymd.app import MDApp
from kivymd.uix.screen import Screen, MDScreen
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextFieldRound
from kivymd.uix.button import MDIconButton, MDFillRoundFlatIconButton, MDFloatingActionButton
from kivymd.uix.floatlayout import MDFloatLayout

from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Rectangle, Line, Color, RoundedRectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation

from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.datatables import MDDataTable

import random
from enum import Enum

'''
    NOTE:
    - Add payment Layout (balance and service)
    - enable scrolling in limited space


'''
pos_center = { "center_x": .5, "center_y": .5 }
Window.size = (300, 500)
class colorPallete:
    white = (242/255, 242/255, 242/255, 1)
    light_gray = (191/255, 191/255, 191/255, 1)
    gray = [140/255, 140/255, 140/255, 1]
    dark_gray = (63/255, 63/255, 63/255, 1)
    black = (12/255, 12/255, 12/255, 1)
    transparent = [0,0,0.1,0]

    white_transparent = (242/255, 242/255, 242/255, .17)

class SearchBar(MDTextFieldRound):
    def __init__(self, **kwargs):
        textFieldConfig = { 
            "normal_color": colorPallete.gray,
            "color_active": colorPallete.light_gray,
            "pos_hint": { "center_y": .5, "center_x": .5},
            "size_hint": (.7,.6)
        }
        super().__init__(**textFieldConfig)

class SearchButton(MDIconButton):
    def __init__(self, **kwargs):
        config = { 
            "icon": 'magnify', 
            "pos_hint": {"center_x": 0, "center_y": .5},
            "theme_text_color": "Custom",
            "text_color": colorPallete.white,
        }
        super().__init__(**config)

class SearchLayout(GridLayout):
    def __init__(self, **kwargs):
        config = {
            "size_hint_y": None,
            "height": 50,
            "cols": 2
        }
        super().__init__(**config)
        bar_screen = MDScreen(
            size_hint_x=None, 
            size=(7* Window.size[0]/8, 50)
        )
        bar_screen.add_widget(SearchBar())
        self.add_widget(bar_screen)

        button_screen = MDScreen()
        button_screen.add_widget(SearchButton())
        self.add_widget(button_screen)

class PaymentLayout(GridLayout):
    def __init__(self):
        config = {
            "size_hint_y": None,
            "height": 70,
            "cols": 2
        }
        super().__init__(**config)
        self.add_widget(self.currentBalance())
        self.add_widget(self.paymentService())

    def currentBalance(self):
        padding = [ dp(30), dp(0), dp(0), dp(0)]
        gl = GridLayout(cols=1, size_hint_x=.8, padding=padding)
        title_text = MDLabel(
            text="Your Balance", 
            pos_hint={"center_y": .3},
            font_style="Subtitle2",
            font_size=10,
            theme_text_color= "Custom",
            text_color= colorPallete.white,
        )
        title = MDScreen()
        title.add_widget(title_text)

        balance_text = MDLabel(
            text="100.000", 
            pos_hint={"center_y": .8}, 
            font_style="H6",
            font_size=100,
            theme_text_color= "Custom",
            text_color= colorPallete.white,
        )
        balance = MDScreen()
        balance.add_widget(balance_text)

        gl.add_widget(title)
        gl.add_widget(balance)
        return gl

    def paymentService(self):
        padding = [ dp(20), dp(0)]
        gl = GridLayout(cols=3, padding=padding,  size_hint_x=1.2)
        iconList = [
            ("account", "Akun", .3),
            ("bag-checked", "Top-up", .4),
            ("book-account", "Rekam", .5)
        ]
        for icon, text, trans in iconList:
            btnScreen = MDScreen()
            btnScreen.add_widget(MDIconButton(
                icon=icon,pos_hint={"center_y": .6, "center_x": .5},
                text_color=colorPallete.white,
                theme_text_color="Custom",
            ))
            btnScreen.add_widget(MDLabel(
                text=text,
                halign="center",
                pos_hint={"center_y": .3},
                font_style="Caption",
                theme_text_color= "Custom",
                text_color= colorPallete.white,
            ))
            gl.add_widget(btnScreen)
        return gl

class NewsLayout(MDScreen):
    def __init__(self, number):
        config = {
            "size_hint_y": None,
            "md_bg_color": colorPallete.gray,
            "height": 200,
            # "padding": padding
        }
        super().__init__(**config)
        self.add_widget(MDLabel(text="Berita {}".format(number), halign='center'))


class MainScreenDivision(MDScreen):
    def __init__(self, size):
        config = {}
        super().__init__(**config)
        mainScrollView = ScrollView()
        gl = GridLayout(cols=1, size_hint_y=None, spacing=5)
        gl.add_widget(SearchLayout())
        if size == "large":
            gl.add_widget(PaymentLayout())
            for i in range(3):
                gl.add_widget(NewsLayout(i))
        # gl.bind(minimum_height=gl.setter('height'))
        mainScrollView.add_widget(gl)
        self.add_widget(mainScrollView)

class MainScreen(MDScreen):
    '''
    Main screen that contains all information regarding the app
    such as news and payment
    '''
    def __init__(self, **kwargs):
        config = {
            "radius": [10, 10, 0, 0],
            "md_bg_color": colorPallete.dark_gray,
            "pos_hint": {"center_x": .5, "center_y": .1},
            "on_touch_up": self.swipe,
            "on_touch_down": self.registerTouchPos,
            "size_hint": (None, None),
            "size": (300, 200)
        }
        super().__init__(**config)
        self.touch_post = 0
        self.innerLayoutSmall = MainScreenDivision("small")
        self.innerLayoutLarge = MainScreenDivision("large")
        self.state = "small"
        
        
    def registerTouchPos(self, instance, touch):
        self.touch_post = touch.y


    def swipe(self, instance, touch):
        if touch.y < self.touch_post:
            animation = Animation(size=(300, 200), duration=.4)
            animation.start(instance)
            try:
                self.remove_widget(self.innerLayoutLarge)
                self.add_widget(self.innerLayoutSmall)
                self.state = "small"
            except:
                pass
        elif touch.y > self.touch_post:
            animation = Animation(size=(300, 800), duration=.4)
            animation.start(instance)
            try:
                self.remove_widget(self.innerLayoutSmall)
                self.add_widget(self.innerLayoutLarge)
                self.state = "large"
            except:
                pass
        else:
            pass

class ToolbarFloatLayout(FloatLayout):
    '''
    Lower toolbar that can be expanded to show all available service
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        mainScreen = MDScreen(
            md_bg_color=colorPallete.light_gray, size_hint=(.75, .12),
            pos_hint={'center_x':.5, 'top': .15},
            radius= [25, 25, 25, 25],
        )
        gll = GridLayout(cols=4)
        for icon in ["map-check", "mastodon", "mushroom", "target-account"]:
            sc = Screen()
            sc.add_widget(MDIconButton(icon=icon, pos_hint={"center_x": .5, "center_y": .5}))
            gll.add_widget(sc)
        mainScreen.add_widget(gll)
        self.add_widget(mainScreen)


class HBoxLayoutExample(MDApp):
    """
    Horizontally oriented BoxLayout example class
    """
    #----------------------------------------------------------------------

    def buildButton(self, icon, pos_hint={"center_x": .5, "center_y": .5}, text='', isTransparent=False):
        screenIcon = MDScreen(md_bg_color=colorPallete.black)
        bg_color = colorPallete.white_transparent if isTransparent else colorPallete.transparent
        screenIconConfig = {
            "icon": icon,
            "text": text,
            "pos_hint": pos_hint,
            "theme_text_color": "Custom",
            "text_color": colorPallete.white,
            "md_bg_color": bg_color,
            "line_color": colorPallete.transparent,
            "icon_color": colorPallete.white,
            "font_size": dp(10)
        }
        screenIcon.add_widget(MDFillRoundFlatIconButton(**screenIconConfig))
        return screenIcon

    def bulidHeader(self, height):
        header = GridLayout(cols=3, size_hint_y= None, height=height)
        headerProp = [
            ['star', 'Promo', False],
            ['home', "Home", True],
            ['chat', "Chat", False]
        ]
        for icon, text, isTransparent in headerProp:
            iconHeader = self.buildButton(icon, text=text, isTransparent=isTransparent)
            header.add_widget(iconHeader)
        return header
    

    def buildToolbar(self):
        tfl = ToolbarFloatLayout()
        return tfl
    
    def mainFloatLayout(self):
        mfl = MainScreen()
        with mfl.canvas:
            Color(*colorPallete.light_gray)
            Rectangle(
                pos_hint={"top": .5}, 
                size=(100, 3)
            )
        
        
        return mfl

    def buildBody(self):
        screen = MDScreen(md_bg_color=colorPallete.black)
        mfl = self.mainFloatLayout()
        tfl = self.buildToolbar()
        screen.add_widget(mfl)
        screen.add_widget(tfl)
        return screen


    def build(self):
        """
        Horizontal BoxLayout example
        """
        layout = GridLayout(cols=1)
        header = self.bulidHeader(dp(50))
        layout.add_widget(header)

        layout.add_widget(self.buildBody())
        
        return layout

HBoxLayoutExample().run()