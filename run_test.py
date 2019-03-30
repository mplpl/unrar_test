
import os
import shutil
import sys
import argparse

EXPECTED_DIR="expected"
TMP_DIR="results"
UNRAR = "unrar"

def call_unpack(test_file, fname, unpack_args):
	sys.stdout.write('.')
	sys.stdout.flush()
	log = os.path.join(TMP_DIR, fname)
	if not os.path.exists(log):
		os.mkdir(log)
	log = os.path.join(log, "test.log")
	cmd = ["unrar", unpack_args, TMP_DIR, ">%s"%log]
	#print(" ".join(cmd))
	return os.system(" ".join(cmd))
	

def compare(fname):
	sys.stdout.write('.')
	sys.stdout.flush()

	cmd = ["diff", "-r", "--exclude=test.log", os.path.join(EXPECTED_DIR, fname), os.path.join(TMP_DIR, fname)]
	ret = os.system(" ".join(cmd))
	if ret != 0:
		print("Error in test (ret code %s)" % ret)
	#else:
	#	print("Test OK")
	return ret


def clean_up(fname):
	sys.stdout.write('.')
	sys.stdout.flush()
	try:
		shutil.rmtree(os.path.join(TMP_DIR, fname), ignore_errors=True)
	except Exception as e:
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


def run_test(test_file, unpack_args, desc):
	sys.stdout.write("\nTesting %s" % test_file)
	#sys.stdout.write("\n%s [%s]" % (desc, test_file))
	sys.stdout.flush()

	if not os.path.exists(test_file):
		print("File %s not found\n" % test_file)

	fname, fext = os.path.splitext(os.path.basename(test_file))

	if call_unpack(test_file, fname, unpack_args) != 0:
		print(" [unpact error] ")
		print("\nTest decription: %s" % desc)
		return 1
	ret = compare(fname)

	if ret == 0:
		if clean_up(fname) !=0:
			print("\nTest decription: %s" % desc)
			return 100
		else:
			sys.stdout.write(' OK')
			sys.stdout.flush()
	return ret


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Test runner")
	parser.add_argument("--go", action="store_true", help="run tests")
	parser.add_argument("--tmp_dir", help="temp directory when files will be unpacked - default is current dir")
	args = parser.parse_args()
	
	to_test = []
	with open("params.lst") as f:
		line = f.readline()
		while (line):
			if line.strip():
				to_test.append(line.strip())
			line = f.readline()
			
	test_desc = []
	with open("test.txt") as f:
		line = f.readline()
		while (line):
			if line.strip():
				test_desc.append(line.strip())
			line = f.readline()
	
	tests = list(zip(to_test, test_desc))
	
	print("Found %d tests" % len(tests))

	if args.tmp_dir:
		TMP_DIR=args.tmp_dir
		if not os.path.exists(TMP_DIR):
			print("%s does not exist\n" % TMP_DIR)
			exit(1)
	else:
		if not os.path.exists(TMP_DIR):
			os.mkdir(TMP_DIR)
		
	if args.go:
		i = 0
		make_static_file()
		for test, desc in tests:
			test_file = test.split()[-1]
			run_test(test_file, test, desc)
		else:
			print("\nAll Done\n")
	else:
		print("\nuse '--go' to run tests\n")






