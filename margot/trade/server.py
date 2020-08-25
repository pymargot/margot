import asyncio
import logging
import json
from pathlib import Path

from margot.config import settings

logger = logging.getLogger('margot')


class MargotJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Path):
            return str(obj)


@asyncio.coroutine
def handle_message(reader, writer):
    data = yield from reader.readline()
    msg = data.decode()
    logger.info('received: {}'.format(msg))
    # it now goes to the portfolio manager
    tokens = msg.split()

    if tokens[0] == 'GETALGO':
        reply = json.dumps(
            settings.algos.get(
                tokens[1],
                'NONE'),
            cls=MargotJSONEncoder)
        writer.write(reply.encode())
        writer.close()
        logger.debug('Sent reply: {}'.format(reply))


def init(logger):
    logger.info('starting server')
    loop = asyncio.get_event_loop()
    coro = asyncio.start_unix_server(
        handle_message,
        path=settings.sys.get('socket'),
        loop=loop
    )
    return loop.run_until_complete(coro)
