#!/usr/bin/python
import re
import sys
from optparse import OptionParser

parser = OptionParser(usage="https://www.youtube.com/watch?v=ioWC-sT0iZI")
parser.add_option("-t", dest="input_target", type="string", help="target string for conversion")
parser.add_option("--auto",dest="auto", action="store_true", default=False, help="add auto open/close strings if you are doing macro things")
parser.add_option("--target",dest="target", type="int", default=2, help="it's a clamav target, it's a number")
parser.add_option("-s", dest="sname", type="string", help="the sig name dumb-dumb")
parser.add_option("-i",dest="i", action="store_false", default=True, help="Disable case insensitive matches")
parser.add_option("-a",dest="a", action="store_true", default=False, help="Enable ascii flag default is false")
parser.add_option("-w",dest="w", action="store_true", default=False, help="Enable wide flag default is false")
parser.add_option("-f",dest="f", action="store_true", default=False, help="Enable fullword flag default is false")
parser.add_option("--or",dest="do_or", action="store_true", default=False, help="Make an or set of matches instead of and")

(options, args) = parser.parse_args()
strings = options.input_target.split(",")
strings2 = []
autostrings2 = []
autostrings = ["Document_Open","Document_Close","Worksheet_Open","Auto_Open","AutoOpen","Workbook_Open","Auto_Close","AutoClose"]

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
for entry in strings:
    strings2.append(entry.encode("hex"))
if not strings:
   print "need a set of target strings via -t"
   sys.exit(-1)

if not options.sname:
   print "need a signame via -s"
   sys.exit(-1)

sig = options.sname + ";Target:%s;(" % (options.target)
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
    sig = sig[:-1]
    sig = sig + "));"
else:
    sig = sig[:-1]
    sig = sig + ");"

optstr = build_opt_string()
optstr3b = optstr + ";"
sig = sig +  optstr3b.join(strings2) + optstr
if options.auto:
    sig = sig + ";" + optstr3b.join(autostrings2) + optstr
print sig
