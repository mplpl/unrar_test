# Automatic black-box testing suite for unrar_amiga

This package contains a set of test rar files with various content as well as test script. 
The package was made to standardize and simplify tests of software from this repo: https://github.com/mplpl/unrar_amiga

In total there are more than 50 tests, including test for extracting from:
* archives with files and directories
* archives with excrypted files
* archives with encrypted headers
* archives with comments
* archives with files packed with absolute path
* archives with multiple versions of the same file
* archives with symbolic and hard links
* archives with identical files stored as rar references
* archives with NTFS junction points
* archives with unix owner and group stored
* archives with files, directories and links having national characters in their names
* archives with password containing national characters
* archives with comment containing national characters
* extracting from archives using filters in filelist using file names with national characters
* multivolume archives
* locked archives
* Linux and Windows SFX archives
* archives created on MacOS using rar5, rar5 but using compression v4 and rar3 
* archives created on Windows using WinRAR

## Requirements

You can runs the test package on one of the following environments:
* MorphOS 3.16
* AmigaOS 4.1
* AROS (i386)
* AmigaOS 3.x

In all the cases, the following software has to be installed:
* GNU make, GNU diff, sh, cp, rm, mkdir
* lha
* python 2

It is also required, that files system on which this package is stored, which is also the filesystem where tests files will be created, supports soft and hard links. For instance, SFS does NOT support hard links.

## Running tests

Before running tests, 'expected' content needs to be created. That basically means unpacking expected.lha package and recreating soft and hard links. To do it, you call:

```make prepare```

If that command fails on making soft or hard links, that typically means that file system does not support the links. It is not recommented to move on - rather find a different partition that will support links and copy entire package there. A RAM disk can be a candidate.

Next, in order to run actual tests, call:

```make UNRAR=path_to_unrar```

For MorphOS and  AmigaOS path_to_unrar should be given in Amiga way for instance:

```make UNRAR=/unrar_amiga/unrar```

In case of AROS, it is the best to give absolute version of Unix path, for instance:

```make UNRAR=/home/documents/unrar_amiga/unrar```

will use unrar command from home:documents/unrar_amiga directory.

And that's it!

The command will run all the tests and will show you execution progress and status of each test. 
At the end, a short summary is shown.

