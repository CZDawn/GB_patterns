from copy import deepcopy
from sqlite3 import connect
from quopri import decodestring
from .behavioral_patterns import FileWriter, AbstractSubject
from .architectural_system_pattern_unit_of_work import DomainObject


class User:

    def __init__(self, name, surname, email=None, pseudonym=None, profession=None):
        self.name = name
        self.surname = surname
        self.email = email
        self.pseudonym = pseudonym
        self.profession = profession


class Author(User):

    def __init__(self, name,surname,  pseudonym):
        self.pseudonym = pseudonym
        super().__init__(name, surname, self.pseudonym)


class Speaker(User):

    def __init__(self, name, surname, profession):
        self.profession = profession
        super().__init__(name, surname, self.profession)


class Listener(User, DomainObject):

    def __init__(self, name, surname, email):
        self.podcasts = []
        super().__init__(name, surname, email)


class UserFactory:
    types = {
        'listener': Listener,
        'speaker': Speaker,
        'author': Author
    }

    @classmethod
    def create(cls, type_, name, surname, email=None, pseudonym=None, profession=None):
        if type_ == 'listener':
            return cls.types[type_](name, surname, email)
        elif type_ == 'speaker':
            return cls.types[type_](name, surname, profession)
        else:
            return cls.types[type_](name, surname, pseudonym)


class PodcastPrototype:

    def clone(self):
        return deepcopy(self)


class Podcast(PodcastPrototype, AbstractSubject):

    def __init__(self, name, category, theme, author):
        self.name = name
        self.category = category
        self.theme = theme
        self.author = author
        self.category.podcasts.append(self)
        self.theme.podcasts.append(self)
        self.listeners = []
        super().__init__()

    def __getitem__(self, item):
        return self.listeners[item]

    def add_listener(self, listener: Listener):
        self.listeners.append(listener)
        listener.podcasts.append(self)
        self.notify()


class BroadcastPodcast(Podcast):
    pass


class RecordedPodcast(Podcast):
    pass


class PodcastFactory:
    types = {
        'broadcast': BroadcastPodcast,
        'recorded': RecordedPodcast
    }

    @classmethod
    def create(cls, type_, name, category, theme, author):
        return cls.types[type_](name, category, theme, author)


class Category:
    auto_id = 0

    def __init__(self, name):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name  = name
        self.themes = []
        self.podcasts = []

    def themes_count(self):
        return len(self.themes)

    def podcast_count(self):
        return round(len(self.podcasts) / 2)


class Theme:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Theme.auto_id
        Theme.auto_id += 1
        self.name = name
        self.category = category
        self.podcasts = []

    def podcast_count(self):
        return round(len(self.podcasts) * 2)


class Engine:

    def __init__(self):
        self.speakers = []
        self.listeners = []
        self.categories = []
        self.themes = []
        self.podcasts = []

    @staticmethod
    def create_user(type_, name, surname, email=None, pseudonym=None, profession=None):
        return UserFactory.create(type_, name, surname, email=None, pseudonym=None, profession=None)

    @staticmethod
    def create_category(name):
        return Category(name)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item

    def find_category_by_name(self, name):
        for item in self.categories:
            print('item', item.name)
            if item.name == name:
                return item

    @staticmethod
    def create_theme(name, category):
        return Theme(name, category)

    def find_theme_by_id(self, id):
        for item in self.themes:
            print('item', item.id)
            if item.id == id:
                return item

    def find_theme_by_name(self, name):
        for item in self.themes:
            print('item', item.name)
            if item.name == name:
                return item

    @staticmethod
    def create_podcast(type_, name, category, theme, author):
        return PodcastFactory.create(type_, name, category, theme, author)

    def find_podcast_by_name(self, name):
        for item in self.podcasts:
            if item.name == name:
                return item

    def find_listener_by_name(self, name) -> Listener:
        for item in self.listeners:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)


class ListenerMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'listener'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, surname, email = item
            listener = Listener(name, surname, email)
            listener.id = id
            result.append(listener)
        return result

    def find_by_id(self, id):
        statement = f'SELECT id, name FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Listener(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f'UPDATE {self.tablename} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CategoryMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'category'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            category = Category(name)
            category.id = id
            result.append(category)
        return result

    def find_by_id(self, id):
        statement = f'SELECT id, name FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Category(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f'UPDATE {self.tablename} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = connect('patterns.sqlite')


class MapperRegistry:
    mappers = {
        'listener': ListenerMapper,
        'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Listener):
            return ListenerMapper(connection)
        elif isinstance(obj, Cattegory):
            return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')

