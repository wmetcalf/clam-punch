#!/usr/bin/python
import re
import sys
from optparse import OptionParser
targetstring="""0 = any file\n
1 = Portable Executable, both 32- and 64-bit.;\n
2 = file inside OLE2 container (e.g. image, embedded executable, VBA;\n
script). The OLE2 format is primarily used by MS Office and MSI installa-tion files.;\n
3 = HTML (normalized: whitespace transformed to spaces, tags/tag at-tributes normalized, all lowercase), Javascript is normalized too: all strings
are normalized (hex encoding is decoded), numbers are parsed and normal-ized, local variables/function names are normalized to n001 format, argu-ment to eval() is parsed as JS again, unescape() is handled, some simple JS packers are handled, output is whitespace normalized.;\n
4 = Mail file;\n
5 = Graphics;\n
6 = ELF;\n
7 = ASCII text file (normalized);\n
8 = Unused;\n
9 = Mach-O files;\n
10 = PDF files;\n
11 = Flash files;\n
12 = Java class files;"""
parser = OptionParser(usage="https://www.youtube.com/watch?v=ioWC-sT0iZI")
parser.add_option("-t", dest="input_target", type="string", help="target string for conversion")
parser.add_option("--auto",dest="auto", action="store_true", default=False, help="add auto open/close strings if you are doing macro things")
parser.add_option("--target",dest="target", type="int", default=2, help="it's a clamav target, it's a number. From clamav man:%s" % (targetstring))
parser.add_option("-s", dest="sname", type="string", help="the sig name dumb-dumb")
parser.add_option("-i",dest="i", action="store_false", default=True, help="Disable case insensitive matches")
parser.add_option("-a",dest="a", action="store_true", default=False, help="Enable ascii flag default is false")
parser.add_option("-w",dest="w", action="store_true", default=False, help="Enable wide flag default is false")
parser.add_option("-f",dest="f", action="store_true", default=False, help="Enable fullword flag default is false")
parser.add_option("--or",dest="do_or", action="store_true", default=False, help="Make an or set of matches instead of and")
parser.add_option("--ppstr",dest="ppstr", action="store_true", default=False,help="prepend single byte strlen")
parser.add_option("--wide",dest="wide", action="store_true", default=False,help="convert all strings to wide matches useful as it seems clamav does global matching with ::w option")
parser.add_option("--exeprime",dest="exeprime",action="store_true",default=False,help="add process execution primitives observed in macros")
(options, args) = parser.parse_args()
strings = options.input_target.split(",")
strings2 = []
autostrings2 = []
execution_primitives2 = []
autostrings = ["InkPicture1_Painted","AutoExec","AutoOpen","Auto_Open","AutoClose","Auto_Close","AutoExit","AutoNew","DocumentOpen","Document_Open","DocumentClose","Document_Close","DocumentBeforeClose","DocumentChange","Document_New","NewDocument","Workbook_Open","WorkbookOpen","Workbook_Activate","Workbook_Close"]
execution_primitives =[".run","shell","SHCreateThread","RtlMoveMemory","WriteProcessMemory","WriteVirtualMemory","CallWindowProc","EnumResourceTypes","EnumSystemLanguageGroups","EnumUILanguages","EnumDateFormats","EnumCalendarInfo","EnumTimeFormats","SHCreateThread","GrayString","CreateTimerQueueTimer","CreateProcess","Win32_Process","MacScript","WinExec"]
def build_opt_string():
    optstr = ""
    if options.i or options.a or options.w or options.f:
        optstr = optstr + "::"
        if options.i:
            optstr = optstr + "i"
        if options.a:
            optstr = optstr + "a"
        if options.w:
            optstr = optstr + "w"
        if options.f:
            optstr = optstr + "f"            
    return optstr

for entry in autostrings:
    autostrings2.append(entry.encode("hex"))
for entry in execution_primitives:
    execution_primitives2.append(entry.encode("hex"))
for entry in strings:
    if options.ppstr and len(entry) < 255:
        strlen = "%0.2X" % len(entry)
        strings2.append("%s%s" % (strlen,entry.encode("hex")))
    elif options.wide:
        i = 0
        newstr = ""
        while i < len(entry):
           newstr = newstr + "00{0}".format(entry[i].encode("hex"))
           i = i + 1
        strings2.append(newstr)
    else:
        strings2.append(entry.encode("hex"))
if not strings:
   print "need a set of target strings via -t"
   sys.exit(-1)

if not options.sname:
   print "need a signame via -s"
   sys.exit(-1)

sig = options.sname + ";Engine:81-255,Target:%s;(" % (options.target)
if options.do_or:
    sig = sig + "("
i = 0
while i < len(strings2):
    if options.do_or:
         sig = sig + "%s|" % (i)
    else:
         sig = sig + "%s&" % (i)
    i = i + 1

if options.auto:
    if options.do_or:
        sig = sig[:-1]
        sig = sig + ")&("
    else:
        sig = sig + "(" 
    while i < (len(strings2) + len(autostrings2)):
        sig = sig + "%s|" % (i)
        i = i + 1
    if options.exeprime:
        sig = sig[:-1]
        sig = sig + ")&("
        while i < (len(strings2) + len(autostrings2) + len(execution_primitives2)):
            sig = sig + "%s|" % (i)
            i = i + 1
    sig = sig[:-1]
    sig = sig + "));"
elif options.exeprime:
    if options.do_or:
        sig = sig[:-1]
        sig = sig + ")&("
    else:
        sig = sig + "("
    while i < (len(strings2) + len(execution_primitives2)):
        sig = sig + "%s|" % (i)
        i = i + 1
    sig = sig[:-1]
    sig = sig + "));"

else:
    sig = sig[:-1]
    sig = sig + ");"

optstr = build_opt_string()
optstr3b = optstr + ";"
sig = sig +  optstr3b.join(strings2) + optstr
if options.auto:
    sig = sig + ";" + "::i;".join(autostrings2) + "::i"
    if options.exeprime:
        sig = sig + ";" + "::i;".join(execution_primitives2) + "::i"
elif options.exeprime:
    sig = sig + ";" + "::i;".join(execution_primitives2) + "::i"
sig=re.sub(r'(?<!2a)2a2a2a2a(?!2a)',r'*',sig)
print sig
