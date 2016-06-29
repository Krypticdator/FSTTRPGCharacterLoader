from __future__ import print_function

from traits.api import *
from traitsui.api import *

from models import JsonListOfActors

list_of_actors = JsonListOfActors()


class Name(HasTraits):
    name = String()
    change_listener = Method()
    view = View(
        Item('name')
    )

    def _name_changed(self):
        self.change_listener()



class Loader(HasTraits):

    role = Enum('NPC', 'PC', 'INPC')
    selection = String()
    name_field = Instance(Name)

    choose_character = ListStr(editor=ListStrEditor(selected='selection'))
    load = Button()
    choose = Button()
    chosen = Dict()
    view = View(
        Item('role'),
        Item('load', show_label=False),
        Item('choose_character'),
        Item('choose'),
        Item('chosen', style='custom')
    )

    def _choose_fired(self):
        self.chosen = list_of_actors.actors[self.selection]
        self.name_field.name = self.selection



    def _load_fired(self):
        list_of_actors.load(self.role)
        self.choose_character = list_of_actors.get_name_list()

class CharacterName(HasTraits):
    role = Enum('NPC', 'PC', 'INPC')
    name = Instance(Name, ())
    loader = Instance(Loader)
    name_change_handler = Method()


    view = View(
        HGroup(
            Item('role'),
            Item('name', style='custom', show_label=False),
            Item('loader', show_label=False)
        )
    )

    def _loader_default(self):
        return Loader(name_field=self.name)

    def _name_default(self):
        return Name(change_listener=self.name_change_handler)
        # n.master = self.load_handler

    def _name_changed(self):
        print('hello')


class Foo(object):
    def bar(self):
        print('foobar')

if __name__ == '__main__':
    f = Foo()
    c = CharacterName(name_change_handler=f.bar)

    c.configure_traits()