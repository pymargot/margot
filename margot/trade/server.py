import asyncio
import logging

logger = logging.getLogger('margot')

@asyncio.coroutine
def handle_message(reader, writer):
    data = yield from reader.read()
    message = data.decode()
    logger.info('received: {}'.format(message))


def init(logger):
    logger.info('starting unix socket listener')
    loop = asyncio.get_event_loop()
    coro = asyncio.start_unix_server(
        handle_message, 
        path='/tmp/.margot-socket',
        loop = loop
        )
    return loop.run_until_complete(coro)
