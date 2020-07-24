from sanic import Sanic
from sanic.response import html
from sanic.log import logger
import sanic
import websockets
import concurrent
import json
import asyncio

app = Sanic(__name__)
app.static("/", "./sample.html")

@app.websocket('/ws1')
async def ws1(request, ws):
    try:
        logger.debug(f"/ws1 connected from {request.ip}")
        await ws.send(json.dumps({ "hello": "world" }))
        while True:
            await ws.recv()
    except websockets.exceptions.ConnectionClosedOK:
        logger.debug("/ws1 ConnectionClosedOK")
    except websockets.exceptions.ConnectionClosedError:
        logger.debug("/ws1 ConnectionClosedError")
    except sanic.websocket.ConnectionClosed:
        logger.debug("/ws1 ConnectionClosed: " + str(e))
    except websockets.exceptions.WebSocketException as e:
        logger.debug("/ws1 WebSocketException: " + str(e))
    except concurrent.futures.CancelledError:
        logger.debug("/ws1 CancelledError") # ws.recv() raised this
    except BaseException as e:
        logger.debug("/ws1 BaseException: " + str(type(e)))

@app.websocket('/ws2')
async def ws2(request, ws):
    try:
        logger.debug(f"/ws2 connected from {request.ip}")
        await asyncio.sleep(10)
        await ws.send(json.dumps({ "hello": "world" }))
        while True:
            await asyncio.sleep(10)
    except websockets.exceptions.ConnectionClosedOK:
        logger.debug("/ws2 ConnectionClosedOK")
    except websockets.exceptions.ConnectionClosedError:
        logger.debug("/ws2 ConnectionClosedError")
    except sanic.websocket.ConnectionClosed:
        logger.debug("/ws2 ConnectionClosed: " + str(e))
    except websockets.exceptions.WebSocketException as e:
        logger.debug("/ws2 WebSocketException: " + str(e))
    except concurrent.futures.CancelledError:
        logger.debug("/ws2 CancelledError") # ws.send() raised this
    except BaseException as e:
        logger.debug("/ws2 BaseException: " + str(type(e)))

@app.websocket('/ws3')
async def ws3(request, ws):
    try:
        logger.debug(f"/ws3 connected from {request.ip}")
        listeners = [ ws ]
        await asyncio.sleep(10)
        await asyncio.wait([ ws.send(json.dumps({ "hello": "world"}) for ws in listeners )])
        while True:
            await asyncio.sleep(10)
    except websockets.exceptions.ConnectionClosedOK:
        logger.debug("/ws3 ConnectionClosedOK")
    except websockets.exceptions.ConnectionClosedError:
        logger.debug("/ws3 ConnectionClosedError")
    except sanic.websocket.ConnectionClosed:
        logger.debug("/ws3 ConnectionClosed: " + str(e))
    except websockets.exceptions.WebSocketException as e:
        logger.debug("/ws3 WebSocketException: " + str(e))
    except concurrent.futures.CancelledError:
        logger.debug("/ws3 CancelledError") # asyncio.wait(ws.send()) raised this
    except BaseException as e:
        logger.debug("/ws3 BaseException: " + str(type(e)))

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
