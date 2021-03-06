#!/usr/bin/env python3 
import os
import sys
import argparse
import textwrap
from classes import sh, pShow, pSize, pJpegtran, NAME 


# contants
VER = '%s: compress JPGs losslessly in batch mode and more... V0.20 ' % NAME


def main():
    parser = argparse.ArgumentParser(
                formatter_class = argparse.RawDescriptionHelpFormatter,
                description = VER + textwrap.dedent('''
    
    Usage Examples:

    1), compress JPGs lossless in batch mode
        $ python3 smally.py -p path1 path2 --jpegtran --jpg
        -p option is mandatory and must have one path argument at least.
        Only --jpg can be combined with --jpegtran.

    2), add interval time between each picture processed
        $ python3 smally.py -p path1 --jpegtran --jpg -i 500
        Default interval time is zero.
        -i option is optional and in milliseconds unit.

    3), recurse into sub-folders 
        $ python3 smally.py -p path1 --jpegtran --jpg -r
        -r option indicates the recursive action.
        Default behavior is not recursive, in line with other cmd tools.

    4), keep mtime unchanged
        $ python3 smally.py -p path1 --jpegtran --jpg -k
        -k option indicates the mtime would not be changed while the
        compressing process. By default, new compressed file will get a new
        mtime stamp.

    5), set time window to skip old file in your routine
        $ python3 smally.py -p path1 --jpegtran --jpg -t 86400
        -t 86400 means the time window is 1 day. If the distance between 
        file mtime and now is within this specific time window, action will
        be applied to this file, otherwise it will be skipped.
        To keep mtime of compressed file unchanged, you need -k option.
        -t is optional, time window is infinite if not configured.

    6), calculate size
        $ python3 smally.py -p path --size --jpg
        Calculate the total JPGs size in /path. You can combine --size with
        -r, -i, -t option. -k option is useless with --size.
        $ python3 smally.py -p path --size --jpg --png --gif --webp
        Calculate the total size of all 4 types of pictures.

    7), show info of picture file
        $ python3 smally.py -p path --show --jpg --png
        Show all JPGs and PNGs in path. You can combine --show with
        -r, -k, -t option. -k option is useless with --show.
    '''),
                epilog = 'Smally project page: '
                         'https://github.com/xinlin-z/smally\n'
                         'Author\'s python note blog: '
                         'https://www.pynote.net'
    )
    parser.add_argument('-p', '--paths', required=True, nargs='+', 
                    help='paths for the picture folder')
    parser.add_argument('-i', '--interval', type=int,
                        help='interval time in milliseconds')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='recursive into sub-folders')
    parser.add_argument('-k', '--keepmtime', action='store_true',
                        help='keep the mtime untouched after compressing')
    parser.add_argument('-t', '--timewindow', type=float, 
                    help='apply action to files those now - mtime is '
                         'in time window (seconds ,float and positive)')
    parser.add_argument('--jpg', action='store_true', 
                            help='for both .jpg and .jpeg suffix')
    parser.add_argument('--png', action='store_true')
    parser.add_argument('--gif', action='store_true')
    parser.add_argument('--webp', action='store_true')
    # group for action type
    actType = parser.add_mutually_exclusive_group(required=True)
    actType.add_argument('--show', action='store_true',
                        help='show pathname and size in KB')
    actType.add_argument('--size', action='store_true',
                        help='calculate total size')
    actType.add_argument('--jpegtran', action='store_true',
                help='lossless compress JPGs with jpegtran tool')
    # version info
    parser.add_argument('-V','--version',action='version',version=VER)
    args = parser.parse_args()  # ~ will be expanded
    # check paths
    for path in args.paths:
        if not os.path.exists(path):
            print('%s: path %s is not existed.' % (NAME,path))
            sys.exit(1)
    # check picture type
    ptype = []
    if args.jpg: ptype.extend(['.jpg','.jpeg'])
    if args.png: ptype.append('.png')
    if args.gif: ptype.append('.gif')
    if args.webp: ptype.append('.webp')
    if ptype == []:
        print('%s: No picture type choosed.' % NAME)
        sys.exit(1)
    # interval
    interval = 0.0
    if args.interval != None:
        if args.interval >= 0: interval = args.interval/1000
        else: 
            print('%s: Interval time must be positive.' % NAME)
            sys.exit(1)
    # time window
    if args.timewindow != None:
        if args.timewindow <= 0:
            print('%s: Time window must be positive.' % NAME)
            sys.exit(1)
    # actions 
    if args.show: 
        if sh.which('identify') is False: sys.exit(1) 
        pShow(ptype, interval, args.recursive, args.timewindow, args.paths)
    if args.size:
        pSize(ptype, interval, args.recursive, args.timewindow, args.paths)
    if args.jpegtran:
        if ptype != ['.jpg','.jpeg']:
            print('%s: --jpegtran only support JPG.' % NAME)
            sys.exit(1)
        if sh.which('jpegtran') is False: sys.exit(1)
        if sh.which('identify') is False: sys.exit(1)
        pJpegtran(ptype, interval, args.recursive, args.timewindow,  
                  args.paths, args.keepmtime)


if __name__ == '__main__':
    main()


