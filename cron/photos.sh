#!/bin/bash
# Loads a random photo from the archive
# Displays the image on the screen

timestamp() {
  date +"%Y-%m-%d %H:%M:%S"
}

echo "[$(timestamp)] Started photos bash script"

# Get new img
echo "[$(timestamp)] Running python script"
cd /home/pi/epaper/eink-cms/py/photos
python3 rand_archive.py

if [ $? -ne 0 ]; then
  echo "[$(timestamp)] Python script failed with non-zero exit code. Terminating bash script"
  exit 0
fi

# Refresh display
echo "[$(timestamp)] Refreshing image to display"
cd /home/pi/epaper/eink-cms/controller/it8951
sudo ./epd -1.27

# Get battery status
#echo "[$(timestamp)] Getting battery status"
#echo "get battery" | nc -q 0 127.0.0.1 8423

echo "[$(timestamp)] Finished photos bash script"