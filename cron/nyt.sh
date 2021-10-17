#!/bin/bash
# Loads a frontpage of the nyt using py/processing/nyt_frontpage.py
# Displays the image on the screen

timestamp() {
  date +"%Y-%m-%d %H:%M:%S"
}

echo "[$(timestamp)] Started nyt bash script"

# Get new img
echo "[$(timestamp)] Running python script"
cd /home/pi/epaper/eink-cms/py/processing
python3 nyt_frontpage.py

if [ $? -ne 0 ]; then
  echo "[$(timestamp)] Python script failed with non-zero exit code. Terminating bash script"
  exit 0
fi

# Refresh display
echo "[$(timestamp)] Refreshing image to display"
cd /home/pi/epaper/eink-cms/controller/it8951
sudo ./epd -1.27

echo "[$(timestamp)] Finished nyt bash script"