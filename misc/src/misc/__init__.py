# @regex (Returns|Raises):\n\s+(.*?):(.+)$
# @flags mg
# @replace $1 ($2):$3
# @endregex

import re
import json as oldjson
import os
import csv
from pathlib import Path
import inspect


# # Get the frame of the caller
caller_frame = inspect.stack()[-3]
caller_file = caller_frame.filename
paths = [*map(lambda x: x.filename, inspect.stack())]
for path in paths:
  # if not Path(path.replace("\\\\", "\\")).exists():
  #   continue
  if path.endswith("\\runpy.py"):
    continue
  if "\\debugpy\\" in path:
    continue
  if "\\debugpy/" in path:
    continue
  if "/debugpy/" in path:
    continue
  if "/debugpy\\" in path:
    continue
  if path.endswith(">"):
    continue
  # print(path)
  caller_file = path
# print(caller_file, paths)

# # Change the working directory to the directory of the caller file
print("changing dir to ", os.path.dirname(os.path.abspath(caller_file)))
os.chdir(os.path.dirname(os.path.abspath(caller_file)))
LOG_FILE_NAME = os.path.basename(caller_file)[:-3] + ".ans"

# from folderikon.folderikon import FolderIkon
from time import sleep as __badsleep
import shutil
import copy
import sys
import re
import os
from tkinter import filedialog
import TKinterModernThemes as TKMT
import sys
import os, commentjson
import subprocess as sp
import tkinter as tk
import win32clipboard

from functools import partial as bind

import requests

MAIN_FILE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

# or os.path.dirname(os.getcwd())

__all__ = [
  "dictmerge",
  "json",
  "setfoldericon",
  "showpath",
  "quote",
  "sleep",
  "enum",
  "args",
  "f",
  "print",
  "fg",
  "bg",
  "listcolors",
  "setfoldericon",
  "printinbox",
  "parse_query_string",
  "LLM",
]


def parse_query_string(qs=os.environ.get("QUERY_STRING", "")):
  data = qs.split("&")
  newdata = {}
  for x in data:
    newdata[x.split("=")[0]] = x.split("=")[1]
  return newdata


class cache:
  """simple caching function

  Returns (self): cache manager object

  EXAMPLE: if cache.has("item"):\n
  \treturn cache.get()\n
  value = dothings()
  return cache.set(value)
  """

  lastinp = None

  def __init__(self):
    """generate new cache object"""
    self.cache = {}

  def has(self, item):
    """tells if item is in cache object

    Args:
      item (ant): item to check

    Returns (bool): returns true if item is cached
    """
    self.lastinp = item
    return item in self.cache

  def get(self):
    """returns the item from the cache - should be called only if self.has has returned true - returns the last item that was checked for in the cache

    Raises (KeyError): if item is not in cache

    Returns (any): returns the item from cache
    """
    if not self.has(self.lastinp):
      raise KeyError(f"No such item {self.lastinp}")
    thing = self.cache[self.lastinp]
    del self.lastinp
    return thing

  def set(self, value):
    """sets the item in cache to a value - should only be used after calling self.has returned false - updates the last item that was checked for in the cache

    Args:
      value (any): the value to set the item to

    Returns (type(value)): the data that was passed in as value
    """
    self.cache[self.lastinp] = value
    del self.lastinp
    return value

  def clear(self):
    """clears the cache"""
    self.cache = {}


class enum:
  """creates an enum var like enum in gdscript"""

  def __init__(self, *args):
    self._dict = dict(zip(args, range(len(args))))

  def __getattr__(self, name: str) -> int:
    return self._dict[name]

  def __getitem__(self, name: str) -> int:
    return self._dict[name]


# F
class f:
  @staticmethod
  def read(
    file,
    default="",
    asbinary=False,
    buffering: int = -1,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
    closefd: bool = True,
    opener=None,
  ):
    if Path(file).exists():
      with open(
        file,
        "r" + ("b" if asbinary else ""),
        buffering=buffering,
        encoding=encoding,
        errors=errors,
        newline=newline,
        closefd=closefd,
        opener=opener,
      ) as f:
        text = f.read()
      if text:
        return text
      return default
    else:
      with open(
        file,
        "w" + ("b" if asbinary else ""),
        buffering=buffering,
        encoding=encoding,
        errors=errors,
        newline=newline,
        closefd=closefd,
        opener=opener,
      ) as f:
        f.write(default)
      return default

  @staticmethod
  def writeCsv(file, rows):
    with open(file, "w", encoding="utf-8", newline="") as f:
      w = csv.writer(f)
      w.writerows(rows)
    return rows

  @staticmethod
  def write(
    file,
    text,
    asbinary=False,
    buffering: int = -1,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
    closefd: bool = True,
    opener=None,
  ):
    with open(
      file,
      "w" + ("b" if asbinary else ""),
      buffering=buffering,
      encoding=encoding,
      errors=errors,
      newline=newline,
      closefd=closefd,
      opener=opener,
    ) as f:
      f.write(text)
    return text

  @staticmethod
  def append(
    file,
    text,
    asbinary=False,
    buffering: int = -1,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
    closefd: bool = True,
    opener=None,
  ):
    with open(
      file,
      "a",
      buffering=buffering,
      encoding=encoding,
      errors=errors,
      newline=newline,
      closefd=closefd,
      opener=opener,
    ) as f:
      f.write(text)
    return text

  @staticmethod
  def writeline(
    file,
    text,
    buffering: int = -1,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
    closefd: bool = True,
    opener=None,
  ):
    with open(
      file,
      "a",
      buffering=buffering,
      encoding=encoding,
      errors=errors,
      newline=newline,
      closefd=closefd,
      opener=opener,
    ) as f:
      f.write("\n" + text)
    return text


