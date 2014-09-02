#
# spec file for package less-select (Version 381)
#
# A modification of the spec file for less by Martin Väth.
#
# Copyright (c) 2004 SUSE LINUX AG, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://www.suse.de/feedback/
#

# neededforbuild  
# usedforbuild    aaa_base acl attr bash bind-utils bison bzip2 coreutils cpio cpp cvs cyrus-sasl db devs diffutils e2fsprogs file filesystem fillup findutils flex gawk gdbm-devel glibc glibc-devel glibc-locale gpm grep groff gzip info insserv kbd libacl libattr libgcc libstdc++ libxcrypt m4 make man mktemp modutils ncurses ncurses-devel net-tools netcfg openldap2-client openssl pam pam-devel pam-modules patch permissions popt ps rcs readline sed sendmail shadow strace syslogd sysvinit tar texinfo timezone unzip util-linux vim zlib zlib-devel autoconf automake binutils cracklib gcc gdbm gettext libtool perl rpm

%define rel 88

Name:         less-select
%define prefix   /usr
%define sysconfdir /etc
License:      GPL, Other License(s), see package
Group:        Productivity/Text/Utilities
Obsoletes:    jless less
Provides:     less = 381
Provides:     normal-less jless
Requires:     file
Autoreqprov:  on
Version:      381
Release:      %{rel}.0.SuSE9.0
Summary:      A Text File Browser and Pager Similar to More
URL:          http://www.greenwoodsoftware.com/less/
Source:       less-%{version}.tar.bz2
Source1:      less-SuSE.tar.bz2
Source2:      README.SuSE
Source3:      less-select.tar.gz
NoSource:     0
NoSource:     1
NoSource:     2
# Japanese patch
# URL: http://www.io.com/~kazushi/less/
# http://www.io.com/~kazushi/less/less-358-iso254.patch.bz2
Patch0:       less-%{version}-iso254.patch
Patch1:       less-%{version}.patch
Patch2:       less-%{version}-utf8.patch
Patch3:       less-%{version}-init_def_codesets.patch
Patch4:       less-%{version}-arabic.patch
Patch5:       less-%{version}-iso254-charset.patch
Patch6:       less-%{version}-mouse.patch
Patch7:       less-%{version}-mouse_test_for_xselection.patch
NoPatch:      0
NoPatch:      1
NoPatch:      2
NoPatch:      3
NoPatch:      4
NoPatch:      5
NoPatch:      6
NoPatch:      7
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
Less is a text file browser and pager similar to More. It allows
backward as well as forward movement within a file. Also, Less does not
have to read the entire input file before starting. It is possible to
start an editor at any time from within Less.

This version includes the select-patch of Martin Väth which allows to
select files interactively from a list and execute commands on them.
Call less-select --man for furhter instructions.



Authors:
--------
    Mark Nudelman <markn@greenwoodsoftware.com>
    Martin Väth <martin@mvath.de>

