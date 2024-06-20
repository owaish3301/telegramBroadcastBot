import logging
from aiogram.client.session.middlewares.request_logging import RequestLogging

class MyRequestLogging(RequestLogging):
    def __init__(self, ignore_methods=None):
        self.ignore_methods = ignore_methods if ignore_methods else []

    async def __call__(self, make_request, bot, method):
        if type(method).__name__ not in self.ignore_methods:
            logging.info("Make request with method=%r by bot id=%d", type(method).__name__, bot.id)
        return await make_request(bot, method)
