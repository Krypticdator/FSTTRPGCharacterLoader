from __future__ import print_function
import aws

class JsonListOfActors(object):
    def __init__(self):
        super(JsonListOfActors, self).__init__()
        self.actors = dict()

    def load(self, actor_role, with_raws=False):
        json = aws.get_aws_character_list(actor_role)
        for actor in json:
            name = str(actor['name'])
            attributes = dict()
            raws = dict()
            for key, value in actor.iteritems():
                attributes[str(key)] = str(value)
                if with_raws:
                    raws[key] = value
            if with_raws:
                attributes['raws'] = raws
            self.actors[name] = attributes



    def get_name_list(self):
        names = []
        for key, value in self.actors.iteritems():
            names.append(key)
        return names

    def get_optional_value(self, actor,  valuename):
        try:
            return self.actors[actor][valuename]
        except KeyError as e:
            print('no such key as ' + valuename)
            return None