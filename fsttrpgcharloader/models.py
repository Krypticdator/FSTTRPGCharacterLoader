import aws
class JsonListOfActors(object):
    def __init__(self):
        super(JsonListOfActors, self).__init__()
        self.actors = dict()

    def load(self, actor_role):
        json = aws.get_aws_character_list(actor_role)
        for actor in json:
            name = str(actor['name'])
            attributes = dict()
            for key, value in actor.iteritems():
                attributes[str(key)] = str(value)
            self.actors[name] = attributes


        #print(str(self.actors))

    def get_name_list(self):
        names = []
        for key, value in self.actors.iteritems():
            names.append(key)
        return names