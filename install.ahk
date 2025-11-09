#Requires AutoHotkey v2.0
#SingleInstance Force

; must include
#Include *i <AutoThemed>
#include <vars>

#Include <base> ; Array as base, Map as base, String as base, File as F, JSON

#Include <Misc> ; print, range, swap, ToString, RegExMatchAll, Highlight, MouseTip, WindowFromPoint, ConvertWinPos, WinGetInfo, GetCaretPos, IntersectRect
SetWorkingDir(A_ScriptDir)

args := 'cd "' A_ScriptDir '" & '
loop files "*.*", "d" {
  if A_LoopFileName.startsWith('.')
    continue
  args .= 'echo y|pip uninstall ' A_LoopFileName ' & pip install ./' A_LoopFileName ' & '
}

lastclip := A_Clipboard
A_Clipboard := args.replace("&", "`;") '`n'
if winactive("ahk_exe vscodium.exe") {
  send("^+~")
  Sleep(100)
  Send("{enter}")
  Sleep(100)
  Send("{enter}{enter}")
  Sleep(100)
  send("^v")
  Sleep(5000)
  A_Clipboard := lastclip
}
; Runwait("cmd /c `"" args " & pause`"", A_ScriptDir)
; cmd.run(args, '')
;  pip install f args ; echo y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y|pip uninstall colorprint args f
;  echo y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y|pip uninstall colorprint args f six; pip install --no-cache ./f ./args ./colorprint

; hatch new f
