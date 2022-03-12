# coding=ISO-8859-2

import os
import shutil
import sys
import time

EXPECTED_DIR="expected"
TMP_DIR="results"
UNRAR = "unrar"
IS_AROS = 0
IS_M68K = 0
SIMPLE_DIFF = 0


def test_dir(test_id):
   return "test_%02d"%test_id
   
   
def call_unpack(test_id, unpack_args):
   sys.stdout.write('.')
   sys.stdout.flush()
   test_d = os.path.join(TMP_DIR, test_dir(test_id))
   if not os.path.exists(test_d):
      os.mkdir(test_d)
   log = os.path.join(test_d, "test.log")
   cmd = [UNRAR, unpack_args, test_d]
   #print(" ".join(cmd))
   if IS_AROS:
      return os.system("sh -c '" + " ".join(cmd) + "' >%s"%log)
   else:
      return os.system(" ".join(cmd) + " >%s"%log)


def compare(test_id, simple_diff):
   sys.stdout.write('.')
   sys.stdout.flush()
   
   path1 = os.path.join(EXPECTED_DIR, test_dir(test_id))
   path2 = os.path.join(TMP_DIR, test_dir(test_id))
   
   if simple_diff:
      ret = compare_dirs(path1, path2, 1)
      if ret == 0:
         ret = compare_dirs(path2, path1, 0)
   else:
      cmd = ["diff", "-r", "--exclude=test.log", path1, path2]
      ret = os.system(" ".join(cmd))
      if ret != 0:
         print("Error in test (ret code %s)" % ret)
   return ret

def compare_dirs(dir1, dir2, detailed):
   if not os.path.exists(dir1):
      print("%s does not exist" % dir1)
      return 4
   for item in os.listdir(dir1):
      if item == "test.log":
         continue
      item1_path = os.path.join(dir1, item)
      item2_path = os.path.join(dir2, item)
      if not exists(dir2, item):
         print("%s missing" % item2_path)
         return 1
      if os.path.islink(item1_path):
         if not os.path.islink(item2_path):
            print("%s should be a link" % item2_path)
            return 5
         target1 = abspath(dir1, item)
         target2 = abspath(dir2, item)
         if not os.path.exists(target1):
            print("Broken link %s" %s)
            return 6
         if os.path.isdir(target1) and os.path.isdir(target2):
            # both dirs
            ret = compare_dirs(target1, target2, detailed)
         if not os.path.isdir(target1) and not os.path.isdir(target2):
            # both files
            ret = compare_files(target1, target2, 0)
         if ret != 0:
            print("not ok %s" %ret)
            return ret
         continue
      if os.path.isdir(item1_path):
         if not os.path.isdir(item2_path):
            print("%s should be a dir" % item2_path)
            return 2
         ret = compare_dirs(item1_path, item2_path, detailed)
         if ret != 0:
            print("not ok %s" %ret)
            return ret
         continue
      # item is a file
      if os.path.isdir(item2_path):
         print("%s should be a file" % item2_path)
         return 3
      ret = compare_files(item1_path, item2_path, detailed)
      if ret != 0:
         return ret
   return 0

def compare_files(item1_path, item2_path, detailed):
   # check files details
   size1 = os.path.getsize(item1_path)
   size2 = os.path.getsize(item2_path)
   if size1 != size2:
      print("Wrong size of file %s: %s vs %s" % (item2_path, size1, size2))
      return 100
   # modification date comparison does not work due to DST difference
   #moddate1 = os.path.getmtime(item1_path)
   #moddate2 = os.path.getmtime(item2_path)
   #if abs(moddate1 - moddate2) > 1:
   #   print("Wrong modification date of file %s: %s vs %s" % (item2_path, moddate1, moddate2))
   #   return 0
   if detailed:
      cmd = ["diff", '"' + item1_path + '"', '"' + item2_path + '"']
      ret = os.system(" ".join(cmd))
      if ret != 0:
         print("Error in test (ret code %s)" % ret)
         return ret
   return 0

def abspath(path, item):
   dir = os.getcwd()
   os.chdir(path)
   target = os.readlink(item)
   abs_target = os.path.abspath(target)
   os.chdir(dir)
   return abs_target

def exists(path, item):
   dir = os.getcwd()
   os.chdir(path)
   ret = os.path.exists(item)
   os.chdir(dir)
   return ret
   
def clean_up(test_id):
   sys.stdout.write('.')
   sys.stdout.flush()
   try:
      if os.path.exists(os.path.join(TMP_DIR, test_dir(test_id))):
         shutil.rmtree(os.path.join(TMP_DIR, test_dir(test_id)), ignore_errors=1)
   except Exception, e:
      print(e)
   return 0;
   
   
