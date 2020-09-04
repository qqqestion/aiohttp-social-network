import asyncio
from aiohttp import web

import logging

from argparse import ArgumentParser

from blog.app import create_app

import aioreloader


# logging.basicConfig(filename='file.log', level=logging.DEBUG)


try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError as exp:
    # logging.debug(f'ImportError: {exp}')
    pass


def parse_arguments(app):
    parser = ArgumentParser()
    parser.add_argument('--host', type=str, help='Host to listen', default='0.0.0.0')
    parser.add_argument('--port', help='Port to access connections', default=8080)
    parser.add_argument('--reload', action='store_true', help='Autoreload code on change')

    args = parser.parse_args()
    if args.reload:
        # logging.debug('Starts with code reload')
        aioreloader.start()
    return args


app = create_app()


if __name__ == '__main__':
    # logging.info('Start project')
    args = parse_arguments(app)
    web.run_app(app, host=args.host, port=args.port)
