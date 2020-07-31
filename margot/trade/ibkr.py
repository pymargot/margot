import threading
import asyncio
from contextlib import contextmanager

import nest_asyncio

from ib_insync import IB


class IBConnection:
    """
    # usage
    with IBConnection.client() as ib:
        ...
    """
    lock = threading.RLock()
    ib = IB()
    nest_asyncio.apply(ib.client._loop)

    @classmethod
    @contextmanager
    def client(cls):
        try:
            asyncio.get_event_loop()
        except RuntimeError:
            asyncio.set_event_loop(cls.ib.client._loop)

        cls.lock.acquire()
        if not cls.ib.isConnected():
            from config import Config
            port = Config.get('broker.ibkr.port')
            ip_address = Config.get('broker.ibkr.ipaddress')
            cls.ib.connect(
                host=ip_address,
                port=port,
                clientId=10,
                readonly=False)
        cls.lock.release()

        yield cls.ib
