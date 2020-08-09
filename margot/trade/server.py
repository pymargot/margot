import asyncio
import logging

from margot.config import settings

logger = logging.getLogger('margot')

@asyncio.coroutine
def handle_message(reader, writer):
    data = yield from reader.read()
    message = data.decode()
    logger.info('received: {}'.format(message))
    # it now goes to the portfolio manager

def init(logger):
    logger.info('starting server')
    loop = asyncio.get_event_loop()
    coro = asyncio.start_unix_server(
        handle_message, 
        path = settings.socket,
        loop = loop
        )
    return loop.run_until_complete(coro)
