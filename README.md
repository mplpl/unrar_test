# Automatic black-box testing suite for unrar_amiga

This package contains a set of test rar files with various content (files, directories, links, references) created using rar3 and rar5 on MacOS and Windows. Some archives are encrypted, some other contains items with national characters in names. In addition a testing scripts are included for making it easy to run the package on Amiga operating systems:
* MorphOS
* AmigaOS4
* AROS (i386)
* AmigaOS3

In all the cases, the following software has to be installed:
* GNU make, diff, cp, rm
* lha
* python 2

Running tests

Before running tests, 'expected' content needs to be created. That basically means unpacking expected.lha package and recreating soft and hard links. To do it, you call:

make prepare

If that command fails on making soft or hard links, that typically means that file system does not support the links. It is not recommented to move on - rather find a different partition that will support links and copy entire package there. A RAM disk can be a candidate.

Next, in order to run actual tests, call:

make UNRAR=path_to_unrar

where path_to_unrar is given in Amiga way, for instance:

make UNRAR=/unrar_amiga/unrar

will use unrar command from unrar_amiga at the same level as current dir.

And that's it!
