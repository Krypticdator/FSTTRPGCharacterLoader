from __future__ import print_function
from traits.api import *
from traitsui.api import *
import aws


from models import JsonListOfActors

list_of_actors = JsonListOfActors()

class Loader(HasTraits):

    role = Enum('NPC', 'PC', 'INPC')
    selection = String()

    choose_character = ListStr(editor=ListStrEditor(selected='selection'))
    load = Button()
    choose = Button()
    chosen = Dict()
    view = View(
        Item('role'),
        Item('load', show_label=False),
        Item('choose_character'),
        Item('choose'),
        Item('chosen')
    )

    def _choose_fired(self):
        self.chosen = list_of_actors.actors[self.selection]
        print(self.chosen['name'])


    def _load_fired(self):
        list_of_actors.load(self.role)
        self.choose_character = list_of_actors.get_name_list()

if __name__ == '__main__':
    l = Loader()
    l.configure_traits()