# END

# ARGS
cmdargs = []
a_args = {}


class args:
  @staticmethod
  def parse(args: list[str] | None = None) -> dict[str, list[str | None]]:
    global a_args
    if args == None:
      args = sys.argv[1:]
    argobj = {}
    key = None
    while len(args):
      arg = args[0]
      if arg.startswith("-") or arg.startswith("/"):
        arg = re.sub(r"^(--?|\/)", "", arg)
        key = arg
        if arg not in argobj:
          argobj[key] = []
      else:
        argobj[key].append(arg)
      args = args[1:]
    a_args = argobj
    return argobj

  @staticmethod
  def anyargs():
    return a_args

  @staticmethod
  def match(cmd, option):
    foundcmd = None
    for obj in cmdargs:
      if cmd in obj["cmds"]:
        foundcmd = obj
        break
    if not foundcmd:
      print.error(cmd, "not in aliases")
      return False
    for value in foundcmd["values"]:
      if option in value["cmds"]:
        if "" in value["cmds"] and not args.get(cmd):
          return True
        for foundopt in value["cmds"]:
          if foundopt in args.get(cmd):
            return True
    return False

  @staticmethod
  def has(hasarg):
    cmd = None
    for obj in cmdargs:
      if hasarg in obj["cmds"]:
        cmd = obj
        break
    if not cmd:
      print.error(hasarg, "not in aliases")
      return False
    for cmd in cmd["cmds"]:
      if cmd in a_args:
        return True
    return False

  @staticmethod
  def setalias(*a):
    global cmdargs
    cmdargs += a

  @staticmethod
  def showgui():
    args = []
    vars = {}
    cmdtypes = enum("bool", "text", "enum", "dir", "file")

    def run(hide=""):
      script_path = os.path.abspath(sys.argv[0])
      for cmd, obj in vars.items():
        val = obj["var"].get()
        # print.debug(cmd, val, obj)
        match obj["type"]:
          case cmdtypes.file | cmdtypes.dir:
            if val != "":
              args.append(f"-{cmd}")
              args.append(val)
          case cmdtypes.enum:
            if val != "UNSET":
              args.append(f"-{cmd}")
              if (
                val in obj["replacements"]
                and obj["replacements"][val] != ""
              ):
                args.append(obj["replacements"][val])
          case cmdtypes.text:
            if val != "UNSET":
              args.append(f"-{cmd}={val}")
          case cmdtypes.bool:
            if val == "1":
              args.append(f"-{cmd}")

      # print.debug(args)
      sp.run(
        [
          f"{os.path.join(os.path.dirname(os.path.abspath(__file__)), 'runpyfile.exe')}",
          f"{script_path}",
          os.getcwd(),
          hide,
          *args,
        ]
      )
      sys.exit(0)

    ui = TKMT.ThemedTKinterFrame("TITLE", "park", "dark", False, False)
    ui.Button("run", run)
    ui.Button("run hidden", bind(run, "hide"))
    ui.Separator() # type: ignore
    ui.root.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))

    class add:
      @staticmethod
      def option(cmd, text, options, replacements):
        ui.Text(text)
        vars[cmd] = {
          "var": tk.StringVar(),
          "type": cmdtypes.enum,
          "replacements": replacements,
        }
        vars[cmd]["var"].set(options[0])
        ui.OptionMenu(options, vars[cmd]["var"])
        # allow custom text
        # ui.Combobox(options, vars[cmd]["var"])

      @staticmethod
      def bool(cmd, text):
        vars[cmd] = {"var": tk.StringVar(), "type": cmdtypes.bool}
        vars[cmd]["var"].set(0)
        ui.SlideSwitch(text, vars[cmd]["var"])

      @staticmethod
      def text(cmd, text):
        vars[cmd] = {"var": tk.StringVar(), "type": cmdtypes.text}
        vars[cmd]["var"].set("")
        ui.Text(text)
        ui.Entry(vars[cmd]["var"])

      @staticmethod
      def dir(cmd, text):
        vars[cmd] = {"var": tk.StringVar(), "type": cmdtypes.dir}
        vars[cmd]["var"].set("")

        def getfile(cmd):
          vars[cmd]["var"].set(filedialog.askdirectory())

        ui.Button("FOLDER: " + text, bind(getfile, cmd))

      @staticmethod
      def file(cmd, text):
        vars[cmd] = {"var": tk.StringVar(), "type": cmdtypes.file}
        vars[cmd]["var"].set("")

        def getfile(cmd):
          vars[cmd]["var"].set(filedialog.Open().show())

        ui.Button("FILE: " + text, bind(getfile, cmd))

    for arg in cmdargs:
      if "values" in arg:
        replacements = {}
        usertexts = ["UNSET"]
        for obj in arg["values"]:
          text = f'"{'", "'.join(obj['cmds'])}"'
          if "help" in obj:
            text += f" = {obj["help"]}"
          replacements[text] = obj["cmds"][0]
          usertexts.append(text)
        add.option(
          arg["cmds"][0],
          arg["help"] if "help" in arg else arg["cmds"][0],
          usertexts,
          replacements,
        )
        continue
        # add.text(val)
      match arg["type"]:
        case "text":
          add.text(
            arg["cmds"][0], f'"{'", "'.join(arg['cmds'])}" = ' + arg["help"]
          )
        case "bool":
          add.bool(
            arg["cmds"][0], f'"{'", "'.join(arg['cmds'])}" = ' + arg["help"]
          )
        case "dir":
          add.dir(
            arg["cmds"][0], f'"{'", "'.join(arg['cmds'])}" = ' + arg["help"]
          )
        case "file":
          add.file(
            arg["cmds"][0], f'"{'", "'.join(arg['cmds'])}" = ' + arg["help"]
          )
        case _:
          print.error("arg needs valid type", arg)

    ui.run()

  @staticmethod
  def get(getarg):
    if not args.has(getarg):
      return []
    cmd = None
    for arg in cmdargs:
      if getarg in arg["cmds"]:
        cmd = arg
        break
    if not cmd:
      # print(arg, "not in aliases")
      return False
    found = []
    for arg in cmd["cmds"]:
      if arg in a_args:
        found += a_args[arg]
    return found


