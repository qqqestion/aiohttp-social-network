from aiohttp import web
from aiohttp_jinja2 import template

from aiohttp_security import (
    remember, forget, authorized_userid,
    check_permission, check_authorized,
)

from .db_auth import check_credentials, authenticate

from . import db

from .validators import validate_registration, validate_post


@template('login.html')
async def login(request: web.Request):
    if request.method == 'POST':
        form = await request.post()
        email, password = form['login'], form['password']
        db_engine = request.app['db']
        user = await authenticate(db_engine, email, password)
        if user:
            next_page = request.query.get('next')
            if next_page:
                response = web.HTTPFound(next_page)
            else:
                response = web.HTTPFound(location=request.app.router['home'].url_for())

            await remember(request, response, str(user['id']))
        else:
            response = web.HTTPFound(location=request.app.router['login'].url_for())

        raise response
    return {}


@template('logout.html')
async def logout(request):
    await check_authorized(request)
    if request.method == 'POST':
        response = web.HTTPFound(location=request.app.router['home'].url_for())
        await forget(request, response)
        raise response
    return {}


@template('register.html')
async def register(request):
    if request.method == 'POST':
        form = await request.post()
        db_engine = request.app['db']
        user = await validate_registration(db_engine, form)
        if user:
            # print(f'User valid: {user}')
            async with db_engine.acquire() as conn:
                user_query = db.users.insert().values(**user)
                ret = await conn.execute(user_query)
                user_id = (await ret.fetchone())[0]
                response = web.HTTPFound(location=request.app.router['home'].url_for())
                await remember(request, response, str(user_id))
            raise response
        raise web.HTTPFound(location=request.app.router['register'].url_for())
    return {}


@template('post_list.html')
async def post_list(request):
    db_engine = request.app['db']
    async with db_engine.acquire() as conn:
        post_query = db.posts.select()
        ret = await conn.execute(post_query)
        raw_posts = await ret.fetchall()
        posts = []
        for post in raw_posts:
            user_query = db.users.select().where(db.users.c.id == post[1])
            ret = await conn.execute(user_query)
            user = await ret.fetchone()
            cleaned_post = db.parse_columns(db.posts, post)
            cleaned_post['user'] = f'{user[1]} {user[2]}'
            cleaned_post['user_img'] = user[7]
            posts.append(cleaned_post)

    return {'posts': posts}


@template('post_form.html')
async def post_form(request: web.Request):
    await check_authorized(request)
    if request.method == 'POST':
        form = await request.post()
        title, content = form.get('title'), form.get('post_content')
        if validate_post(title, content):
            user_id = int(await authorized_userid(request))
            async with request.app['db'].acquire() as conn:
                post_query = db.posts.insert().values(user_id=user_id, title=title, content=content)
                ret = await conn.execute(post_query)
                post_id = (await ret.fetchone())[0]
                response = web.HTTPFound(location=request.app.router['post-detail'].url_for(post_id=str(post_id)))
        else:
            response = web.HTTPFound(location=request.app.router['post-form'].url_for())
        raise response
    return {}


@template('post_detail.html')
async def post_detail(request: web.Request):
    async with request.app['db'].acquire() as conn:
        post_query = db.posts.select().where(db.posts.c.id == request.match_info['post_id'])
        ret = await conn.execute(post_query)
        post = await ret.fetchone()
        if not post:
            raise web.HTTPNotFound()
        context = db.parse_columns(db.posts, post)
        user_query = db.users.select().where(db.users.c.id == context['user_id'])
        user = await (await conn.execute(user_query)).fetchone()
        context['user'] = f'{user[1]} {user[2]}'
    return context


@template('user_detail.html')
async def user_detail(request: web.Request):
    await check_authorized(request)
    async with request.app['db'].acquire() as conn:
        user_id = request.match_info['user_id']
        user_query = db.users.select().where(db.users.c.id == user_id)
        ret = await conn.execute(user_query)
        user = await ret.fetchone()
        if not user:
            raise web.HTTPNotFound()
        context = db.parse_columns(db.users, user)
        posts_query = db.posts.select().where(db.posts.c.user_id == user_id)
        ret = await conn.execute(posts_query)
        raw_posts = await ret.fetchall()
        context['user_posts'] = [db.parse_columns(db.posts, one_raw_post) for one_raw_post in raw_posts]

    return context


@template('profile.html')
async def profile(request: web.Request):
    pass
