# sanic-websocket-sample

## What exceptions will Sanic websocket handlers raise?

When a connection is closed during ws.recv(), ws.send(), or ws.send() in asyncio.wait(),
those methods will raise `concurrent.futures.CancelledError`.

```python
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
```
