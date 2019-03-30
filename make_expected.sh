rm -rf expected
mkdir expected
./unrar x -y -ad unrar_test_01.rar expected
./unrar x -y -ad unrar_test_02.rar expected
./unrar x -y -ad unrar_test_03.rar expected
./unrar x -y -ad -pqwerty unrar_test_04.rar expected
./unrar x -y -ad -pqwerty unrar_test_05.rar expected
./unrar x -y -ad unrar_test_06.rar expected
./unrar x -y -ad unrar_test_07.rar expected
./unrar x -y -ad unrar_test_08.rar expected
./unrar x -y -ad unrar_test_09.rar expected
./unrar x -y -ad unrar_test_10.rar expected
./unrar x -y -ad unrar_test_11.rar expected
./unrar x -y -ad unrar_test_12.rar expected
./unrar x -y -ad unrar_test_13.rar expected
./unrar x -y -ad unrar_test_14.rar expected
./unrar x -y -ad unrar_test_15.rar expected
./unrar x -y -ad unrar_test_16.rar expected
./unrar x -y -ad unrar_test_17.part1.rar expected
./unrar x -y -ad unrar_test_18.rar expected
./unrar x -y -ad -pżółć unrar_test_19.rar expected
./unrar x -y -ad unrar_test_20.rar expected
./unrar x -y -ad unrar_test_21.rar expected
./unrar x -y -ad -pżółć unrar_test_22.rar expected
./unrar x -y -ad unrar_test_23.rar expected
./unrar x -y -ad unrar_test_24.rar expected
./unrar x -y -ad -ola unrar_test_25.rar expected
./unrar x -y -ad -ola unrar_test_26.rar expected
./unrar x -y -ad unrar_test_27.rar expected
./unrar x -y -ad unrar_test_28.rar expected
./unrar x -y -ad unrar_test_29.rar expected
./unrar x -y -ad unrar_test_30.rar expected
./unrar x -y -ad unrar_test_31.rar expected
./unrar x -y -ad -ola unrar_test_32.rar expected
./unrar x -y -ad unrar_test_33.rar expected
./unrar x -y -ad unrar_test_34.rar expected
./unrar x -y -ad unrar_test_35.rar expected
./unrar x -y -ad unrar_test_36.rar expected
./unrar x -y -ad unrar_test_37.rar expected
./unrar x -y -ad unrar_test_38.rar expected
./unrar x -y -ad unrar_test_39.rar expected
./unrar x -y -ad unrar_test_40.rar expected
./unrar x -y -ad unrar_test_41.rar expected
./unrar x -y -ad unrar_test_42.rar expected
./unrar x -y -ad unrar_test_43.rar expected
./unrar x -y -ad unrar_test_44.rar expected
./unrar x -y -ad unrar_test_45.rar expected
./unrar x -y -ad unrar_test_46.rar expected
mkdir expected/unrar_test_46
./unrar x -y -ad unrar_test_47.rar expected

rm expected.rar
./rar a -ola -oh expected.rar expected