args.parse(["-log"])

# args.parse()

args.setalias(
  {
    "cmds": ["log"],
    "help": "log all print statements",
    "type": "bool",
    "default": False,
  },
)
args.setalias(
  {
    "cmds": ["h", "help", "?"],
    "help": "Show this help message.",
    "type": "bool",
    "default": False,
  },
  {
    "cmds": ["gui"],
    "help": "Open the GUI",
    "type": "bool",
    "default": False,
  },
)

args.setalias(
  {
    "cmds": ["plainprint", "plain print", "plain-print", "pp"],
    "help": "print all text with no colors",
    "type": "bool",
    "default": False,
  }
)
plainprint = args.has("plainprint")


def printinbox(
  printtext,
  box="""
╔═╗
║ ║
╚═╝
""",
):
  box = [*map(lambda x: x.strip(), box.strip().split("\n"))]
  printtext = printtext.strip().split("\n")
  linelen = len(max(printtext, key=len))
  print.plain(fg(90) + box[0][0] + box[0][1] * (linelen + 2) + box[0][2] + fg())
  print.plain(
    fg(90) + box[1][0] + fg() + " " * (linelen + 2) + fg(90) + box[1][2] + fg()
  )
  for text in printtext:
    print.plain(
      fg(90)
      + box[1][0]
      + fg()
      + " "
      + text
      + " " * (linelen - len(text))
      + " "
      + fg(90)
      + box[1][2]
      + fg()
    )
  print.plain(
    fg(90) + box[1][0] + fg() + " " * (linelen + 2) + fg(90) + box[1][2] + fg()
  )
  print.plain(fg(90) + box[2][0] + box[2][1] * (linelen + 2) + box[2][2] + fg())


# apathyosis
from threading import Timer

Timer(0, lambda: args.showgui() if args.has("gui") else None).start()


def showhelp():
  if args.has("?"):
    printtext = ""
    for cmdarg in cmdargs:
      if "help" in cmdarg:
        printtext += f'\n"{'", "'.join(cmdarg["cmds"])}" = {cmdarg['help']}'
      else:
        printtext += f'\n"{'", "'.join(cmdarg["cmds"])}"'
      if "values" in cmdarg and cmdarg["values"]:
        printtext += ":"
        for obj in cmdarg["values"]:
          printtext += f'\n  "{'", "'.join(obj['cmds'])}" = {obj['help']}'
    printinbox(printtext)


Timer(
  0.1, showhelp
).start() # dont know why but 0 doesnt work on this like it did above
# END


def flat(args):
  """flattens a list by one layer

  Args:
    args (list): list to flatten

  Returns (list): flattened list
  """
  retvals = []
  for arg in args:
    retvals += arg
  return retvals


def sleep(time):
  """sleep but in ms

  Args:
    time (int | float): time to wait
  """
  __badsleep(time / 1000)


def quote(data):
  return f'"{data}"'


def showpath(path):
  return quote(os.path.normpath(path))


def dictmerge(dict1, dict2, reversePriority=False):
  """
  Merge two dictionaries into one, with the second dictionary's values taking priority over the first dictionary's values.
  If a key in both dictionaries is a list, append all items from the second dictionary's list to the first dictionary's list.
  If a key in both dictionaries is a sub-dictionary, recursively merge the sub-dictionaries.
  If reversePriority is True, prioritize the first dictionary's values over the second dictionary's values.

  Parameters:
    dict1 (dict): The base dictionary.
    dict2 (dict): The secondary dictionary whose values take priority.
    reversePriority (bool): Whether to prioritize the first dictionary's values. Default: False.

  Returns (dict:): The merged dictionary.
  """
  for key, value in dict2.items():
    if isinstance(value, list) and key in dict1:
      for listitem in value:
        if listitem not in dict1[key]:
          dict1[key].append(listitem)
    elif isinstance(value, dict) and key in dict1:
      dictmerge(dict1[key], value, reversePriority=reversePriority)
    else:
      if not reversePriority or key not in dict1:
        dict1[key] = value
  return dict1


