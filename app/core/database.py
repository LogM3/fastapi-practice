from app.core.singleton import SingletonMeta


class DatabaseDescriptor:
    def __init__(self) -> None:
        self.name: str | None = None

    def __set_name__(self, owner: 'Database', name: str) -> None:
        self.name = name

    def __set__(self) -> None:
        raise AttributeError()

    def __get__(self, instance: 'Database | None', owner: 'Database'):
        if not instance:
            return self
        if not getattr(instance, '_accessed', False):
            raise RuntimeError('Access only through context manager!')
        if self.name not in instance.__dict__:
            instance.__dict__[self.name] = {
                'users': {
                    1: {
                        'id': 1,
                        'username': 'maksu',
                        'is_staff': True,
                        'password': '$2b$12$gvo50zUah.LFFYWgrFCFLet67FvCxa0Vgd8Z.tEI.fZ7Gpb8T/Y66'
                    },
                    2: {
                        'id': 2,
                        'username': 'popkin',
                        'is_staff': False,
                        'password': '$2b$12$gvo50zUah.LFFYWgrFCFLet67FvCxa0Vgd8Z.tEI.fZ7Gpb8T/Y66'
                    }
                },
                'refresh': {}
            }
        return instance.__dict__[self.name]


class Database(metaclass=SingletonMeta):
    db: DatabaseDescriptor = DatabaseDescriptor()

    def __init__(self) -> None:
        self._accessed = False
        self._connections = 0

    def __enter__(self) -> DatabaseDescriptor:
        if not self._connections:
            self._accessed = True
        self._connections += 1
        print(f'Database connected! Current connections: {self._connections}')
        return self.db

    def __exit__(self, exc_type, exc, tb) -> None:
        self._connections = max(0, self._connections - 1)
        print('Database disconnected!')
        if not self._connections:
            self._accessed = False


db: Database = Database()
