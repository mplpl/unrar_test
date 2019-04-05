#!/usr/bin/python

import os

if not os.path.exists("expected"):
    os.mkdir("expected")

with open("params_expected.lst") as f:
    line = f.readline()
    test_id = 1
    while line:
        if line.strip():
            path = "expected/test_%02d" % test_id
            if not os.path.exists(path):
                os.mkdir(path)
            cmd = ["./unrar", line.strip(), path]
            print(" ".join(cmd))
            if os.system(" ".join(cmd)):
                print("Error in test %d" % test_id)
        line = f.readline()
        test_id += 1

if os.path.exists("expected.rar"):
    os.remove("expected.rar")
os.system("./rar a -ola -oh expected.rar expected")