class json:
  """
  A class for working with JSON data.

  This class provides methods for parsing and merging JSON data, as well as setting folder icons.
  """

  @staticmethod
  def parseincludes(
    parent, innerjson=None, splitpathat="/", previnnerjson=None
  ) -> dict | list:
    """
    Recursively merge included JSON data into a parent dictionary.

    This method traverses the parent dictionary and includes referenced JSON data from specified paths.
    If a path is invalid or a recursion error occurs, an error message will be printed.

    Parameters:
      parent (dict): The parent dictionary to merge into.
      innerjson : SHOULD NOT BE SET
      splitpathat (str): The path separator to use when splitting include paths. Defaults to "/".
      previnnerjson : SHOULD NOT BE SET

    Returns (dict): The merged dictionary with included JSON data.
    """

    def ref(mainjson, thisjson=None):
      thisjson = copy.deepcopy(mainjson if thisjson is None else thisjson)
      if isinstance(thisjson, dict) and "#include" in thisjson:
        if not isinstance(thisjson["#include"], list):
          print.error(
            f"JSONREF: #include should be a list not a {type(thisjson["#include"])}",
            thisjson,
          )
          # os._exit(-1)
          raise TypeError(
            f"JSONREF: #include should be a list not a {type(thisjson["#include"])}"
          )
        for include in thisjson["#include"]:
          try:
            jsonatpath = mainjson
            for pathpart in (
              include.split(splitpathat) if splitpathat else [include]
            ):
              jsonatpath = jsonatpath[pathpart]
            newref = ref(mainjson, jsonatpath)
            # if isinstance(newref, list):
            #     key = include.split(splitpathat)[-1]
            #     if key in thisjson and thisjson[key]:
            #         thisjson[key] += newref
            #     else:
            #         thisjson[key] = newref
            # elif isinstance(newref, dict):
            dictmerge(thisjson, newref, reversePriority=True)
          except (RecursionError, KeyError) as e:
            if isinstance(e, KeyError):
              print.warn(
                f"JSONREF: error accessing included path {showpath(include)} originating from path {showpath(key)}"
              )
            elif isinstance(e, RecursionError):
              print.error(
                f"JSONREF: recursion error found when reading included path {showpath(include)} originating from path {showpath(key)}"
              )
              raise e
        del thisjson["#include"]
      if isinstance(thisjson, list):
        for item in thisjson:
          if isinstance(item, dict) and "#include" in item:
            thisjson.remove(item)
            lastthisjson = copy.deepcopy(thisjson)
            thisjson = []
            # asdasdajkasdgasdjksadjkasdgsadkgjsajkasdgkjgassdagkjasd
            if not isinstance(item["#include"], list):
              print.error(
                f"JSONREF: #include should be a list not a {type(item["#include"])}",
                thisjson,
              )
              # os._exit(-1)
              raise TypeError(
                f"JSONREF: #include should be a list not a {type(item["#include"])}"
              )

            for include in item["#include"]:
              try:
                jsonatpath = mainjson
                for pathpart in (
                  include.split(splitpathat)
                  if splitpathat
                  else [include]
                ):
                  jsonatpath = jsonatpath[pathpart]
                newref = ref(mainjson, jsonatpath)
                if isinstance(newref, list):
                  thisjson += newref
              except (RecursionError, KeyError) as e:
                if isinstance(e, KeyError):
                  print.warn(
                    f"JSONREF: error accessing included path {showpath(include)} originating from path {showpath(key)}"
                  )
                elif isinstance(e, RecursionError):
                  print.error(
                    f"JSONREF: recursion error found when reading included path {showpath(include)} originating from path {showpath(key)}"
                  )
                  raise e
            thisjson += lastthisjson
            # asdasd
      return copy.deepcopy(thisjson)

    if innerjson is None:
      innerjson = parent
    if isinstance(innerjson, list):
      for item in innerjson:
        if isinstance(item, list):
          json.parseincludes(
            parent, item, splitpathat=splitpathat, previnnerjson=innerjson
          )
        if isinstance(item, dict):
          if "#include" in item:
            for key, val in previnnerjson.items(): # type: ignore
              if val == innerjson:
                previnnerjson[key] = ref(parent, innerjson) # type: ignore
                break
          json.parseincludes(
            parent, item, splitpathat=splitpathat, previnnerjson=innerjson
          )
    else:
      for key, val in innerjson.items():
        if isinstance(val, list):
          json.parseincludes(
            parent, val, splitpathat=splitpathat, previnnerjson=innerjson
          )
        if isinstance(val, dict):
          innerjson[key] = ref(parent, innerjson[key])
          json.parseincludes(
            parent,
            innerjson[key],
            splitpathat=splitpathat,
            previnnerjson=innerjson,
          )
    return parent

  @staticmethod
  def parse(json: str) -> list | dict:
    """Parse a JSON string into a Python object ignoring comments.

    This method removes any // or /* */ style comments from the input JSON string before parsing it.

    Parameters:
      json (str): The JSON string to parse.

    Returns (list | dict): The parsed JSON data.
    """
    # json = re.sub(
    #     r"^ *//.*$\n?", "", json, flags=re.MULTILINE
    # ) # remove // comments
    # json = re.sub(
    #     r"^ */\*[\s\S]*?\*\/$", "", json, flags=re.MULTILINE
    # ) # remove /**/ comments
    # json = re.sub(
    #     r"(,\s+)\}", "}", json, flags=re.MULTILINE
    # ) # remove extra trailing commas
    # json = re.sub(
    #     r"(,\s+)\]", "]", json, flags=re.MULTILINE
    # ) # remove extra trailing commas
    return commentjson.loads(json)

  @staticmethod
  def str(obj, indent=False):
    if indent:
      return oldjson.dumps(obj, indent=2)
    else:
      return oldjson.dumps(obj)


# def setfoldericon(dir: str, imgpath: str) -> None:
#     """
#     Set the folder icon for a directory.

#     This function replaces the existing folder icon with a new one from the specified image path.
#     If the new image is identical to the old one, no changes are made.

#     Parameters:
#         dir (str): The absolute path of the directory whose icon should be updated.
#         imgpath (str): The absolute path of the new image file to use as the folder icon.
#     """
#     dir = os.path.abspath(dir)
#     if Path(os.path.join(dir, "foldericon.ico")).is_file():
#         oldfilebin = f.read(os.path.join(dir, "foldericon.ico"), asbinary=True)
#         newfilebin = f.read(imgpath, asbinary=True)
#         if newfilebin == oldfilebin:
#             return
#     try:
#         os.remove(os.path.join(dir, "foldericon.ico"))
#     except Exception:
#         pass
#     sleep(10)
#     shutil.copy(imgpath, os.path.join(dir, "foldericon.ico"))
#     sleep(10)