def make_static_file():
   if not os.path.exists(":tmp"):
      os.mkdir(":tmp")
   if not os.path.exists(":tmp/1.txt"):
      open(":tmp/1.txt", "a").close()
   if not os.path.exists(os.path.join(EXPECTED_DIR, "2.txt")):
      open(os.path.join(EXPECTED_DIR, "2.txt"), "a").close()
   if not os.path.exists(TMP_DIR):
      os.mkdir(TMP_DIR)
   if not os.path.exists(os.path.join(TMP_DIR, "2.txt")):
      open(os.path.join(TMP_DIR, "2.txt"), "a").close()  
   if not os.path.exists(os.path.join(TMP_DIR, "ąęćż.jpeg")):
      open(os.path.join(TMP_DIR, "ąęćż.jpeg"), "a").close()


def clean_up_tests():
  if os.path.exists("tests/unrar_test_57.part2.rar"):
    os.remove("tests/unrar_test_57.part2.rar")
  if os.path.exists("tests/unrar_test_58.part2.rar"):
    os.remove("tests/unrar_test_58.part2.rar")
    
    
def run_test(test_id, unpack_args, desc):
   sys.stdout.write("\nTest %s" % test_id)
   sys.stdout.flush()

   clean_up(test_id)

   if call_unpack(test_id, unpack_args) != 0:
      print(" [unpact error] ")
      print("\nTest decription: %s" % desc)
      return 1
   ret = compare(test_id, SIMPLE_DIFF)

   if ret == 0:
      if clean_up(test_id) !=0:
         print("\nTest decription: %s" % desc)
         return 100
      else:
         sys.stdout.write(' OK')
         sys.stdout.flush()
   return ret

def print_syntax_and_exit(exit_code):
   print("python run_test.py path_to_unrar base_dir [tests_to_skip]")
   exit(exit_code)

if __name__ == "__main__":
   
   #parser = argparse.ArgumentParser(description="Test runner")
   #parser.add_argument("--go", action="store_true", help="run tests")
   #parser.add_argument("--tmp_dir", help="temp directory when files will be unpacked - default is current dir")
   #args = parser.parse_args()
   
   if len(sys.argv) < 3 or len(sys.argv) > 4:
      print_syntax_and_exit(1)
   
   if os.path.exists(sys.argv[1]):
      UNRAR = sys.argv[1]
      print("Using unrar command: %s" % UNRAR)
   else:
      print("%s not found" % sys.argv[1])
      print_syntax_and_exit(2)
      
   if sys.argv[2] == ".":
      pass
   elif os.path.exists(sys.argv[2]):
      BASE_DIR = sys.argv[2]
      print("Base dir: %s" % BASE_DIR)
      EXPECTED_DIR = os.path.join(BASE_DIR, EXPECTED_DIR)
      TMP_DIR = os.path.join(BASE_DIR, TMP_DIR)
   else:
      print("%s not found" % sys.argv[2])
      print_syntax_and_exit(3)

   os.system("version %s\n\n" % UNRAR)
   print("Codepage %s\n\n" % os.getenv("RAR_CODEPAGE"))

   to_skip = []
   if len(sys.argv) == 4:
      to_skip = sys.argv[3].split(",")
      print("Tests to skip: %s\n\n" % ",".join(to_skip))

   try:
      if os.uname()[0] == "AROS":
        IS_AROS = 1
   except:
      IS_AROS = 0
      
   try:
      if os.uname()[4] == "m68k":
        IS_M68K = 1
   except:
      IS_M68K = 0

   SIMPLE_DIFF = os.getenv("SIMPLE_DIFF") == "1" or IS_M68K
   if SIMPLE_DIFF:
      print("Runnin in 'SIMPLE_DIFF' mode\n\n")
   to_test = []
   f = open("tests/params.lst")
   if f:
      line = f.readline()
      while (line):
         if line.strip():
            to_test.append(line.strip())
         line = f.readline()
         
   test_desc = []
   f=open("tests/test.txt")
   if f:
      line = f.readline()
      while (line):
         if line.strip():
            test_desc.append(line.strip())
         line = f.readline()
   
   tests = list(zip(to_test, test_desc))
   
   print("Found %d tests" % len(tests))

   
   if not os.path.exists(TMP_DIR):
      os.mkdir(TMP_DIR)
      
   i = 0
   make_static_file()
   clean_up_tests()
   test_id = 1
   success = 0
   failures = 0
   skipped = 0
   start_time = time.time()
   for test, desc in tests:
      if str(test_id) in to_skip:
         sys.stdout.write("\nTest %s    Skipped" % test_id)
         sys.stdout.flush()
         skipped += 1
      else:
         res = run_test(test_id, test, desc)
         if res == 0:
            success += 1
         else:
            failures += 1
      test_id += 1
   
   
   print("\nDone\n")
   print("Tests successful: %d\n"%success)
   print("Tests failed: %d\n"%failures)
   print("Tests skipped: %d\n"%skipped)
   print("Tests time: %ds\n" % (time.time() - start_time))







