# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools

def setup():
    pisitools.dosed("test/Makefile.am", "^(SUBDIRS =).*$", r"\1 vainfo")

    autotools.autoreconf("-vif")
    autotools.configure("--enable-glx \
                         --enable-dummy-driver \
                         --enable-i965-driver")

def build():
    autotools.make()

def install():
    autotools.install()

    pisitools.dodoc("COPYING")