#     class temp:
#         image = os.path.join(dir, "foldericon.ico")
#         icon = Path(os.path.join(dir, "foldericon.ico"))
#         parent = Path(dir)
#         delete_original = False
#         raise_on_existing = False
#         dont_hide_icon = False
#         no_color = False

#     workdir = os.getcwd()
#     os.chdir(dir)
#     fi = FolderIkon(temp)
#     fi.image = Path(os.path.join(dir, "foldericon.ico"))
#     fi.iconize()
#     os.chdir(workdir)

#     print.debug(f"icon updated for {showpath(dir)}")


# def move(start, end):
#     """
#     Moves a single file from the start path to the end directory.

#     If the destination is a directory and the source is a file,
#     renames the file using the rename function.

#     Args:
#         start (str): The original path of the file.
#         end (str): The destination directory.


#     Returns (None):
#     """
#     if Path(start).is_file() and Path(end).is_dir():
#         file = start
#         base_name, extension = os.path.splitext(file)
#         os.rename(file, rename(extension, end, base_name))
def make_same_length(strings: list[str], char_to_use: str = " "):
  """makes all strings the same length by adding to start and equally to center

  Args:
    strings (list[str]): the list of strings to center
    char_to_use (str, optional): the char to use to center items - only one char length for best results. Defaults to " ".

  Returns (list[str]): list of strings
  """
  # Find the maximum length of the strings in the array
  max_length = max(len(s) for s in strings)

  # Pad each string to the maximum length
  for i in range(len(strings)):
    current_length = len(strings[i])
    if current_length < max_length:
      padding = (max_length - current_length) // 2
      strings[i] = char_to_use * padding + strings[i] + char_to_use * padding
      # If still shorter, add one more char_to_use
      if len(strings[i]) < max_length:
        strings[i] += char_to_use
  return strings


# COLORPRINT

prevprint = print


def fg(color=None):
  """returns ascii escape for foreground colors

  Args:
    color (str, optional): the number of the collor to get. Defaults to None - if none return the remove color sequence instead.

  Returns (str): ascii escape for foreground colors
  """
  return "\33[38;5;" + str(color) + "m" if color else "\u001b[0m"


def bg(color=None):
  """returns ascii escape for background colors

  Args:
    color (str, optional): the number of the collor to get. Defaults to None - if none return the remove color sequence instead.

  Returns (str): ascii escape for background colors
  """
  return "\33[48;5;" + str(color) + "m" if color else "\u001b[0m"


def getcolor(color):
  """will make better later

  Args:
    color (string): one of the set colors

  Raises (ValueError): if color is not a valid color

  Returns (str): an ascii escape sequence of the color
  """
  # if plainprint:
  #     return ""
  match color.lower():
    case "end":
      return "\x1b[0m"
    case "nc":
      return "\x1b[0m"
    case "red":
      return fg(1) or "\033[0m"
    case "purple":
      return fg(92)
    case "blue":
      return fg(19)
    case "green":
      return fg(28)
    case "magenta":
      return fg(90)
    case "bright blue":
      return fg(27)
    case "yellow":
      return fg(3)
    case "bold":
      return "\033[1m"
    case "underline":
      return "\033[4m"
    case "white":
      return fg(15)
    case "cyan":
      return fg(45) or "\033[96m"
    case "orange":
      return fg(208)
    case "pink":
      return fg(213)
    case _:
      raise ValueError(f"{color} is not a valid color")


def listcolors():
  """
  Print a table of colors.
  """
  for row in range(-1, 42):

    def print_six(row, format):
      for col in range(6):
        color = row * 6 + col + 4
        if color >= 0:
          text = "{:3d}".format(color)
          print(format(color) + text + getcolor("END"), end=" ")
        else:
          print("   ", end=" ")

    print_six(row, fg)
    print("", end=" ")
    print_six(row, bg)
    print()


def logfile(
  type, *data, sep: str | None = " ", end: str | None = "\n", format: bool = True
):
  if not args.has("log"):
    return
  if not sep:
    sep = " "
  if not end:
    end = "\n"
  if end != "\n":
    type = ""
  else:
    type += " "
  if format:
    data = sep.join(map(formatitem, data))
  else:
    data = sep.join(map(str, data))
  dir = os.path.join(MAIN_FILE_DIR, "logs")
  if not os.path.exists(dir):
    os.makedirs(dir)
  f.append(
    os.path.join(dir, LOG_FILE_NAME),
    type + data + getcolor("end") + end,
    encoding="utf-8",
  )


# re.sub(r"\[\d+m", "", data)


