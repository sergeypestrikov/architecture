from threading import local


# Unit of Work the Архитектурный системный паттерн
class UnitOfWork:
    '''
    Паттерн Unit of Work
    '''
    # Который работает с конкретным потоком
    current = local()

    def __init__(self):
        self.new_obj = []
        self.dirty_obj = []
        self.deleted_obj = []

    def set_mapper_registry(self, MapperRegistry):
        self.MapperRegistry = MapperRegistry

    def new_register(self, obj):
        self.new_obj.append(obj)

    def dirty_register(self, obj):
        self.dirty_obj.append(obj)

    def deleted_register(self, obj):
        self.deleted_obj.append(obj)

    def commit(self):
        self.new_insert()
        self.dirty_update()
        self.deleted_del()

        self.new_obj.clear()
        self.dirty_obj.clear()
        self.deleted_obj.clear()

    def new_insert(self):
        print(self.new_obj)
        for obj in self.new_obj:
            print(f'Вывод {self.MapperRegistry}')
            self.MapperRegistry.get_mapper(obj).insert(obj)

    def dirty_update(self):
        for obj in self.dirty_obj:
            self.MapperRegistry.get_mapper(obj).update(obj)

    def deleted_del(self):
        for obj in self.deleted_obj:
            self.MapperRegistry.get_mapper(obj).delete(obj)


    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:
    def new_mark(self):
        UnitOfWork.get_current().new_register(self)

    def dirty_mark(self):
        UnitOfWork.get_current().dirty_register(self)

    def deleted_mark(self):
        UnitOfWork.get_current().deleted_register(self)