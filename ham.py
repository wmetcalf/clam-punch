#!/usr/bin/python
try:
    import re2 as re
except ImportError:
    import re
import binascii
import sys
from optparse import OptionParser
import glob
import os
try:
    from cisco.bass.algorithms import hamming_klcs
    from cisco.bass.algorithms import ndb_from_common_sequence
    HAVE_BASS = True
except:
    HAVE_BASS = False

if not HAVE_BASS:
    print("You must be all about that b.a.s.s.... https://github.com/Cisco-Talos/BASS/tree/master/bass\nsudo yum -y install graphviz graphviz-devel\ngit clone https://github.com/Cisco-Talos/BASS.git\ncd BASS/bass/python\nsudo python setup.py install")
    sys.exit(0)

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
parser = OptionParser(usage="https://www.youtube.com/watch?v=nLB4dU3Yc6M\nexample:\n\n./ham.py -i --maxsplit=500 --normwhite --target=7 -P '.{0,500}(?i)ActiveXObject.{0,500}' -s LockyJS -d /home/coz/Downloads/LockyJS")
parser.add_option("-s", dest="sname", type="string", help="the sig name dumb-dumb")
parser.add_option("-d", dest="dir", type="string", help="dir of similar samples to H.A.M")
parser.add_option("-f", dest="input_file", type="string", help="will read a LF seperated file and treat each line as a seperate string to HAM")
parser.add_option("-P", dest="i_re", type="string", help="Must match this regex to be included as input string '(?i).{0,100}poopship.{0,500}")
parser.add_option("--target",dest="target", type="int", default=2, help="it's a clamav target, it's a number. From clamav man:%s" % (targetstring))
parser.add_option("--normwhite",dest="normwhite", action="store_true", default=False, help="Some targets clamav will normalize whitespace in the backgroup, so do the same")
parser.add_option("--maxsplit",dest="maxsplit", type="int", default=0, help="remove wildcards from sig replace with max distance format like {0-500} where --maxplit=500")
parser.add_option("--seqrepl",dest="seqrepl", type="int", default=0,help="replace repeating byte sequences longer than argument with length of sequence minumum of 8.Good starting value might be 20")
parser.add_option("-i",dest="nocase", action="store_true", default=False,help="make the resulting sig nocase")
parser.add_option("-l",dest="lwsom", action="store_true", default=False,help="make the resulting sig nocase")
(options, args) = parser.parse_args()

include_regex = None
target_strings = []
matches = []
misses = []

if options.i_re:
    try:
        include_regex = re.compile(options.i_re,re.S)
    except Exception as e:
        print("Error Compiling Include Regex" % (e))
        sys.exit(-1)

if options.input_file and os.path.exists(options.input_file):
    lines=open(options.input_file).readlines()
    if not lines:
        print "empty input file exiting"
        sys.exit(-1)
    lines = sorted(lines, key=len)
    print("The number of lines in the list is: %s." % (len(lines)))
    print("The shortest line in the list is: %s." % (len(lines[0])))
    print("The longest line in the list is: %s." % (len(lines[-1])))
    for dapoop in lines:
        if options.normwhite:
            dapoop = re.sub(r'[\r\n\s\t]+',"\x20",dapoop)
        if options.nocase:
            dapoop = dapoop.lower()
        if include_regex:
            m=include_regex.search(dapoop)
            if m and m.group(0) not in target_strings:
                dapoop2=m.group(0)
                target_strings.append(dapoop2)
        elif dapoop not in target_strings:
            target_strings.append(dapoop)

elif(options.dir):
    flist = []
    if os.path.isdir(options.dir):
        flist = glob.glob(options.dir + "/*")
    else:
       print("print you gotta provdie a dir dawg")
       sys.exit(-1)
    if len(flist) > 1:
        for entry in flist:
            print entry
            dapoop=open(entry).read()
            if options.normwhite:
                dapoop = re.sub(r'[\r\n\s\t]+',"\x20",dapoop)
            if options.nocase:
                dapoop = dapoop.lower()
            if include_regex:
                m=include_regex.search(dapoop)
                if m and m.group(0) not in target_strings:
                    target_strings.append(m.group(0))
                    matches.append(entry)
                else:
                    misses.append(entry)

            elif dapoop not in target_strings:
                target_strings.append(dapoop)
print "finished loading files"
if not options.sname:
   print "need a signame via -s"
   sys.exit(-1)

sig = options.sname + ";Engine:81-255,Target:%s;(0);" % (options.target)
if include_regex:
    for entry in matches:
        print("match: {0}".format(entry))
    for entry in misses:
        print("miss: {0}".format(entry))
    print("Matches:{0}, Misses:{1}\n".format(len(matches),len(misses)))

if include_regex:
    for entry in matches:
        print("match: {0}".format(entry)) 
    for entry in misses:
        print("miss: {0}".format(entry))
    print("Matches:{0}, Misses:{1}\n".format(len(matches),len(misses)))
    if len(matches) == 0:
       print("not going to generate sig no files matched the regex")
       sys.exit(-1)
    elif len(matches) == 1:
       print("not going to generate sig only one one file matched the regex {0}".format(matches[0]))
       sys.exit(-1)
print("finding klcs")
common = hamming_klcs(target_strings)
print("steaming dem clams")
ndb = ndb_from_common_sequence(target_strings, common)

if not options.lwsom:
    disass=ndb.split('*')
    reass=[]
    for entry in disass:
        if re.match("^(?:[0[9dabc]|20)+$",entry) == None:
            reass.append(entry)
    ndb="*".join(reass)


def replacenulls(nullmatch):
    nullseqlen=len(nullmatch) - 4
    return "%sclamnullseqrep{%s}%s" % (nullmatch[0:2],nullseqlen,nullmatch[-2:])

def addmatch(match):
    tmp=binascii.unhexlify(match[4:-4])
    tmp=tmp.replace("clamnullseqrep","")
    return match[0:4] + tmp + match[-4:]

if options.seqrepl and options.seqrepl > 0:
    if options.seqrepl < 8:
        options.seqrepl = 8

    disass=ndb.split('*')
    reass=[]
    for entry in disass:
        buflen=len(entry)
        buff=binascii.unhexlify(entry)                    
        buff=re.sub(r'(.)\1{%s,}' % (options.seqrepl),lambda m: replacenulls(m.group()),buff)
        buff=re.sub(r'.{4}636c616d6e756c6c7365717265707b.+?7d.{4}',lambda m: addmatch(m.group()),binascii.hexlify(buff))
        reass.append(buff)
    ndb="*".join(reass)

if options.nocase:
    ndb = ndb + "::i"
if options.maxsplit > 0:
    ndb = re.sub(r'\*',"{0-%s}" % (options.maxsplit),ndb)
print("{0}{1}".format(sig,ndb))