class print:
  c = (lambda x: "") if args.has("pp") else getcolor
  showdebug = True
  showinfo = False
  defaultiscolor = True

  @staticmethod
  def plain(
    *a,
    sep: str | None = " ",
    end: str | None = "\n",
    file=None,
    flush=False,
  ):
    logfile(f"{fg(213)}[plain]", *a, sep=sep, end=end)
    prevprint(*map(str, a), sep=sep, end=end, file=file, flush=flush)

  @staticmethod
  def color(
    *a,
    sep: str | None = " ",
    end: str | None = "\n",
    file=None,
    flush=False,
  ):
    logfile(f"{fg(213)}[color]", *a, sep=sep, end=end)
    prevprint(
      *map(bind(formatitem, nocolor=args.has("pp")), a),
      print.c("END"),
      sep=sep,
      end=end,
    )

  @staticmethod
  def __init__(
    *a,
    sep: str | None = " ",
    end: str | None = "\n",
    file=None,
    flush=False,
  ):
    logfile("[default]", *a, sep=sep, end=end, format=print.defaultiscolor)

    if print.defaultiscolor:
      prevprint(
        *map(bind(formatitem, nocolor=args.has("pp")), a),
        print.c("END"),
        sep=sep,
        end=end,
      )
    else:
      prevprint(*a, sep=sep, end=end)

  @classmethod
  def debug(
    cls,
    *a,
    sep: str | None = " ",
    end: str | None = "\n",
    file=None,
    flush=False,
  ):
    if not cls.showdebug:
      return
    logfile(
      f"{getcolor("BLUE")}{getcolor("BOLD")}[DEBUG]{getcolor("END")}",
      *a,
      sep=sep,
      end=end,
    )

    prevprint(
      f"{print.c("BLUE")}{print.c("BOLD")}[DEBUG]{print.c("END")}",
      *map(bind(formatitem, nocolor=args.has("pp")), a),
      print.c("END"),
      sep=sep,
      end=end,
      file=file,
      flush=flush,
    )

  @classmethod
  def info(
    cls,
    *a,
    sep: str | None = " ",
    end: str | None = "\n",
    file=None,
    flush=False,
  ):
    if not cls.showinfo:
      return
    logfile(
      f"{getcolor("bright blue")}{getcolor("BOLD")}[INFO]{getcolor("END")}",
      *a,
      sep=sep,
      end=end,
    )

    prevprint(
      f"{print.c("bright blue")}{print.c("BOLD")}[INFO]{print.c("END")}",
      *map(bind(formatitem, nocolor=args.has("pp")), a),
      print.c("END"),
      sep=sep,
      end=end,
      file=file,
      flush=flush,
    )

  @staticmethod
  def warn(
    *a,
    sep: str | None = " ",
    end: str | None = "\n",
    file=None,
    flush=False,
  ):
    logfile(
      f"{getcolor("YELLOW")}{getcolor("BOLD")}[WARNING]{getcolor("END")}",
      *a,
      sep=sep,
      end=end,
    )

    prevprint(
      f"{print.c("YELLOW")}{print.c("BOLD")}[WARNING]{print.c("END")}",
      *map(bind(formatitem, nocolor=args.has("pp")), a),
      print.c("END"),
      sep=sep,
      end=end,
      file=file,
      flush=flush,
    )

  @staticmethod
  def error(
    *a,
    sep: str | None = " ",
    end: str | None = "\n",
    file=None,
    flush=False,
  ):
    logfile(
      f"{getcolor("RED")}{getcolor("BOLD")}[ERROR]{getcolor("END")}",
      *a,
      sep=sep,
      end=end,
    )

    prevprint(
      f"{print.c("RED")}{print.c("BOLD")}[ERROR]{print.c("END")}",
      *map(bind(formatitem, nocolor=args.has("pp")), a),
      print.c("END"),
      sep=sep,
      end=end,
      file=file,
      flush=flush,
    )

  @staticmethod
  def success(
    *a,
    sep: str | None = " ",
    end: str | None = "\n",
    file=None,
    flush=False,
  ):
    logfile(
      f"{getcolor("GREEN")}{getcolor("BOLD")}[SUCCESS]{getcolor("END")}",
      *a,
      sep=sep,
      end=end,
    )
    prevprint(
      f"{print.c("GREEN")}{print.c("BOLD")}[SUCCESS]{print.c("END")}",
      *map(bind(formatitem, nocolor=args.has("pp")), a),
      print.c("END"),
      sep=sep,
      end=end,
      file=file,
      flush=flush,
    )


