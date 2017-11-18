# less-select

This is a patch and a demo perl wrapper script to provide selection support
for the "less" utility.

(C) Martin Väth (martin at mvath.de)

The license of this package is the GNU Public License GPL-2 or BSD
(it should be used with the less program without changing the license).

It allows to select files (or other content) interactively from a list,
using the less program. A perl script making use of this feature and
executing certain commands on the selected files is also provided.

To see what the perl script does, run it with the --man option
(this option should also work if you have not yet installed the patched
version of less program).

Compatibility problems with this patch should hardly occur:
If the new option (-Y) of the less program is not used,
less will behave exactly as without the patch.

For Gentoo, there is an ebuild in the mv overlay for less (available by layman)
which optionally applies the patch and installs the demo script.
