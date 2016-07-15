from peewee import Model, SqliteDatabase, CharField, DoesNotExist

actor_db = SqliteDatabase(None)
file_locations = SqliteDatabase('filepaths.db')


class ActorDBFilepath(Model):
    name = CharField(unique=True)
    filepath = CharField(unique=True)

    @staticmethod
    def add_or_modify(name, filepath):
        f, created = ActorDBFilepath.get_or_create(name=name, defaults={'filepath': filepath})

        if created:
            print('created new filepath')
        else:
            f.filepath = filepath
            f.save()
        return f

    @staticmethod
    def get_filepath(name):
        try:
            return ActorDBFilepath.get(ActorDBFilepath.name == name)
        except DoesNotExist:
            print('filepath doesnt exist')
            return None

    class Meta:
        database = file_locations


class Actor(Model):
    name = CharField(unique=True)
    role = CharField()

    @staticmethod
    def add_or_get(role, name):
        actor, created = Actor.get_or_create(role=role, name=name)
        if created:
            print('created new actor')
        else:
            pass
        return actor

    @staticmethod
    def get_all():
        return Actor.select()

    @staticmethod
    def get_all_with_role(role):
        return Actor.select().where(Actor.role == role)

    class Meta:
        database = actor_db


class DBManager(object):
    def __init__(self, actor_db_filepath=None):
        super(DBManager, self).__init__()
        file_locations.connect()
        file_locations.create_tables([ActorDBFilepath], safe=True)
        self.filepaths = ActorDBFilepath()

        if actor_db_filepath:

            actor_db.init(actor_db_filepath)
            self.filepaths.add_or_modify('actors_location', actor_db_filepath)
        else:
            f = self.filepaths.get_filepath('actors_location')
            if f:
                actor_db.init(f.filepath)
        actor_location = self.filepaths.get_filepath('actors_location')
        if actor_location:
            print('saving actors to location: ' + actor_location.filepath)
        else:
            actor_db.init('actors.db')
            self.filepaths.add_or_modify('actors_location', 'actors.db')

        actor_db.connect()
        actor_db.create_tables([Actor], safe=True)
        self.actors = Actor()

    def __del__(self):
        if actor_db:
            actor_db.close()
        if file_locations:
            file_locations.close()
