# @regex (Returns|Raises):\n\s+(.*?):(.+)$
# @flags mg
# @replace $1 ($2):$3
# @endregex

import clr  # type: ignore
from threading import Thread
import time

clr.AddReference("System")  # type: ignore
import System  # type: ignore
import os, sys
from functools import partial as bind
from misc import print


import os
import inspect


def get_script_location():
  # Get the current frame
  current_frame = inspect.currentframe()
  # Get the file name from the frame
  file_path = inspect.getfile(current_frame)  # type: ignore
  # Get the absolute path
  absolute_path = os.path.abspath(file_path)
  return absolute_path


dllFile = os.path.normpath(
  os.path.join(get_script_location(), r"../AutoHotInterception.dll")
)

print(dllFile)


class AutoHotInterception:
  Instance = System.Activator.CreateInstance(
    System.Reflection.Assembly.LoadFile(dllFile).GetType(
      "AutoHotInterception.Manager"
    )
  )
  _contextManagers = {}

  def GetInstance(self):
    return self.Instance

  #   ; --------------- Input Synthesis ----------------
  def SendKeyEvent(self, id, code, state):
    self.Instance.SendKeyEvent(id, code, state)

  def SendMouseButtonEvent(self, id, btn, state):
    self.Instance.SendMouseButtonEvent(id, btn, state)

  def SendMouseButtonEventAbsolute(self, id, btn, state, x, y):
    self.Instance.SendMouseButtonEventAbsolute(id, btn, state, x, y)

  def SendMouseMove(self, id, x, y):
    self.Instance.SendMouseMove(id, x, y)

  def SendMouseMoveRelative(self, id, x, y):
    self.Instance.SendMouseMoveRelative(id, x, y)

  def SendMouseMoveAbsolute(self, id, x, y):
    self.Instance.SendMouseMoveAbsolute(id, x, y)

  def SetState(self, state):
    self.Instance.SetState(state)

  def MoveCursor(self, x, y, cm="Screen", mouseId=-1):
    pass
    # if (mouseId == -1)
    # mouseId = 11 ; Use 1st found mouse
    # oldMode = A_CoordModeMouse
    # CoordMode("Mouse", cm)
    # loop {
    # MouseGetPos(&cx, &cy)
    # dx = self.GetDirection(cx, x)
    # dy = self.GetDirection(cy, y)
    # if (dx == 0 && dy == 0)
    #     break
    # self.SendMouseMove(mouseId, dx, dy)
    # }
    # CoordMode("Mouse", oldMode)

  def GetDirection(self, cp, dp):
    d = dp - cp
    if d > 0:
      return 1
    if d < 0:
      return -1
    return 0

  #   ; --------------- Querying ------------------------
  def GetDeviceId(self, IsMouse, VID, PID, instance=1):
    devType = {0: "Keyboard", 1: "Mouse"}
    dev = self.Instance.GetDeviceId(IsMouse, VID, PID, instance)
    if dev == 0:
      print.error(
        "Could not get ",
        devType[IsMouse],
        " with VID ",
        VID,
        ", PID ",
        PID,
        ", Instance ",
        instance,
      )
      sys.exit(-1)
    return dev

  def GetDeviceIdFromHandle(self, isMouse, handle, instance=1):
    devType = {0: "Keyboard", 1: "Mouse"}
    dev = self.Instance.GetDeviceIdFromHandle(isMouse, handle, instance)
    if dev == 0:
      print.error(
        "Could not get ",
        devType[isMouse],
        " with Handle ",
        handle,
        ", Instance ",
        instance,
      )
      sys.exit(-1)
    return dev

  def GetKeyboardId(self, VID, PID, instance=1):
    return self.GetDeviceId(False, VID, PID, instance)

  def GetMouseId(self, VID, PID, instance=1):
    return self.GetDeviceId(True, VID, PID, instance)

  def GetKeyboardIdFromHandle(self, handle, instance=1):
    return self.GetDeviceIdFromHandle(False, handle, instance)

  def GetMouseIdFromHandle(self, handle, instance=1):
    return self.GetDeviceIdFromHandle(True, handle, instance)

  def GetDeviceList(self):
    DeviceList = {}
    arr = self.Instance.GetDeviceList()
    for v in arr:
      # ; ToDo: Return a class, so code completion works?
      DeviceList[v.Id] = {
        "ID": v.Id,
        "VID": v.Vid,
        "PID": v.Pid,
        "IsMouse": v.IsMouse,
        "Handle": v.Handle,
      }
    return DeviceList

  #   ; ---------------------- Subscription Mode ----------------------
  def SubscribeKey(self, id, code, block, callback, concurrent=False):
    self.Instance.SubscribeKey(id, code, block, callback, concurrent)

  def UnsubscribeKey(self, id, code):
    self.Instance.UnsubscribeKey(id, code)

  def SubscribeKeyboard(self, id, block, callback, concurrent=False):
    self.Instance.SubscribeKeyboard(id, block, callback, concurrent)

  def UnsubscribeKeyboard(self, id):
    self.Instance.UnsubscribeKeyboard(id)

  def SubscribeMouseButton(self, id, btn, block, callback, concurrent=False):
    self.Instance.SubscribeMouseButton(id, btn, block, callback, concurrent)

  def UnsubscribeMouseButton(self, id, btn):
    self.Instance.UnsubscribeMouseButton(id, btn)

  def SubscribeMouseButtons(self, id, block, callback, concurrent=False):
    self.Instance.SubscribeMouseButtons(id, block, callback, concurrent)

  def UnsubscribeMouseButtons(self, id):
    self.Instance.UnsubscribeMouseButtons(id)

  def SubscribeMouseMove(self, id, block, callback, concurrent=False):
    self.Instance.SubscribeMouseMove(id, block, callback, concurrent)

  def UnsubscribeMouseMove(self, id):
    self.Instance.UnsubscribeMouseMove(id)

  def SubscribeMouseMoveRelative(self, id, block, callback, concurrent=False):
    self.Instance.SubscribeMouseMoveRelative(id, block, callback, concurrent)

  def UnsubscribeMouseMoveRelative(self, id):
    self.Instance.UnsubscribeMouseMoveRelative(id)

  def SubscribeMouseMoveAbsolute(self, id, block, callback, concurrent=False):
    self.Instance.SubscribeMouseMoveAbsolute(id, block, callback, concurrent)

  def UnsubscribeMouseMoveAbsolute(self, id):
    self.Instance.UnsubscribeMouseMoveAbsolute(id)

  #   ; ------------- Context Mode ----------------
  #   ; Creates a context class to make it easy to turn on/off the hotkeys
  def CreateContextManager(self, id):
    if id in self._contextManagers:
      print("ID ", id, " already has a Context Manager")
      sys.exit(-1)
    cm = AutoHotInterception.ContextManager(self, id)
    self._contextManagers[id] = cm
    return cm

  def RemoveContextManager(self, id):
    if not (id in self._contextManagers):
      print("ID ", id, " does not have a Context Manager")
      sys.exit(-1)
    self._contextManagers[id].Remove()
    self._contextManagers.__delattr__(id)

  #   ; Helper class for dealing with context mode
  class ContextManager:
    IsActive = 0

    def __init__(self, parent, id):
      self.parent = parent
      self.id = id
      result = self.parent.Instance.SetContextCallback(
        id, self.OnContextCallback  # bind(, self)
      )

    def OnContextCallback(self, state, *a):
      # Sleep(0)
      # print.debug("AAA", state, a)
      self.IsActive = state

    def Remove(self):
      self.parent.Instance.RemoveContextCallback(self.id)


