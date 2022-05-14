@echo off
set /p comment="Enter Changes: "
git add .
git commit -m comment
git pull
git push
cmd /k