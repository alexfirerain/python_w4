import sqlite3


class Crud:
    def __init__(self, db_path):
        self._connection = sqlite3.connect(db_path)
        self._cursor = self._connection.cursor()

    def __del__(self):
        """
        деструктор такой, вызывается мусорщиком по идее
        """
        print('В Питоне есть деструктор!')
        self._cursor.close()
        self._connection.close()

    def read_all(self, table_name):
        res = self._cursor.execute(
            f'SELECT * FROM {table_name}'
        ).fetchall()
        for num, name, age in res:
            print(num, name, age)

    def delete_by_id(self, table_name, id_num):
        self._cursor.execute(f'DELETE from {table_name} WHERE id={id_num}')
        self._connection.commit()

    def create(self, table_name, name, age):
        self._cursor.execute(f'INSERT INTO {table_name}(name, age) VALUES(?, ?)', (name, age))
        self._connection.commit()

    def update(self, table_name, id_num, name=None, age=None):
        self._cursor.execute(f'UPDATE {table_name} SET name="{name}", age ={age} WHERE id={id_num}')
        self._connection.commit()


db = Crud('../db/movies.sqlite')

db.delete_by_id('users', 5)
db.create('users', 'Тёмыч', 30)
db.update('users', 1, name='Толян', age=39)
db.read_all('users')
