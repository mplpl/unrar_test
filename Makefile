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

ifeq ($(PLATFORM),MorphOS)
SOFT=
HARD=hard
DEVNULL=/dev/null
endif

ifeq ($(PLATFORM),AmigaOS4)
SOFT=
HARD=hard
SHELL=sh
DEVNULL=nil:
endif

ifeq ($(PLATFORM),AROS)
SOFT=soft
HARD=
DEVNULL=/dev/null
endif

ifeq ($(PLATFORM),AmigaOS3)
SOFT=soft
HARD=
DEVNULL=/dev/null
endif


ifeq ($(UNRAR),)
test:
	@echo unrar to test is not set
	@echo call: make test UNRAR=path_of_unrar_to_test
else

ifeq ($(PLATFORM),AmigaOS3)
test:
	setenv RAR_CODEPAGE=ISO-8859-2
	@python run_test.py $(UNRAR)
	
else
		
test:
	@python run_test.py $(UNRAR)
	
endif
endif

prepare:
	@echo Deleting exising expected directory
	-@delete expected all >unpack_expected.log

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
	@delete unpack_expected.log >$(DEVNULL)

clean:
	-@rm -rf expected results 
  
.PHONY: test prepare clean