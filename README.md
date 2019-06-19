run crontab -e, select an editor, then insert the line '0 * * * * python /home/pi/git/downloadSbcVersions/check.py > /home/pi/git/downloadSbcVersions/log'
this runs the python script at the start of every hour, i.e. 12:00, 1:00, 2:00
