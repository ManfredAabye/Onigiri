@echo off

:: Lösche Onigiri.zip, falls sie existiert
if exist Onigiri.zip (
    del Onigiri.zip
)

:: Den Ordner Onigiri komprimieren als ZIP-Datei.
powershell -Command "Compress-Archive -Path Onigiri -DestinationPath Onigiri.zip"
echo Onigiri.zip wurde erfolgreich erstellt.
pause