@echo off
@chcp 65001 > nul

set PGCLIENTENCODING=UTF8
set PGPASSFILE=%APPDATA%\postgresql\.pgpass

dropdb -U postgres --if-exists matmaneuver
createdb -U postgres matmaneuver

cmd /c "chcp 65001 > nul && psql -U postgres -v ON_ERROR_STOP=1 -d matmaneuver -f schema.sql > out.txt 2>&1"
REM psql -U postgres -v ON_ERROR_STOP=1 -d matmaneuver -f seed.sql

pause