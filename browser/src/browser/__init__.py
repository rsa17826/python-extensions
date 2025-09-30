# @regex (Returns|Raises):\n\s+(.*?):(.+)$
# @flags mg
# @replace $1 ($2):$3
# @endregex

import websocket
import threading
import requests
from misc import print, json, bind

__all__: list[str] = ["browser"]


class browser:
  @staticmethod
  class tab:
    ws = None
    wsId = 1
    isOpen = None
    responses = {}

    def closeWebSocket(self, *args):
      # print(args)
      self.ws.close()
      self.isOpen = False
      self.responses = {}

    def openWebSocket(self):
      def on_message(self, ws, message):
        message = json.parse(message)
        print.info("response", message)
        if "error" in message:
          print.error(self, message["error"])
          self.responses[message["id"]] = 1
          # ws.close()
        else:
          self.responses[message["id"]] = message["result"]
          # ws.close()

      def on_error(self, ws, error):
        print.error(self, error)
        # self.responses[]
        self.closeWebSocket()

      def on_open(self, ws):
        self.isOpen = True

      ws = websocket.WebSocketApp(
        self.webSocketDebuggerUrl,
        on_message=bind(on_message, self),
        on_error=bind(on_error, self),
        on_close=bind(self.closeWebSocket),
      )
      ws.on_open = bind(on_open, self)
      self.ws = ws
      self.responses = {}
      threading.Thread(target=ws.run_forever).start()

    def run(self, method, data={}, **kwargs):
      if not self.isOpen:
        self.openWebSocket()
      while not self.isOpen:
        pass

      self.wsId += 1
      responseID = self.wsId
      command = {"id": responseID, "method": method, "params": {**kwargs}, **data}

      self.ws.send(json.str(command))
      print.info(command)
      while responseID not in self.responses:
        pass

      return self.responses[responseID]

    def __init__(self, id):
      self.id = id

      class click:
        tab = 0

        def __init__(self, tab):
          self.tab = tab

        def __call__(
          self,
          x=0,
          y=0,
          down=True,
          up=True,
          button=0,
          modifiers=0,
          heldButtons=0,
          clickCount=1,
        ):
          # print(self.tab.url)
          # print(self, self.tab, "asdasdsasdasds")

          def press(down):
            self.tab.run(
              "Input.dispatchMouseEvent",
              type="mousePressed" if down else "mouseReleased",
              x=x,
              y=y,
              button=button,
              buttons=heldButtons,
              clickCount=clickCount,
              pointerType="mouse",
              modifiers=modifiers,
            )

          if down:
            press(True)
          if up:
            press(False)

        enumerate("left")
        alt = 1
        ctrl = 2
        shift = 8
        meta = 4

        left = "left"
        right = "right"
        middle = "middle"
        back = "back"
        forward = "forward"

      self.click = click(self)
      # print(self, self.click.tab, "asdasds")

    def __str__(self):
      return f"<Tab [{self.id}]>"

    def close(self):
      requests.get(f"http://127.0.0.1:9222/json/close/{self.id}", json=True)

    def getData(self):
      return list(
        filter(
          lambda x: x["id"] == self.id,
          requests.get("http://127.0.0.1:9222/json", json=True).json(),
        )
      )[0]

    def eval(self, script):
      return self.run("Runtime.evaluate", {"params": {"expression": script}})[
        "result"
      ]["value"]

    __name__ = "Tab"

    def reload(self, cache=False):
      self.run("Page.reload", {"ignoreCache": not cache})

    def disableCsp(self, true=True):
      self.run("Page.setBypassCSP", {"enabled": true})

    def stopLoading(self):
      self.run("Page.stopLoading")

    def __getattr__(self, name):
      # Fallback for any unset properties
      data = self.getData()
      return data[name] if name in data else data

    __repr__ = __str__

  @staticmethod
  def open(url="http://127.0.0.1:8080"):
    res = requests.put(f"http://127.0.0.1:9222/json/new?{url}", json=True).json()
    # print.info(res)
    return browser.tab(res["id"])

  @staticmethod
  def close(id):
    requests.get(f"http://127.0.0.1:9222/json/close/{id}", json=True)

  @staticmethod
  def getTabs():
    return list(
      map(
        lambda x: browser.tab(x["id"]),
        requests.get("http://127.0.0.1:9222/json").json(),
      )
    )

  @staticmethod
  def getTab(id):
    return requests.get(f"http://127.0.0.1:9222/json/{id}", json=True).json()

  @staticmethod
  def getActiveTab():
    tablist = browser.tab(
      requests.get("http://127.0.0.1:9222/json").json()[0]["id"]
    ).run("Target.getTargets")
    return browser.tab(
      list(filter(lambda x: x["attached"], tablist["targetInfos"]))[0]["targetId"]
    )

  @staticmethod
  def closeBrowser():
    return browser.getActiveTab().run(
      "Browser.close",
    )