class AHIHook(AutoHotInterception):
  def blockKeyboard(self, block=True, id=None):
    def nullcb(*a):
      pass

    if block:
      self.SubscribeKeyboard(True, nullcb, False, id)
    else:
      self.UnsubscribeKeyboard(id)

  @staticmethod
  def getUserDevice(getKeyboard=1, getMouse=1):
    class test:
      k = 0
      m = 0

      def kk(self, id, h, *a):
        self.k = h.GetDeviceList()[id]["Handle"]
        # print("PRESSED: keyboard id is ", id, "handle: ", self.k)
        for i in range(1, 11):
          h.Instance.UnsubscribeKeyboard(i)

      def mm(self, id, h, *a):
        self.m = h.GetDeviceList()[id]["Handle"]
        # print("PRESSED: mouse id is ", id, "handle: ", self.m)
        for i in range(1, 11):
          h.Instance.UnsubscribeMouseMove(10 + i)

      def getUserInputMethod(self, h, getKeyboard, getMouse):
        for i in range(1, 11):
          if getKeyboard:
            h.Instance.SubscribeKeyboard(
              i, False, bind(self.kk, i, h), False
            )
          if getMouse:
            h.Instance.SubscribeMouseMove(
              10 + i, False, bind(self.mm, 10 + i, h), False
            )
        if getKeyboard and getMouse:
          print("Move the mouse and Press any key to continue")
        elif getKeyboard:
          print("Press any key to continue")
        elif getMouse:
          print("Move the mouse to continue")
        else:
          print.error(
            "dont call this function if you dont need keyboard or mouse handles"
          )
          os._exit(-1)
        while not ((self.k or not getKeyboard) and (self.m or not getMouse)):
          pass
        for i in range(1, 11):
          h.Instance.UnsubscribeKeyboard(i)
          h.Instance.UnsubscribeMouseButtons(10 + i)
        print("KEYBOARD ID: ", self.k, "MOUSE ID: ", self.m)
        return self.k, self.m
        # return {"keyboardHandle": self.k, "mouseHandle": self.m}

    return test().getUserInputMethod(AutoHotInterception(), getKeyboard, getMouse)

  AHI = AutoHotInterception()
  keyboardId = 0
  mouseId = 0
  keyboardHandle = None
  mouseHandle = None
  _ContextManager = 0
  subbed = []

  def __init__(self, kid: str | int | None = None, mid: str | int | None = None):
    # print("kidmid", kid, mid)
    if kid is None:
      kid = os.environ.get("INTERCEPTON_MAIN_KEYBOARD_HANDLE", None)
    if mid is None:
      mid = os.environ.get("INTERCEPTON_MAIN_MOUSE_HANDLE", None)
    # print("kidmid", kid, mid)

    if isinstance(kid, int):
      self.keyboardId = kid
    elif isinstance(kid, str):
      self.keyboardHandle = kid
      self.keyboardId = self.AHI.GetDeviceIdFromHandle(False, kid)
    if isinstance(mid, int):
      self.mouseId = mid
    elif isinstance(mid, str):
      self.mouseHandle = mid
      self.mouseId = self.AHI.GetDeviceIdFromHandle(True, mid)

    if self.keyboardHandle or self.mouseHandle:
      Thread(
        target=self.__autoKeepSameDevice,
      ).start()

    for name, code in keyCodeList.items():
      self.keyDownList[name] = 0
      # self.AddKeyStateListener(k)

  # def AddKeyStateListener(self, key):
  #     # self.keyDownList[key] = False
  #     def getKeyStateCb(self, key, down):
  #         pass
  #         # self.keyDownList[key] = down
  #         # print(key, down)

  #     self.SubscribeKey(key, False, getKeyStateCb)

  def __autoKeepSameDevice(self):
    while 1:
      if (not self.keyboardHandle) and (not self.mouseHandle):
        return

      list = self.GetDeviceList()
      if self.keyboardId and self.keyboardHandle and self.keyboardId not in list:
        self.keyboardId = self.AHI.GetDeviceIdFromHandle(
          False, self.keyboardHandle
        )
      if self.mouseId and self.mouseHandle and self.mouseId not in list:
        self.mouseId = self.AHI.GetDeviceIdFromHandle(True, self.mouseHandle)
      time.sleep(1)

  def autoUseNewestDevice(self):
    self.keyboardHandle = None
    self.mouseHandle = None
    while 1:
      list = self.GetDeviceList()
      if self.keyboardId and self.keyboardId not in list:
        self.keyboardId = self.AHI.GetDeviceIdFromHandle(
          False, AHIHook.getUserDevice(1, 0)[0]
        )
      if self.mouseId and self.mouseId not in list:
        self.mouseId = self.AHI.GetDeviceIdFromHandle(
          True, AHIHook.getUserDevice(0, 1)[1]
        )
      time.sleep(1)

  def GetMouseId(self, VID, PID, instance=1):
    return self.AHI.GetDeviceId(True, VID, PID, instance)

  def sendRaw(self, key):
    upperlist = {
      "{": "[",
      "}": "]",
      '"': "'",
      ":": ";",
      "<": ",",
      ">": ".",
      "?": "/",
      "|": "\\",
      "_": "-",
      "+": "=",
      "~": "`",
      "!": "1",
      "@": "2",
      "#": "3",
      "$": "4",
      "%": "5",
      "^": "6",
      "&": "7",
      "*": "8",
      "(": "9",
      ")": "0",
    }
    if (key == key.upper() and key.lower() != key.upper()) or key in upperlist:
      self.SendKeyEvent(("shift"), True)
      self.SendKeyEvent(
        (upperlist[key] if key in upperlist else key.lower()), True
      )
      self.SendKeyEvent(
        (upperlist[key] if key in upperlist else key.lower()), False
      )
      self.SendKeyEvent(("shift"), False)
    else:
      self.SendKeyEvent(("shift"), False)
      self.SendKeyEvent((key), True)
      self.SendKeyEvent((key), False)

  def GetKeyboardId(self, VID, PID, instance=1):
    self._ContextManager = self.AHI.CreateContextManager(
      keyboardId := self.AHI.GetDeviceId(False, VID, PID, instance)
    )
    return keyboardId

  keyDownList = {}

  def SubscribeKey(
    self, keyName, block, callback, onlyOnFirstDown=False, concurrent=False, id=None
  ):
    if id is None:
      id = self.keyboardId
    self.subbed.append(keyName)

    def FUNC(down):
      self.keyDownList[keyName] = down
      return Thread(target=callback, args=[down]).start()

    def onlyOnFirstDownFUNC(down):
      if down == self.keyDownList[keyName]:
        # print.debug("SAME", keyName, down)
        return
      # print.debug("CHANGING", keyName, down)
      self.keyDownList[keyName] = down
      return Thread(target=callback, args=[down]).start()

    if onlyOnFirstDown:
      self.keyDownList[keyName] = 0
      self.AHI.Instance.SubscribeKey(
        id, keyToCode(keyName), block, onlyOnFirstDownFUNC, concurrent
      )

    self.AHI.Instance.SubscribeKey(id, keyToCode(keyName), block, FUNC, concurrent)

  def SendKeyEvent(self, keyName, state, id=None):
    if id is None:
      id = self.keyboardId

    self.AHI.Instance.SendKeyEvent(id, keyToCode(keyName), state)

  def SubscribeMouseButtons(self, block, callback, concurrent=False, id=None):
    if id is None:
      id = self.mouseId

    self.AHI.Instance.SubscribeMouseButtons(id, block, callback, concurrent)

  def SendMouseButtonEvent(self, btn, state, id=None):
    if id is None:
      id = self.mouseId

    self.AHI.Instance.SendMouseButtonEvent(id, btn, state)

  def RebindKey(self, key1, key2, swap=0):
    def BOUND1(state):
      print.debug("changing from ", key1, " to ", key2)
      self.SendKeyEvent(key2, state)

    def BOUND2(state):
      print.debug("changing from ", key2, " to ", key1)
      self.SendKeyEvent(key1, state)

    self.SubscribeKey(key1, True, BOUND1)
    if swap:
      self.SubscribeKey(key2, True, BOUND2)

  def SubscribeKeyboard(self, block, callback, concurrent=False, id=None):
    if id is None:
      id = self.keyboardId
    self.AHI.Instance.SubscribeKeyboard(id, block, callback, concurrent)

  def UnsubscribeKeyboard(self, id=None):
    if id is None:
      id = self.keyboardId
    self.AHI.Instance.UnsubscribeKeyboard(id)

  def UnsubscribeKey(self, keyName, id=None):
    if id is None:
      id = self.keyboardId
    if keyName in self.subbed:
      self.subbed.remove(keyName)
      self.Instance.UnsubscribeKey(id, keyToCode(keyName))
      return True
    else:
      return False

  def UnsubscribeAllKeys(self, id=None):
    if id is None:
      id = self.keyboardId
    for key in self.subbed:
      self.Instance.UnsubscribeKey(id, keyToCode(key))
    self.subbed = []

  def GetKeyState(self, key):
    return self.keyDownList[key]


