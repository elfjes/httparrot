import asyncio
import os
from dataclasses import dataclass
from typing import Dict

import tornado.ioloop
import tornado.web


@dataclass
class Response:
    body: bytes
    status: int = 200
    delay: float = 0


responses: Dict[str, Response] = {}


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        response = responses.get(self.request.path)
        if response:
            await self.write_response(response)
        else:
            raise tornado.web.HTTPError(404)

    async def post(self):
        status = int(self.get_argument("status", default="200"))
        if status < 200:
            raise tornado.web.HTTPError(400)

        delay = float(self.get_argument("delay", default="0"))
        uri = self.request.path
        body = self.request.body
        responses[uri] = Response(body, status, delay)
        self.write("OK")

    async def write_response(self, response: Response):
        self.clear()
        await asyncio.sleep(response.delay)
        self.set_status(response.status)
        await self.finish(response.body)


def make_app():
    return tornado.web.Application(default_handler_class=MainHandler, autoreload=True)


def get_env():
    prefix = "HTTPARROT_"
    params = {"PORT": (int, 8888)}
    return {
        key: value[0](os.environ.get(prefix + key, value[1])) for key, value in params.items()
    }


def main():
    tornado.log.enable_pretty_logging()
    app = make_app()
    params = get_env()
    app.listen(params["PORT"])
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