def formatitem(item, tab=-2, isarrafterdict=False, nocolor=False):
  """formats data into a string

  Args:
    item (any): the item to format
    tab (): - DONT SET MANUALLY
    isarrafterdict (): - DONT SET MANUALLY

  Returns (str): the formatted string
  """

  class _class:
    pass

  def _func():
    pass

  def stringify(obj):
    def replace_unstringables(value):

      if type(value) in [type(_func), type(_class)]:
        return f"<{value.__name__}>"
      return value

    def convert(obj):
      if isinstance(obj, dict):
        return {k: convert(v) for k, v in obj.items()}
      if isinstance(obj, list):
        return [convert(v) for v in obj]
      return replace_unstringables(obj)

    return oldjson.dumps(convert(obj))

  wrapat = 80
  tab += 2
  TYPENAME = ""
  c = (lambda x: "") if nocolor else getcolor
  try:
    # print.plain(item, tab)
    if item == True and type(item) == type(True):
      return "true"
    if item == False and type(item) == type(False):
      return "false"
    if type(item) in [type(_class), type(_func)]:
      return f"{c("RED")}<{"class" if type(item)==type(_class) else "function"} {c("BOLD")}{c("BLUE")}{item.__name__}{c("END")}{c("RED")}>{c("END")}" # type: ignore
    if isinstance(item, str):
      return (
        c("purple")
        + '"'
        + str(item).replace("\\", "\\\\").replace('"', '\\"')
        + '"'
        + c("END")
      )
    if isinstance(item, int) or isinstance(item, float):
      item = str(item)
      reg = [r"(?<=\d)(\d{3}(?=(?:\d{3})*(?:$|\.)))", r",\g<0>"]
      if "." in item:
        return (
          c("GREEN")
          + re.sub(reg[0], reg[1], item.split(".")[0])
          + "."
          + item.split(".")[1]
          + c("END")
        )
      return c("GREEN") + re.sub(reg[0], reg[1], item) + c("END")
      # Σ╘╬╧╨╤╥╙╘╒╓╖╕╔╛╙╜╝╚╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬╭╮╯╰╱╲╳╴╵╶╷╸╹╺╻╼╽╾╿

    def name(item):
      try:
        return f'{c("pink")}╟{item.__name__}╣{c("END")}'
        # return f'{c("pink")}╟{item.__name__}╿{item.__class__.__name__}╣{c("END")}'
      except:
        return f'{c("pink")}╟{item.__class__.__name__}╣{c("END")}'

    # TYPENAME=name(item)

    if not (isinstance(item, dict) or isinstance(item, list)):
      if isinstance(item, tuple):
        TYPENAME = name(item)
      else:
        try:
          temp = [*item]
          TYPENAME = name(item)
          item = temp
        except:
          try:
            temp = {**item}
            TYPENAME = name(item)
            item = temp
          except:
            pass

    if isinstance(item, dict):
      strlen = 9999999
      try:
        strlen = len(stringify(item))
      except Exception as e:
        pass
      if not len(item):
        return f"{c("orange")}{'{}'}{c("END")}"
      if strlen + tab < wrapat:
        return (
          TYPENAME
          + c("orange")
          # + "\n"
          + (" " * tab if not isarrafterdict else "")
          + "{ "
          + c("END")
          + (
            f"{c("orange")},{c("END")} ".join(
              f"{c("purple")+(f'"{k}"' if isinstance(k, str) else formatitem(k, 0))+c("END")}{c("orange")}:{c("END")} {formatitem(v, 0, True)}"
              for k, v in item.items()
            )
          )
          + c("orange")
          + " }"
          + c("END")
        )
      else:
        return (
          TYPENAME
          + c("orange")
          # + "\n"
          + (" " * tab if not isarrafterdict else "")
          + "{"
          + c("END")
          + "\n  "
          + (
            f"{c("orange")},{c("END")}\n  ".join(
              f"{c("purple")+(" "*tab)+(f'"{k}"' if isinstance(k, str) else formatitem(k, tab))+c("END")}{c("orange")}:{c("END")} {formatitem(v, tab, True)}"
              for k, v in item.items()
            )
          )
          + "\n"
          + c("orange")
          + " " * tab
          + "}"
          + c("END")
        )
    if isinstance(item, list):
      strlen = 9999999
      try:
        strlen = len(stringify(item))
      except Exception as e:
        pass
      if not len(item):
        return f'{c("orange")}[]{c("END")}'
      if strlen + tab < wrapat:
        return (
          TYPENAME
          + c("orange")
          + ("" if isarrafterdict else " " * tab)
          + "[ "
          + c("END")
          + (
            f"{c("orange")},{c("END")} ".join(
              map(
                lambda newitem: formatitem(newitem, -2),
                item,
              )
            )
          )
          + c("orange")
          + " ]"
          + c("END")
        )
      else:
        return (
          TYPENAME
          + c("orange")
          + ("" if isarrafterdict else " " * tab)
          + "[\n"
          + c("END")
          + (
            f"{c("orange")},{c("END")}\n".join(
              map(
                lambda newitem: (
                  "  " + " " * tab
                  if isinstance(newitem, str)
                  or isinstance(newitem, int)
                  or isinstance(newitem, float)
                  else ""
                )
                + formatitem(newitem, tab),
                item,
              )
            )
          )
          + c("orange")
          + "\n"
          + " " * tab
          + "]"
          + c("END")
        )

    return " " * tab + name(item) + '"' + str(item).replace('"', '\\"') + '"'
  except Exception as e:
    print.plain(e)
    return " " * tab + f"{c("red")}{repr(item)}{c("end")}"


logfile(f"{fg(30)}---PROGRAM STARTED---{fg()}")
logfile(f"{fg(30)}[ARGS]{fg()}", sys.argv)
# END


import configparser
from os import system
from typing import Optional, Union
import os, shutil

import colorama
from PIL import Image
import sys
import ctypes


class Error(Exception):
  """Base class for all FolderIkon errors."""

  color = False

  def __repr__(self):
    return self.red(self.__doc__)

  @staticmethod
  def red(string):
    if Error.color:
      return colorama.Fore.RED + string
    return string


class DesktopIniError(Error):
  """The 'desktop.ini' file could not be parsed. Delete it and try again."""

  def __init__(self, exc):
    self.__exc = exc
    super().__init__()

  def __repr__(self):
    exc_name = self.__exc.__class__.__name__
    exc_info = f"An exception of {exc_name} occurred when parsing it."
    return super().__repr__() + " " + exc_info


def exception_exit(exc):
  raise exc
  # print(repr(exc()))
  # sys.exit(-1)


"""Win32 API function **SHChangeNotify**.
https://docs.microsoft.com/windows/win32/api/shlobj_core/nf-shlobj_core-shchangenotify

Only required constants are defined.
"""


SHCNE_ASSOCCHANGED = 0x08000000
SHCNF_IDLIST = 0x0000

__all__ = ["notify_shell"]


def notify_shell():
  """Request the Windows shell to invalidate icon cache and rebuild it.
  See https://docs.microsoft.com/windows/win32/api/shlobj_core/nf-shlobj_core-shchangenotify#remarks.
  """

  ctypes.windll.shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, 0, 0)


