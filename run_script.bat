@echo off
Rem Enter json file path here
set file=C:\Users\Saleha\Desktop\Homer\itunedata_into_database-main\itunedata_into_database-main\itunedata_into_database-main\data.json
Rem Possible environments = dev, prod
set env="dev"
Rem Possible operations = insert, create, select, delete, count
set op="select"
Rem Python script path
set python_script_path=C:\Users\Saleha\Desktop\Homer\itunedata_into_database-main\itunedata_into_database-main\itunedata_into_database-main\homer_test.py
Rem Enter csv file path to store
set csvpath=C:\Users\Saleha\Desktop\Homer
echo python %script_path% -file %file% -env %env% -op %op% --csvpath %csvpath%
python %python_script_path% -file %file% -env %env% -op %op% --csvpath %csvpath%
Rem python homer_test.py -file data.json -env dev -op insert --csvpath C:\Users\Saleha\Desktop\Homer