ifeq ($(PLATFORM),)
PLATFORM=$(shell uname)
endif

ifeq ($(PLATFORM),AmigaOS)
ifeq ($(shell uname -m),ppc)
PLATFORM=AmigaOS4
else
PLATFORM=AmigaOS3
endif
endif

TESTS_TO_SKIP=
OS3_INVOCATION=0

ifeq ($(PLATFORM),MorphOS)
SOFT=
HARD=hard
endif

ifeq ($(PLATFORM),AmigaOS4)
SOFT=
HARD=hard
SHELL=sh
endif

ifeq ($(PLATFORM),AROS)
SOFT=
HARD=hard
endif

ifeq ($(PLATFORM),AmigaOS3)
SOFT=soft
HARD=
OS3_INVOCATION=1
endif

ifeq ($(PLATFORM),Mini)
SOFT=soft
HARD=
TESTS_TO_SKIP=11,12,13,14,19,21,22,30,31,34,35,41,42,43,44,45,46,47,48,49,50,51,52,53,56
OS3_INVOCATION=1
endif

ifeq ($(PROFILE),SFS)
# SFS does not support hardlinks
TESTS_TO_SKIP+=27,37,44
endif

ifeq ($(UNRAR),)
test:
test_ram:
	@echo unrar to test is not set
	@echo call: make test UNRAR=path_of_unrar_to_test
	
else

ifeq ($(OS3_INVOCATION),1)
test:
	setenv RAR_CODEPAGE=ISO-8859-2
	@python run_test.py $(UNRAR) . $(TESTS_TO_SKIP)

test_ram:
	setenv RAR_CODEPAGE=ISO-8859-2
	@python run_test.py $(UNRAR) ram:unrar_test $(TESTS_TO_SKIP)
	
else
		
test:
	@RAR_CODEPAGE=ISO-8859-2 python run_test.py $(UNRAR) . $(TESTS_TO_SKIP)
	
test_ram:
	@RAR_CODEPAGE=ISO-8859-2 python run_test.py $(UNRAR) ram:unrar_test $(TESTS_TO_SKIP)
	
endif
endif

prepare:
	@echo Deleting exising expected directory
	-@rm -rf expected >unpack_expected.log

	@echo Unpacking expected.lha
	@lha x expected.lha >>unpack_expected.log

	@echo Making soft links
	
	@echo test_18
	@cd expected/test_18; makelink 0758.jpg IMG_0758.jpeg $(SOFT)
	@cd expected/test_18; makelink 0762.jpg IMG_0762.jpeg $(SOFT)
	@cd expected/test_18; makelink 0796.jpg IMG_0796.jpeg $(SOFT)
	
	@echo test_23
	@cd expected/test_23; makelink 0758.jpg IMG_0758.jpeg $(SOFT)
	@cd expected/test_23; makelink 0762.jpg IMG_0762.jpeg $(SOFT)
	@cd expected/test_23; makelink 0796.jpg IMG_0796.jpeg $(SOFT)

	@echo test_24
	@cd expected/test_24; makelink 0796.jpg subdir/IMG_0796.jpeg $(SOFT)

	@echo test_25
	-@mkdir :tmp
	@touch :tmp/1.txt
	@cd expected/test_25; makelink 1.txt :tmp/1.txt $(SOFT)

	@echo test_26
	@cd expected/test_26; makelink 2.txt /2.txt $(SOFT)

	@echo test_30
	@cd expected/test_30; makelink 标舵.jpg 标舵.jpeg $(SOFT)

	@echo test_31
	@makedir expected/test_31/subdir
	@cd expected/test_31/subdir; makelink IMG_0796.jpeg /IMG_0796.jpeg $(SOFT)

	@echo test_32
	@makedir expected/test_32
	@cd expected/test_32; makelink tmp :tmp $(SOFT) force

	@echo test_38
	@cd expected/test_38; makelink 0796.jpg IMG_0796.jpeg $(SOFT)

	@echo test_40
	@cd expected/test_40; makelink kat_2 kat $(SOFT) force

	@echo test_42
	@cd expected/test_42; makelink 矿虫_2 矿虫 $(SOFT) force

	@echo test_45
	@cd expected/test_45; makelink 标婵_3.jpg 标婵.jpeg $(SOFT)

	@echo test_46
	@makedir expected/test_46
	@copy expected/2.txt expected/标婵.jpeg
	@cd expected/test_46; makelink file2.jpg /标婵.jpeg $(SOFT)

	@echo test_47
	@cd expected/test_47; makelink 标舵.jpg 标舵.jpeg $(SOFT)
	
	@echo Making hard links

	@echo test_27
	-@cd expected/test_27; makelink IMG_0796.jpeg 0796.jpg $(HARD)
	
	@echo test_37
	-@cd expected/test_37; makelink IMG_0796.jpeg 0796.jpg $(HARD)

	@echo test_44
	-@cd expected/test_44; makelink 标婵_2.jpg 标婵.jpeg $(HARD)
	
	@echo Done
	-@rm -f unpack_expected.log

prepare_ram:
	@makedir ram:unrar_test
	@copy expected.lha ram:unrar_test
	@copy Makefile ram:unrar_test
	$(MAKE) -C ram:unrar_test prepare
	@rm ram:unrar_test/expected.lha

clean:
	-@rm -rf expected 
	-@rm -rf results 

.PHONY: test test_ram prepare prepare_ram clean