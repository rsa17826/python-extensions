#Requires AutoHotkey v2.0
#SingleInstance Force

; must include
#Include *i <AutoThemed>
#include <vars>

#Include <base> ; Array as base, Map as base, String as base, File as F, JSON

#Include <Misc> ; print, range, swap, ToString, RegExMatchAll, Highlight, MouseTip, WindowFromPoint, ConvertWinPos, WinGetInfo, GetCaretPos, IntersectRect

; MsgBox(JSON.stringify("hjajkasdjksadsd"))
; try MsgBox(JSON.stringify(A_Args))
; try MsgBox(JSON.stringify(A_Args.sub(4, -1)))
if !(A_Args.Has(3))
  return
SetWorkingDir(A_Args[2])
cmd := 'python' (A_Args[3] = "hide" ? "w" : "") ' "' A_Args[1] '"'
args := ""
for arg in A_Args.sub(4, -1) {
  args .= ' "' . StrReplace(arg, '"', '\"') . '"'
}
run(cmd args)