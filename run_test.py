# coding=ISO-8859-2

import os
import shutil
import sys

EXPECTED_DIR="expected"
TMP_DIR="results"
UNRAR = "unrar"
IS_AROS = 0


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
      return os.system(" ".join(cmd) + ">%s"%log)


def compare(test_id):
   sys.stdout.write('.')
   sys.stdout.flush()

   cmd = ["diff", "-r", "--exclude=test.log", os.path.join(
      EXPECTED_DIR, test_dir(test_id)), os.path.join(TMP_DIR, test_dir(test_id))]
   ret = os.system(" ".join(cmd))
   if ret != 0:
      print("Error in test (ret code %s)" % ret)
   #else:
   #  print("Test OK")
   return ret


def clean_up(test_id):
   sys.stdout.write('.')
   sys.stdout.flush()
   try:
      shutil.rmtree(os.path.join(TMP_DIR, test_dir(test_id)), ignore_errors=1)
   except Exception, e:
      print(e)
   return 0;
   
   
def make_static_file():
   if not os.path.exists(":tmp"):
      os.mkdir(":tmp")
   if not os.path.exists(":tmp/1.txt"):
      open(":tmp/1.txt", "a").close()
   if not os.path.exists("expected/2.txt"):
      open("expected/2.txt", "a").close()
   if not os.path.exists(TMP_DIR):
      os.mkdir(TMP_DIR)
   if not os.path.exists(os.path.join(TMP_DIR, "2.txt")):
      open(os.path.join(TMP_DIR, "2.txt"), "a").close()  
   if not os.path.exists(os.path.join(TMP_DIR, "ąęćż.jpeg")):
      open(os.path.join(TMP_DIR, "ąęćż.jpeg"), "a").close()


def run_test(test_id, unpack_args, desc):
   sys.stdout.write("\nTest %s" % test_id)
   sys.stdout.flush()

   if call_unpack(test_id, unpack_args) != 0:
      print(" [unpact error] ")
      print("\nTest decription: %s" % desc)
      return 1
   ret = compare(test_id)

   if ret == 0:
      if clean_up(test_id) !=0:
         print("\nTest decription: %s" % desc)
         return 100
      else:
         sys.stdout.write(' OK')
         sys.stdout.flush()
   return ret


if __name__ == "__main__":

   #parser = argparse.ArgumentParser(description="Test runner")
   #parser.add_argument("--go", action="store_true", help="run tests")
   #parser.add_argument("--tmp_dir", help="temp directory when files will be unpacked - default is current dir")
   #args = parser.parse_args()
   
   if len(sys.argv) != 2:
      print("python run_test.py [path_to_unrar]")
      exit(1)
   
   if os.path.exists(sys.argv[1]):
      UNRAR = sys.argv[1]
      print("Using unrar command: %s" % UNRAR)
      
   else:
      print("%s not found" % sys.argv[1])
      print("python run_test.py [path_to_unrar]")
      exit(2)


   os.system("version %s\n\n" % UNRAR);

   try:
      if os.uname()[0] == "AROS":
        IS_AROS = 1
   except:
      IS_AROS = 0

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
   test_id = 1
   for test, desc in tests:
      run_test(test_id, test, desc)
      test_id += 1
   else:
      print("\nAll Done\n")