keyCodeList = {
  "escape": 0x1,
  "0": 0xB,
  "1": 0x2,
  "2": 0x3,
  "3": 0x4,
  "4": 0x5,
  "5": 0x6,
  "6": 0x7,
  "7": 0x8,
  "8": 0x9,
  "9": 0xA,
  "-": 0xC,
  "=": 0xD,
  "backspace": 0xE,
  "tab": 0xF,
  "q": 0x10,
  "w": 0x11,
  "e": 0x12,
  "r": 0x13,
  "t": 0x14,
  "y": 0x15,
  "u": 0x16,
  "i": 0x17,
  "o": 0x18,
  "p": 0x19,
  "[": 0x1A,
  "]": 0x1B,
  "enter": 0x11C,
  # "enter": 0x1C,
  "lcontrol": 0x1D,
  "a": 0x1E,
  "s": 0x1F,
  "d": 0x20,
  "f": 0x21,
  "g": 0x22,
  "h": 0x23,
  "j": 0x24,
  "k": 0x25,
  "l": 0x26,
  ";": 0x27,
  "'": 0x28,
  "`": 0x29,
  "~": 0x29,
  "lshift": 0x2A,
  "\\": 0x2B,
  "z": 0x2C,
  "x": 0x2D,
  "c": 0x2E,
  "v": 0x2F,
  "b": 0x30,
  "n": 0x31,
  "m": 0x32,
  ",": 0x33,
  ".": 0x34,
  "/": 0x35,
  "rshift": 0x36,
  "numpadmult": 0x37,
  "lalt": 0x38,
  "space": 0x39,
  "capslock": 0x3A,
  "f1": 0x3B,
  "f2": 0x3C,
  "f3": 0x3D,
  "f4": 0x3E,
  "f5": 0x3F,
  "f6": 0x40,
  "f7": 0x41,
  "f8": 0x42,
  "f9": 0x43,
  "f10": 0x44,
  "pause": 0x45,
  "scrolllock": 0x46,
  "numpadhome": 0x47,
  "numpadup": 0x48,
  "numpadpgup": 0x49,
  "numpadsub": 0x4A,
  "numpadleft": 0x4B,
  "numpadclear": 0x4C,
  "numpadright": 0x4D,
  "numpadadd": 0x4E,
  "numpadend": 0x4F,
  "numpaddown": 0x50,
  "numpadpgdn": 0x51,
  "numpadins": 0x52,
  "numpaddel": 0x53,
  # "printscreen": 0x54,
  # "\\": 0x56,
  "f11": 0x57,
  "f12": 0x58,
  "numpadclear": 0x59,
  "help": 0x63,
  "f13": 0x64,
  "f14": 0x65,
  "f15": 0x66,
  "f16": 0x67,
  "f17": 0x68,
  "f18": 0x69,
  "f19": 0x6A,
  "f20": 0x6B,
  "f21": 0x6C,
  "f22": 0x6D,
  "f23": 0x6E,
  "f24": 0x76,
  # "tab": 0x7C,
  "media_prev": 0x110,
  "media_next": 0x119,
  "numpadenter": 0x11C,
  "rcontrol": 0x11D,
  "volume_mute": 0x120,
  "launch_app2": 0x121,
  "media_play_pause": 0x122,
  "media_stop": 0x124,
  "volume_down": 0x12E,
  "volume_up": 0x130,
  "browser_home": 0x132,
  "numpaddiv": 0x135,
  "rshift": 0x136,
  "printscreen": 0x137,
  "ralt": 0x138,
  "numlock": 0x145,
  "ctrlbreak": 0x146,
  "home": 0x147,
  "up": 0x148,
  "pgup": 0x149,
  "left": 0x14B,
  "right": 0x14D,
  "end": 0x14F,
  "down": 0x150,
  "pgdn": 0x151,
  "insert": 0x152,
  "delete": 0x153,
  "lwin": 0x15B,
  "rwin": 0x15C,
  "appskey": 0x15D,
  "sleep": 0x15F,
  "browser_search": 0x165,
  "browser_favorites": 0x166,
  "browser_refresh": 0x167,
  "browser_stop": 0x168,
  "browser_forward": 0x169,
  "browser_back": 0x16A,
  "launch_app1": 0x16B,
  "launch_mail": 0x16C,
  "launch_media": 0x16D,
  "media_prev": 0x310,
  "media_next": 0x319,
  # "enter": 0x31C,
  # "rcontrol": 0x31D,
  "volume_mute": 0x320,
  "launch_app2": 0x321,
  "media_play_pause": 0x322,
  "media_stop": 0x324,
  "volume_down": 0x32E,
  "volume_up": 0x330,
  "browser_home": 0x332,
  # "numpaddiv": 0x335,
  # "printscreen": 0x337,
  # "ralt": 0x338,
  "ctrlbreak": 0x346,
  "numpadhome": 0x347,
  "numpadup": 0x348,
  "numpadpgup": 0x349,
  "numpadleft": 0x34B,
  "numpadright": 0x34D,
  "numpadend": 0x34F,
  "numpaddown": 0x350,
  "numpadpgdn": 0x351,
  "numpadins": 0x352,
  "numpaddel": 0x353,
  # "lwin": 0x35B,
  # "rwin": 0x35C,
  # "appskey": 0x35D,
  "sleep": 0x35F,
  "browser_search": 0x365,
  "numpad0": 0x52,
  "numpad1": 0x4F,
  "numpad2": 0x50,
  "numpad3": 0x51,
  "numpad4": 0x4B,
  "numpad5": 0x4C,
  "numpad6": 0x4D,
  "numpad7": 0x47,
  "numpad8": 0x48,
  "numpad9": 0x49,
  "numpaddot": 0x53,
  "browser_favorites": 0x366,
  "browser_refresh": 0x367,
  "browser_stop": 0x368,
  "browser_forward": 0x369,
  "browser_back": 0x36A,
  "launch_app1": 0x36B,
  "launch_mail": 0x36C,
  "launch_media": 0x36D,
}


def ReverseObj(obj):
  return dict((v, k) for (k, v) in obj.items())


def keyToCode(keyName):
  otherlist = {
    " ": "space",
    "\r": "enter",
    "\n": "enter",
    "ctrl": "lcontrol",
    "control": "lcontrol",
    "alt": "lalt",
    "shift": "lshift",
  }
  return (
    keyCodeList[str(keyName)]
    if str(keyName) in keyCodeList
    else keyCodeList[otherlist[str(keyName)]]
  )

  # return chr(code)


def codeToKey(code):
  return ReverseObj(keyCodeList)[code]
