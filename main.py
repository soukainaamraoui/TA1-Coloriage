from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from functools import partial
from kivy.uix.image import Image
from kivy.uix.splitter import Splitter
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup


class ColorWidget(Widget):

    #Définition des actions sur la zone de dessin (affichage d'une ligne suivant le mouvement
    # du pointeur, la couleur de la ligne est défini par la variable globale color-choice
    global color_choice, d
    color_choice = (1, 1, 1)
    d = 15

    def on_touch_down(self, touch):
        if touch.x < 100+d:     #Permert de ne pas colorier en dehors de la zone de dessin
            pass
        else:
            with self.canvas:
                (a, b, c) = color_choice
                Color(a, b, c)
                Ellipse(pos=(touch.x - int(d / 2), touch.y - int(d / 2)), size=(d, d))
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=d)

    def on_touch_move(self, touch):
        if touch.x < 100+d:
            pass
        else:
            touch.ud['line'].points += [touch.x, touch.y]


class ColorApp(App):


    def set_color(self, color, *largs):
        #Change la couleur du pinceau
        global color_choice
        color_choice = color

    def clear_canvas(self, *largs):
        #Efface la zone de dessin
        self.dessin.canvas.clear()

    def on_value(self, instance, size):
        #Mise à jour de l'affichage de la taille du pinceau
        self.lbl.text = 'size = ' + str(int(size))
        global d
        d = size

    def build(self):
        #Définition de la zone de dessin
        self.dessin = dessin = ColorWidget()

        #Slider pour définir la taille du pinceau
        sld = Slider(min=5, max=50, value=15)
        sld.fbind('value', self.on_value)
        self.lbl= lbl = Label(text='size = {}'.format(sld.value))

        #Définition de la zone de dessin, les fonctions update permettent d'adapter le coloriage
        # à la taille de la fenêtre
        dessin.bind(size=self._update_rect, pos=self._update_rect)
        with dessin.canvas.before:
            Color(1, 1, 1)
            self.fond = Rectangle(size=dessin.size, pos=dessin.pos)

        with dessin.canvas.after:
            self.rect = Image(source = 'link.png')  # l'image doit être dans le dossier du main

        #Définition du panel
        panel = BoxLayout(orientation='vertical', size_hint=(None, 1))
        palette = GridLayout(cols=2, size_hint_y=4)

        btn1 = Button(text='Clear')
        btn1.bind(on_release=partial(self.clear_canvas))

        panel.add_widget(btn1)
        panel.add_widget(self.lbl)
        panel.add_widget(sld)

        #Splitter pour séparer le dessin du panel
        splitter = Splitter(sizable_from='right', size_hint=(None, 1))
        splitter.strip_size = '5pt'
        splitter.add_widget(panel)
        splitter.min_size = panel.width
        splitter.max_size = panel.width

        #Pallette de couleur
        for choice in (('crtte', (0.96, 0.4, 0.1)), ('red', (0.85, 0, 0.08)),
                       ('mron', (0.53, 0.26, 0.11)), ('pink', (1, 0.42, 0.62)),
                       ('beige', (0.78, 0.67, 0.50)), ('FUSH', (0.86, 0, 0.45)),
                       ('safra', (0.95, 0.84, 0.09)), ('violet', (0.475, 0.11, 0.97)),
                       ('LIME', (0.62, 0.99, 0.22)), ('blue', (0.06, 0.20, 0.65)),
                       ('green', (0, 0.8, 0.3)), ('blue', (0.15, 0.769, 0.93)),
                       ('btll', (0.04, 0.42, 0.04)), ('GRS', (0.5, 0.5, 0.5)),
                       ('blc', (1, 1, 1)), ('nr', (0, 0, 0))):
            button = Button(background_normal='',
                            background_color=[choice[1][0], choice[1][1], choice[1][2], 1])
            button.bind(on_release=partial(self.set_color, choice[1]))
            palette.add_widget(button)

        panel.add_widget(palette)

        root = BoxLayout(orientation='horizontal')
        root.add_widget(splitter)
        root.add_widget(self.dessin)

        return root

    def _update_rect(self, instance, value):
        #Adapte la taille du coloriage à la taille de la fenêtre
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        self.fond.pos = instance.pos
        self.fond.size = instance.size

if __name__ == '__main__':
    ColorApp().run()
