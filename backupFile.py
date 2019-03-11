#!/usr/bin/env python
# coding: utf8
#
# backup /etc/shadow to /tmp
# file read write append -> with
# tempfile
#

from optparse import OptionParser

import os
import sys
import commands
import shutil

if os.geteuid() != 0:
    print "请使用超级用户运行!"
    sys.exit(1)

op = OptionParser()
op.add_option("-s", "--src", help="src file path", metavar="FILE")
op.add_option("-d", "--dst", help="dst dir path", metavar="DIR")

options, args = op.parse_args()

srcfile = options.src
dstdir = options.dst

if not srcfile or not dstdir:
    op.print_help()
    sys.exit(3)

if not os.path.exists(srcfile):
    print "%s 文件不存在" % srcfile
    sys.exit(2)

#status, output = commands.getstatusoutput("cp %s /tmp/" % srcfile)

#if  status != 0:
#    print "备份失败: %s" % output
#    sys.exit(3)
#
#print "备份成功"

#try:
#    shutil.copytree(srcfile, "/tmp/")
#    print "备份成功"
#except:
#    print "备份失败"
dstdir_name = os.path.basename(srcfile.rstrip("/"))

if os.path.isfile(srcfile):
    shutil.copy2(srcfile, dstdir)
elif os.path.isdir(srcfile):
    shutil.copytree(srcfile, os.path.join(dstdir, dstdir_name), symlinks=True)
else:
    print "不支持备份这种文件!"
    sys.exit(4)

print "备份成功"