class FolderIkon:
  def __init__(self, args):
    self.__image: Union[str, Path, None] = args.image
    self.__icon: Optional[str] = args.icon
    self.__parent: Union[str, Path] = args.parent
    self.__delete_original: Optional[bool] = args.delete_original
    # self.__raise_on_existing: Optional[bool] = args.raise_on_existing
    self.__dont_hide_icon: Optional[bool] = args.dont_hide_icon
    self.__no_color: Optional[bool] = args.no_color

    self.parent = self.__parent

  def iconize(self):
    if not self.__no_color:
      colorama.init(autoreset=True)

    if isinstance(self.__image, str):
      pass
    else:
      # Image is a local path or default argument
      self.image = Path(self.__image) # type: ignore

    if self.__icon:
      if self.parent == Path.cwd():
        self.parent = Path(self.__icon).parent
      self.icon = Path(self.__icon)
      if not self.icon.is_absolute():
        self.icon = self.parent / self.icon
    else:
      self.icon = self.image.with_suffix(".ico")
      # if self.icon.exists() and self.__raise_on_existing:
      #     exception_exit(FolderIconAlreadyExistsError)

    if not self.image.suffix == ".ico":
      if self.icon.exists():
        # if self.__raise_on_existing:
        #     exception_exit(FolderIconAlreadyExistsError)
        self.icon.unlink()
      with Image.open(self.image) as img:
        img.save(self.icon, bitmap_format="bmp")

    self.conf = self.parent / Path("desktop.ini")
    conf_existed = False
    if self.conf.exists():
      conf_existed = True
      system('attrib -r -h -s "%s"' % str(self.conf))
    else:
      open(self.conf, "x").close()
    config = configparser.ConfigParser()
    try:
      config.read(self.conf)
    except configparser.Error as exc:
      fp.close() # type: ignore
      if not conf_existed:
        self.conf.unlink()
      self.icon.unlink()
      system('attrib +h +s "%s"' % str(self.conf))
      exception_exit(DesktopIniError(exc))
    with open(self.conf, "w") as fp:
      if ".ShellClassInfo" not in config:
        config.add_section(".ShellClassInfo")
      name = str(self.icon.name)
      section = config[".ShellClassInfo"]
      section["IconResource"] = "%s,0" % name
      config.write(fp, space_around_delimiters=False)

    if not self.__dont_hide_icon:
      system('attrib +h "%s"' % str(self.icon))
    system('attrib +h +s "%s"' % str(self.conf))
    system('attrib +r "%s"' % str(self.parent))

    notify_shell()
    if self.__delete_original and self.image != self.icon:
      self.image.unlink()


def setfoldericon(dir, imgpath):
  try:
    dir = os.path.abspath(dir)
    if not (Path(imgpath).is_file() and Path(dir).is_dir()):
      print.error(f'failed to update "{dir}"')
      return False
    if Path(os.path.join(dir, "foldericon.ico")).is_file():
      oldfilebin = f.read(os.path.join(dir, "foldericon.ico"), asbinary=True)
      newfilebin = f.read(imgpath, asbinary=True)
      if newfilebin == oldfilebin:
        # print.error(f'"{dir}" is already using "{imgpath}"')
        # return False
        return True
    try:
      os.remove(os.path.join(dir, "foldericon.ico"))
    except Exception:
      pass
    shutil.copy(imgpath, os.path.join(dir, "foldericon.ico"))

    class temp:
      image = os.path.join(dir, "foldericon.ico")
      icon = Path(os.path.join(dir, "foldericon.ico"))
      parent = Path(dir)
      delete_original = False
      raise_on_existing = False
      dont_hide_icon = False
      no_color = False

    workdir = os.getcwd()
    os.chdir(dir)
    fi = FolderIkon(temp)
    fi.image = Path(os.path.join(dir, "foldericon.ico"))
    fi.iconize()
    os.chdir(workdir)
    return True
  except Exception as e:
    print.error(f'failed to update "{dir}"')
    print.error(e)
    return False


def joinObjs(*objs, newOnly=False) -> dict:
  obj1 = objs[0]
  for obj in objs[1:]:
    for key, val in obj.items():
      if newOnly and hasattr(obj1, key):
        continue
      obj1[key] = val
  return obj1


class OptObj:
  # def __iter__(self):
  #     return self.__dict__.__iter__()

  def __init__(self, obj, default=0):
    self.__dict__ = copy.deepcopy(obj)
    self._default = default

  def __getattribute__(self, name: str):
    if name in super().__getattribute__("__dict__"):
      return super().__getattribute__("__dict__")[name]
    else:
      return super().__getattribute__("_default")

  def __repr__(self) -> str:
    return repr(super().__getattribute__("__dict__"))


def setclip(data):
  win32clipboard.OpenClipboard()
  win32clipboard.EmptyClipboard()
  win32clipboard.SetClipboardText(data) # type: ignore
  win32clipboard.CloseClipboard()


def getclip():
  win32clipboard.OpenClipboard()
  data = win32clipboard.GetClipboardData() # type: ignore
  win32clipboard.CloseClipboard()
  return data


class LLM:
  def __init__(self, model=None):
    self.ctx = []
    self.model = "llama3.1:8b" if model is None else model

  def ask(self, prompt):
    res = requests.post(
      url="http://127.0.0.1:11434/api/generate",
      json={
        "model": self.model,
        "prompt": prompt,
        "stream": False, # Use boolean False instead of string "false"
        "context": self.ctx,
        # "format": "json",
      },
    ).json()
    self.ctx = res["context"]
    return res["response"]
    # return json.parse(res["response"])

  def clear(self):
    self.ctx = []

  def __call__(self, prompt):
    return self.ask(prompt)
