# -*- coding: utf-8 -*-
#
# Copyright 2011 TUBITAK/BILGEM
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

import os
from distutils.dir_util import copy_tree

WorkDir = "."

def setup():
    # Unpack and prepare files
    for tar_file in shelltools.ls(get.workDIR()):
        if tar_file.endswith("xz"):
            shelltools.system("tar Jxfv %s" % tar_file)

def build():
    for folder in ["tlpkg", "doc", "source", "omega"]:
        shelltools.unlinkDir("%s/%s" %(get.workDIR() , folder))

def install():
    pisitools.dodir("/usr/share")

    wanteddirs = []
    for file_ in shelltools.ls(get.workDIR()):
        if shelltools.isDirectory(file_) and not "texmf" in file_:
            wanteddirs.append(file_)

    for folder in wanteddirs:
        pisitools.insinto("/usr/share/texmf-dist", folder)

    if shelltools.can_access_directory("texmf-dist"):
        # Recursively copy on directory on top of another, overwrite duplicate files too
        copy_tree("texmf-dist", "%s/usr/share/texmf-dist" % get.installDIR())

    ## chmod of script files
    script_dir = get.installDIR() + "/usr/share/texmf-dist/scripts"
    if shelltools.can_access_directory(script_dir):
        for root, dirs, files in os.walk(script_dir):
            for name in files:
                shelltools.chmod(os.path.join(root, name), 0755)

    # copy config file to texmf-config
    pisitools.dodir("/etc/texmf/tex/context/config")
    shelltools.copy("%s/usr/share/texmf-dist/tex/context/config/cont-usr.tex" % get.installDIR(), \
                    "%s/etc/texmf/tex/context/config/cont-usr.tex" % get.installDIR())

    # old packages, we will not provide them
    pisitools.remove("/usr/share/texmf-dist/tex/plain/config/omega.ini")
    pisitools.remove("/usr/share/texmf-dist/tex/plain/config/aleph.ini")
    pisitools.removeDir("/usr/share/texmf-dist/scripts/context/stubs/mswin/")
