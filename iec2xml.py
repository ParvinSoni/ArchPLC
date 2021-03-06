#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""\
IEC 61131-3 Structured Text to XML compiler 1.4
Copyleft (c), 2009-2011 X-Pie Software GmbH

"""
import time
import sys
import fileinput
from optparse import OptionParser

try:
    from lxml import etree

    lxml_found = True
except:
    lxml_found = False

from pyPEG import parse
import iec_grammar
from xmlast import pyAST2XML
import re

r = re.compile


def printInfo(option, opt_str, value, parser):
    sys.stdout.write(__doc__)
    sys.exit(0)

optParser = OptionParser()
optParser.add_option(
    "-E",
    "--EPAS-pragmas",
    action="store_true",
    dest="epaspragmas",
    help="read and process EPAS pragmas at top of file",
    default=False,
)
optParser.add_option(
    "-o",
    "--output",
    dest="outputFile",
    metavar="FILE",
    help="place output in file FILE",
)
optParser.add_option(
    "-p",
    "--parse-only",
    action="store_true",
    dest="parseonly",
    help="parse only, then output pyAST as text to stdout",
    default=False,
)
if lxml_found:
    optParser.add_option(
        "-P",
        "--pretty",
        action="store_true",
        default=False,
        help="pretty print output adding whitespace",
    )

optParser.add_option(
    "--version", action="callback", callback=printInfo, help="show version info"
)
(options, args) = optParser.parse_args()

comment = r(r"(\(\*.*?\*\))|({.*?})", re.S)


def iec():
    return (iec_grammar.iec_source, )


pragma = r(r"\s*\(\*\s*\@(\w+)\s*:=\s*'(.*?)'\s*\*\)\s*")
empty = r(r"^\s*$")


def consumeEPAS(files):
    global comment
    for l in files:
        m = empty.match(l)
        if m:
            continue
        m = pragma.match(l)
        if m:
            if m.group(1) == "NESTEDCOMMENTS" and m.group(2) == "Yes":
                comment = [
                    r("{.*?}"),
                    (
                        "(*",
                        -1,
                        [
                            r(r"(?m)[^*()]+"),
                            comment,
                            r(r"(?m)(\((?!\*))+"),
                            r(r"(?m)\)+"),
                            r(r"(?m)(\*(?!\)))+"),
                        ],
                        "*)",
                    ),
                ]
        else:
            break


start_time = time.time()

try:
    files = fileinput.input(args)
    if options.epaspragmas:
        consumeEPAS(files)
        files.close()
        files = fileinput.input(args)

    ast = parse(iec, files, True, comment)
    if options.parseonly:
        print(ast)
    else:
        xml = '<?xml version="1.0"?>\n'
        if lxml_found:
            if options.pretty:
                xml = etree.tostring(etree.fromstring((xml + pyAST2XML(ast))),
                                     pretty_print=True)
                xml = xml.decode('utf-8')
            else:
                xml += pyAST2XML(ast)
        else:
            xml += pyAST2XML(ast)

        if options.outputFile and options.outputFile != "-":
            outfile = open(options.outputFile, "w")
            outfile.write(xml)
            outfile.close()
        else:
            print(xml)

except KeyboardInterrupt:
    sys.stderr.write("\n")
    sys.exit(1)
except:
    me, parm, tb = sys.exc_info()
    sys.stderr.write(str(parm) + "\n")
    sys.exit(5)

print("--- %s seconds ---" % (time.time() - start_time))