%prep
%setup -q -a 1 -n less-%{version}
chmod -R +rX *
chmod -R +w *
%patch0 -p1 -b .iso
%patch1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5
%patch6
%patch7
#
cp %{S:2} .
%setup -T -D -q -a 3 -n less-%{version}
# If the patch is in a subdirectory, move that out:
test -d less-select* && ( mv less-select* lsd ; mv lsd/* . ; rmdir lsd )
patch -p1 <less-%{version}-SuSE9.0-select.patch
rm -f less.man lesskey.man help.c

%build
%{?suse_update_config:%{suse_update_config -f}}
autoreconf -fi
CFLAGS="$RPM_OPT_FLAGS" \
./configure --mandir=%{_mandir} \
                --prefix=%{prefix} \
                --infodir=%{_infodir} \
                --sysconfdir=%{sysconfdir}
#
# regenerate help.c because less.hlp was patched
make mkhelp
./mkhelp <less.hlp >help.c
#
# build less
make
strip less lesskey
test -e less.man || nroff -man less.nro >less.man
test -e lesskey.man || nroff -man lesskey.nro >lesskey.man


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT/ install
install -m 644 lessecho.1 $RPM_BUILD_ROOT%{_mandir}/man1/
#
# lesskey
install -m 755 -d $RPM_BUILD_ROOT/%{sysconfdir}
install -p -m 644 lesskey.src $RPM_BUILD_ROOT/%{sysconfdir}/lesskey
$RPM_BUILD_ROOT%{prefix}/bin/lesskey -o $RPM_BUILD_ROOT%{sysconfdir}/lesskey.bin $RPM_BUILD_ROOT%{sysconfdir}/lesskey
#
# less-select-key
install -p -m 644 less-select-key.src $RPM_BUILD_ROOT/%{sysconfdir}/less-select-key.src
$RPM_BUILD_ROOT%{prefix}/bin/lesskey -o $RPM_BUILD_ROOT%{sysconfdir}/less-select-key.bin $RPM_BUILD_ROOT%{sysconfdir}/less-select-key.src
#
# preprocessor
install -p -m 755 lessopen.sh lessclose.sh $RPM_BUILD_ROOT/%{prefix}/bin
#
# less-select
install -p -m 755 less-select $RPM_BUILD_ROOT/%{prefix}/bin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc LICENSE COPYING NEWS README.SuSE README.less-select
%doc %{_mandir}/*/*
%config %{sysconfdir}/*
%{prefix}/bin/*

%changelog
* Sun Jun 24 2004 - martin@mvath.de
- Added selection patch
* Thu May 13 2004 - pmladek@suse.cz
- removed potential tmp file race [#39272]
* Wed Sep 10 2003 - pmladek@suse.cz
- test the utility xselection only if the mouse support is enabled [#29612]
* Mon Aug 04 2003 - pmladek@suse.cz
- updated to version 381 [#17201]:
  * new -L option to disable LESSOPEN processing
  * further support for large (64 bit) file addressing
  * use only 7 spaces for line numbers in -N mode, if possible
  * fix some nroff issues in the man page
- removed obsolete patch for support for large file addressing (lfs.patch)
- used autoreconf to rebuild autoconf stuff
* Mon Dec 30 2002 - pmladek@suse.cz
- updated to version 378:
  * default buffer space is now 64K as documented
  * search highlighting works properly when used with -R
  * windows version works properly when input file contains carriage returns
  * clean up some compiler warnings
- merged less-378-iso254-bug.patch into the less-378-iso254.patch
- removed unused CXXFLAGS setting from the spec file
- fixed the patch for the mouse support (prefixes to a less commands were not
  printed immediately in the searched string as yet) [#21320]
* Tue Aug 27 2002 - pmladek@suse.cz
- removed code which is obsoleted by Japanese patch and make
  problems with UTF-8 [#17592, #17593]
* Fri Aug 09 2002 - pmladek@suse.cz
- updated to new stable version 376
  * -x option can now specify multiple variable-width tab stops
  * -X option no longer disables keypad initialization
  * new option --no-keypad disables keypad initialization
  * new commands t and T step through multiple tag matches
  * new prompt style set by option -Pw
  * system-wide lesskey file now defaults to sysless in etc directory
  instead of .sysless in bin directory
  * pressing RightArrow or LeftArrow while entering a number now shifts
  the display N columns rather than editing the number itself
  * searching works better with ANSI (SGR) escape sequences
  * improved performance in reading very large pipes
  * eliminated some dependencies on file offets being 32 bits
  * fixed problems when viewing files with very long lines
  * fixed overstriking in UTF-8 mode, and overstriking tabs
  * improved horizontal shifting of text using -R option with ANSI color
  * improved handling of filenames containing shell metacharacters
- fixed Japanese patch for this less version
- iso247-bugs patch merged with Japanese patch
- fixed bug in detection of xselection utillity
* Fri May 17 2002 - pmladek@suse.cz
- added mouse support (inspired by vim-6.0):
  * it is enabled by -A option
  * works only in xterm
  * contains support for mouse wheel [#9385]
  * direct access to X selection by xselection utility
- applied patches less preprocessor patches
* Thu Mar 21 2002 - pmladek@suse.cz
- improved detection for input conding from keyboard, proper input
  coding is detected by locales now [#15155]
- changed default input coding from "japanese-iso7" to "iso8859"
- user can still define his input conding by the environment
  variable JLESSKEYCHARSET
* Tue Mar 12 2002 - pmladek@suse.cz
- changed meaning of the variable LESS_ADVANCED_PREPROCESSOR,
  many binary formats are preprocessed always, the text
  formats (ps, troff, html) are preprocessed only when
  the variable LESS_ADVANCED_PREPROCESSOR=yes
* Thu Feb 21 2002 - pmladek@suse.cz
- added support for cab files into less preprocessor
* Mon Feb 18 2002 - pmladek@suse.cz
- fixed to do not install .orig files
* Fri Feb 15 2002 - pmladek@suse.cz
- error messages in lessopen.sh must be redirected to the standard
  error output
- fixed Copyright in lessopen.sh and lessclose.sh
* Thu Feb 14 2002 - pmladek@suse.cz
- added man page for lessecho from the Debian GNU/Linux distribution
  [#13275]
- fixed usage of macro %%suse_update_config
* Mon Nov 05 2001 - mfabian@suse.de
- add init_def_codesets.diff (fixes the problem that less
  outputs ESC-A to set 'G1' to 'Right-hand Part of Latin
  Alphabet No.1 ISO 8859/1, ECMA-94'. This works only with
  xterm but fails with konsole, rxvt ...)
  Thanks to Michael Schroeder <mls@suse.de>
- add arabic.diff to fix typo in possible values of JLESSPLANESET
  (alabic -> arabic).
- remove %%attr(644, -, -) in front of %%doc, this gives
  wrong permissions to the directory /usr/share/doc/packages/less
  use 'chmod 644 LICENSE COPYING NEWS' instead.
* Fri Sep 21 2001 - vinil@suse.cz
- README.SuSE about LESS_ADVANCED_PREPROCESSOR added
* Tue Sep 11 2001 - mfabian@suse.de
- include Japanese patch
- rewrote utf8.diff. Together with the Japanese patch it almost
  works now. German, Italian and Spanish man pages display fine
  in an UTF-8 xterm. Czech is still broken, but that seems to
  be the fault of groff rather than less.
- add less-SuSE.patch to display Japanese roff files correctly
* Wed Sep 05 2001 - vinil@suse.cz
- .zip handled by "unzip -v" (#10211)
* Tue Aug 28 2001 - vinil@suse.cz
- LESS_ADVANCED_PREPROCESSOR used for handling more than compressed
  files (#9287)
* Tue Aug 14 2001 - vinil@suse.cz
- typo fixed (#9730)
* Tue Jul 17 2001 - vinil@suse.cz
- can handle symlinks              \
- can handle x and pm man pages    -- bug #9393
* Mon May 14 2001 - vinil@suse.cz
- utf8.diff added: less can handle bold and underlined utf-8 chars
  (needed especially for man)
* Sat May 05 2001 - schwab@suse.de
- lessopen.sh: Create tempfiles securely; add quotes as necessary; make
  sure we don't match the file type against the file name; don't leave
  temporary files around.
* Fri May 04 2001 - schwab@suse.de
- lessopen.sh: echo nothing if we have no alternate file (#7679).
* Fri May 04 2001 - schwab@suse.de
- lessopen.sh: Use the first stage contents if the second stage has
  nothing special.  Tighten the patterns that recognize compressed
  data.  Just echo the original file name if the file is not readable.
* Tue May 01 2001 - schwab@suse.de
- lessclose.sh: Only remove file if different from original file.
* Mon Apr 30 2001 - schwab@suse.de
- lessopen.sh: Use original file name if no conversions were done (#7421).
* Fri Apr 27 2001 - vinil@suse.cz
- lessing non-existing files now produce error message [bug #7320]
* Thu Apr 19 2001 - mfabian@suse.de
- removed "LESSCHARSET=latin1" from /etc/lesskey
  If LESSCHARSET is not set, latin1 is the default, unless
  "UTF-8" is found in LC_ALL, LC_CTYPE or LANG, the the default
  is utf-8. So setting "LESSCHARSET=latin1" is useless in
  case of a iso-8859-x locale and bad in case of a UTF-8 locale.
  If LESSCHARSET is set in /etc/lesskey, one cannot even override
  it by setting the environment variable anymore.
* Fri Mar 16 2001 - vinil@suse.cz
- less piping completely rewritten (using 'file', now)
  (bug #6256 fixed)
* Wed Jan 10 2001 - smid@suse.cz
- lesspipe.sh fixed
* Tue Jan 09 2001 - smid@suse.cz
- lesspipe.sh fixed [#5003]
* Wed Dec 13 2000 - mfabian@suse.de
- added "Provides: normal-less". This enables the japanized
  jless to use "Provides: less" and "Conflicts: normal-less".
  (Suggestion by bjacke@suse.de)
* Mon Dec 11 2000 - smid@suse.cz
- added conflict with jless
* Fri Dec 01 2000 - aj@suse.de
- Compile with LFS support, fix CFLAGS/CXXFLAGS.
* Tue Nov 21 2000 - werner@suse.de
- Remove swapping of kp-separator/kp-decimal because it's
  done in xkbd map for german keyboards
* Tue Nov 21 2000 - werner@suse.de
- Add some newer xterm escape sequences (oldFunctionsKeys)
* Tue Sep 26 2000 - ro@suse.de
- make lesspipe executable again
* Mon Sep 25 2000 - smid@suse.cz
- upgrade to 358
* Mon May 22 2000 - smid@suse.cz
- upgrade to 354
- Copyright field fix
- documentation added
* Thu Apr 13 2000 - smid@suse.cz
- buildroot added
- upgrade to 3.46
* Thu Feb 10 2000 - kukuk@suse.de
- Fill out Copyright and Group field
* Mon Jan 24 2000 - kukuk@suse.de
- Move /usr/man -> /usr/share/man
* Mon Sep 13 1999 - bs@suse.de
- ran old prepare_spec on spec file to switch to new prepare_spec.
* Fri Jun 18 1999 - ro@suse.de
- update to less-340 using jurix-dif
- added [rs]pm to lesspipe-switch
- added werners lesskey
* Thu Sep 04 1997 - bs@suse.de
- added *.as to lesspipe.sh
* Wed May 28 1997 - werner@suse.de
- added new etc/lesskey and etc/lesskey.bin
* Sat Apr 26 1997 - florian@suse.de
- update to new version 332
* Sun Apr 13 1997 - florian@suse.de
- update to new version 330
* Thu Jan 02 1997 - bs@suse.de
  added new etc/lesskey*
* Thu Jan 02 1997 - bs@suse.de
  lesskey from aaa_base inserted.
* Thu Jan 02 1997 - florian@suse.de
- Neue Version 321.
- Bug mit falschen Aufruf von free() behoben.
- In /etc/profile wird global fuer alle Benutzer eine 'lesskey'-Datei
  eingetragen. Braucht also nicht mehr im Home-Verzeichnis aller Benutzer
  erstellt werden.
