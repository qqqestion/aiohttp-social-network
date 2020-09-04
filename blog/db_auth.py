from aiohttp_security.abc import AbstractAuthorizationPolicy

import bcrypt

import sqlalchemy as sa

from . import db


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):

    def __init__(self, dbengine):
        self.dbengine = dbengine

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False

        async with self.dbengine.acquire() as conn:
            where = sa.and_(db.users.c.email == identity,
                            sa.not_(db.users.c.is_deleteds))
            query = db.users.select().where(where)
            ret = await conn.execute(query)
            user = await ret.fetchone()
            if user is not None:
                user_id = user[0]
                is_superuser = user[5]
                if is_superuser:
                    return True

                where = db.permissions.c.user_id == user_id
                query = db.permissions.select().where(where)
                ret = await conn.execute(query)
                result = await ret.fetchall()
                if ret is not None:
                    for record in result:
                        if record.perm_name == permission:
                            return True

            return False

    async def authorized_userid(self, identity):
        async with self.dbengine.acquire() as conn:
            where = sa.and_(db.users.c.id == int(identity),
                            sa.not_(db.users.c.is_deleted))
            query = db.users.count().where(where)
            ret = await conn.scalar(query)
            if ret:
                return identity
            else:
                return None


async def check_credentials(db_engine, email, password):
    async with db_engine.acquire() as conn:
        where = sa.and_(db.users.c.email == email,
                        sa.not_(db.users.c.is_deleted))
        query = db.users.select().where(where)
        ret = await conn.execute(query)
        user = await ret.fetchone()
        if user is not None:
            hashed = user[4]
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    return False


async def authenticate(db_engine, email, password):
    async with db_engine.acquire() as conn:
        where = sa.and_(db.users.c.email == email,
                        sa.not_(db.users.c.is_deleted))
        query = db.users.select().where(where)
        ret = await conn.execute(query)
        user = await ret.fetchone()
        if user is not None:
            hashed = user[4]
            if bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')):
                return db.parse_columns(db.users, user)
