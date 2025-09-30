import os, sys,re
from pathlib import Path


# cd c:\users\user & pyinstaller --noconfirm --onefile --console --icon "C:\Users\User\Desktop\file sorter\icons\icon.ico"  "C:\Users\User\Desktop\file sorter\setfoldericon.py"
# cd c:\users\user ; pyinstaller --noconfirm --onefile --console --icon "C:\Users\User\Desktop\file sorter\icons\icon.ico"  "C:\Users\User\Desktop\file sorter\setfoldericon.py"
cmdargs = []
a_args = {}





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
  def sucess(
    *a,
    sep: str | None = " ",
    end: str | None = "\n",
    file=None,
    flush=False,
  ):
    logfile(
      f"{getcolor("GREEN")}{getcolor("BOLD")}[SUCESS]{getcolor("END")}",
      *a,
      sep=sep,
      end=end,
    )
    prevprint(
      f"{print.c("GREEN")}{print.c("BOLD")}[SUCESS]{print.c("END")}",
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
    tab (): - DONT SET MANUALY
    isarrafterdict (): - DONT SET MANUALY

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
      return f"{c("RED")}<{"class" if type(item)==type(_class) else "function"} {c("BOLD")}{c("BLUE")}{item.__name__}{c("END")}{c("RED")}>{c("END")}"  # type: ignore
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
      if not len(item):
        return "{}"
      if len(stringify(item)) + tab < wrapat:
        return (
          TYPENAME
          + c("orange")
          # + "\n"
          + (" " * tab if not isarrafterdict else "")
          + "{ "
          + c("END")
          + (
            f"{c("orange")},{c("END")} ".join(
              f"{c("purple")+(f'"{k}"' if isinstance(k, str) else formatitem(k, tab))+c("END")}{c("orange")}:{c("END")} {formatitem(v, tab, True)}"
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
      if len(stringify(item)) + tab < wrapat:
        return (
          TYPENAME
          + c("orange")
          + ("" if isarrafterdict else " " * tab)
          + "[ "
          + c("END")
          + (
            f"{c("orange")},{c("END")} ".join(
              map(
                lambda newitem: formatitem(newitem, tab),
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


def sfi():
  def getimg(path, dir):
    if not path.endswith(".ico"):
      path = path + ".ico"
    if Path(os.path.abspath(path)).is_file():
      return os.path.abspath(path)
    if Path(os.path.abspath(os.path.join(dir, path))).is_file():
      return os.path.abspath(os.path.join(dir, path))
    return False

  if not args.has("p"):
    print.error(
      "No path specified! Please specify a path to the folder you want to add an icon to."
    )
    sys.exit(-1)
  if args.has("i"):
    for path in args.get("p"):
      icon = args.get("i")[0]
      img = getimg(icon, path)
      if not img:
        print.error(f'"{os.path.abspath(icon)}" is not a file')
      if setfoldericon(path, img):
        print.sucess(f'icon updated for "{path}"')

  else:
    for path in args.get("p"):
      path = os.path.abspath(path)
      if Path(os.path.join(path, "desktop.ini")).exists():
        os.remove(os.path.join(path, "desktop.ini"))
      else:
        print.error(f'"{path}" has no icon')
      if Path(os.path.join(path, "foldericon.ico")).exists():
        os.remove(os.path.join(path, "foldericon.ico"))
      else:
        print.error(f'"{path}" has no icon')
      os.system('attrib -r "%s"' % str(path))
      print.sucess(f'icon removed for "{path}"')
  return 0

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
      self.image = Path(self.__image)  # type: ignore

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
      fp.close()  # type: ignore
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

