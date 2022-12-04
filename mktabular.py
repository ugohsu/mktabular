#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, argparse, re

# define regressions
remulti = re.compile(r"\\?_multi\\?_")
rehline = re.compile(r"\\?_(hline|midrule)\\?_")
recline = re.compile(r"\\?_(cline|cmidrule)\\?_")
reunion = re.compile(r"\\?_union\\?_")

def basiconv (x):
    return " & ".join(x) + " \\\\"

def searchflg (x, flg):
    return True in (True if flg.search(y) else False for y in x)

def complexconv (x, multi, head):
    # preparation
    x = [remulti.sub("", y) for y in x] if multi else x
    v = list(reversed(x)); nelem = len(v)
    unionflg = [True if reunion.search(y) else False for y in v]
    clineflg = [True if recline.search(y) else False for y in v]

    # make body
    n, clinenum, flg, clinebody = 0, 0, False, []
    for i, y in enumerate(v):
        if unionflg[i]:
            v[i], n = None, n + 1
            if not clinenum:
                clinenum = nelem - i
            if clineflg[i]:
                flg = True
        elif i > 0 and unionflg[i-1]:
            v[i] = "\\multicolumn{" + str(n+1) + "}{c}{" + y + "}"
            if flg or clineflg[i]:
                v[i] = recline.sub("", v[i])
                clinebody.append("\\cmidrule(lr){" + \
                        str(nelem-i) + "-" + str(clinenum) + "}")
            n, clinenum, flg = 0, 0, False
        else:
            v[i] = "\\multicolumn{1}{c}{" + y + "}" if head else y
            if i == len(x) - 1 and multi:
                v[i] = "\\multicolumn{1}{l}{" + y + "}"
            elif multi:
                v[i] = "\\multicolumn{1}{c}{" + y + "}"
            if clineflg[i]:
                v[i] = recline.sub("", v[i])
                clinebody.append("\\cmidrule(lr){" + str(nelem-i) \
                        + "-" + str(nelem-i) + "}")
            n = 0

    return (y for y in reversed(v) if type(y) != type(None)), \
            " ".join(reversed(clinebody))

def mktabular (string, sep, nhead, dcolumn, align):
    # get a number of columns
    ncol = len(string[0].split(sep))

    # separate by sep
    cstr = (x.strip("\n").split(sep) for x in string)

    if align:
        print("\\begin{tabular}{" + align + "}")
    elif dcolumn:
        print("\\begin{tabular}{" + "l" + "D{.}{.}{-1}"*(ncol-1) + "}")
    else:
        print("\\begin{tabular}{" + "l" + "r"*(ncol-1) + "}")

    print("\\toprule")

    for i, x in enumerate(cstr):
        x = [y.strip() for y in x]
        flg = searchflg(x, rehline)
        if flg: x = [rehline.sub("", y) for y in x]
        x, add = complexconv(x, searchflg(x, remulti), i < nhead)

        print(basiconv(x))
        if add: print(add)
        if flg or i == nhead - 1: print("\\midrule")

    print("\\bottomrule")
    print("\\end{tabular}")


if __name__ == "__main__":
    # argument parse
    p = argparse.ArgumentParser()
    p.add_argument("-s", "--sep", dest="sep", 
            default="\t", help=r"separator (default: \t)")
    p.add_argument("-n", "--nhead", type=int, dest="nhead", default=1,
            help="column number of the title (default: 1)")
    p.add_argument("-d", "--dcolumn", dest="dcolumn",
            action="store_true", default=False,
            help="use dcolumn")
    p.add_argument("--align", dest="align", default=None,
            help="specific alignment")
    args = p.parse_args()

    args.sep = '\t' if args.sep == '\\t' else args.sep

    mktabular(string=sys.stdin.readlines(), sep=args.sep, 
            nhead=args.nhead, dcolumn=args.dcolumn, align=args.align)
