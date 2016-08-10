#!/usr/bin/python
import re
import sys
from optparse import OptionParser

parser = OptionParser(usage="https://www.youtube.com/watch?v=ioWC-sT0iZI")
parser.add_option("-t", dest="input_target", type="string", help="target string for conversion")
parser.add_option("-a",dest="auto", action="store_true", default=False, help="add auto open/close strings if you are doing macro things")
parser.add_option("--target",dest="target", type="int", default=2, help="it's a clamav target, it's a number")
parser.add_option("-s", dest="sname", type="string", help="the sig name dumb-dumb")
(options, args) = parser.parse_args()
strings = options.input_target.split(",")
strings2 = []
autostrings2 = []
autostrings = ["Document_Open","Document_Close","Worksheet_Open","Auto_Open","AutoOpen","Workbook_Open","Auto_Close","AutoClose"]

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
i = 0
while i < len(strings2):
    sig = sig + "%s&" % (i)
    i = i + 1
if options.auto:
    sig = sig + "("
    while i < (len(strings2) + len(autostrings2)):
        sig = sig + "%s|" % (i)
        i = i + 1
    sig = sig[:-1]
    sig = sig + "));"
else:
    sig = sig[:-1]
    sig = sig + ");"
sig = sig +  "::i;".join(strings2) + "::i"
if options.auto:
    sig = sig + ";" +  "::i;".join(autostrings2) + "::i"
print sig
