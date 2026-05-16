@echo off
@chcp 65001 > nul

set PGCLIENTENCODING=UTF8
set PGPASSWORD=quick

dropdb -U postgres --if-exists matmaneuver
createdb -U postgres matmaneuver

psql -U postgres -d matmaneuver -f schema.sql
psql -U postgres -d matmaneuver -f seed.sql

set PGPASSWORD=
pause