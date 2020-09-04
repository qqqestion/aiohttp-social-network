import re
import bcrypt
from . import db


async def validate_registration(db_engine, form):
    try:
        email = form['login']
        first_name, last_name = form['first_name'], form['last_name']
        password, password_confirmation = form['password'], form['password_confirmation']
    except KeyError:
        return
    if not re.match(r'[\w\.]+@\w+\.\w+', email):  # email validation
        return
    if password != password_confirmation:
        return
    async with db_engine.acquire() as conn:
        email_query = db.users.select().where(db.users.c.email == email)
        ret = await conn.execute(email_query)
        if ret.rowcount:
            return
    return {'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')}


def validate_post(title, content):
    return title is not None and content is not None \
        and isinstance(title, str) and isinstance(content, str)
