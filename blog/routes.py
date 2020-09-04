from aiohttp import web

from . import views


def setup_routes(app: web.Application):
    app.add_routes([
        web.get('/', views.post_list, name='home'),
        web.get('/post/{post_id}', views.post_detail, name='post-detail'),
        web.get('/profile', views.profile, name='profile'),
        web.get('/user/{user_id}', views.user_detail, name='user-detail'),

        web.get('/post', views.post_form, name='post-form'),
        web.post('/post', views.post_form),
        web.get('/login', views.login, name='login'),
        web.post('/login', views.login),
        web.get('/logout', views.logout, name='logout'),
        web.post('/logout', views.logout),
        web.get('/register', views.register, name='register'),
        web.post('/register', views.register),
    ])
