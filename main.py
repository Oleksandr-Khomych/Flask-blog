import os
from app import app
import view


def create_db():
    '''Функція для створення таблиць БД'''
    db = view.connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


if __name__ == '__main__':
    app.config.update(dict(DATABASE=os.path.join(app.root_path, 'database.db')))
    # create_db()
    app.run(debug=True)
