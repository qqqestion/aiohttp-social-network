from aiohttp import web

from aiohttp_session import setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

import base64
from cryptography import fernet

import aiohttp_jinja2
import jinja2

from aiohttp_security import setup as setup_security
from aiohttp_security import SessionIdentityPolicy

from aiopg.sa import create_engine
from aiopg import create_pool

from .routes import setup_routes
from . import settings
from .db_auth import DBAuthorizationPolicy


async def create_app():
    app = web.Application()
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('blog', 'templates')
    )
    app['db'] = await create_engine(dsn=settings.DATABASE)

    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup_session(app, EncryptedCookieStorage(secret_key))
    setup_security(app, SessionIdentityPolicy(), DBAuthorizationPolicy(app['db']))

    app.router.add_static('/blog/static/',
                          path=str('blog/static'),
                          name='static')
    app['static_root_url'] = '/blog/static'

    setup_routes(app)
    return app
