'D=Time
'answer=MsgBox(D,0,"Example")
'Set objShell = CreateObject("Wscript.Shell")
'objShell.Run("https://t.bilibili.com/")
set objTTS = createobject("sapi.spvoice")
for i = 1 to 1
    objTTS.speak "Á¬Ó¾öÎ ÊÇ¸öÉµ±Æ"
Next