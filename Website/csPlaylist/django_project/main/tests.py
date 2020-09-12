#from django.test import TestCase

# Create your tests here.
import websocket
import json
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    message = json.loads(message)
    print(message)
    time.sleep(1)
    s = input("yeet")
    print("sending shit")
    ws.send(json.dumps({"signal":"oops"}))

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        ws.send(json.dumps({"id":"1"}))
        time.sleep(1)
    #print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://172.104.17.15:8000/camera1",
                              on_message = lambda ws,msg: on_message(ws, msg),
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()