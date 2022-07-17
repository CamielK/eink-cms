CMS to generate and display content on an e-paper display using an IT8951 controller.

###Source
- IT8951 controller code forked from [waveshare/IT8951-ePaper](https://github.com/waveshare/IT8951-ePaper)
- Raspberry Pi OS Lite

###Hardware
- Display Controller: IT8951 HAT
- Display: [Waveshare 10.3 inch 1872×1404 e-Paper (16 Grey Scales)](https://www.waveshare.com/10.3inch-e-paper.htm)
- Controller: Raspberry Pi Zero WH
- Power Supply: [Pisugar2](https://www.pisugar.com/)


### PiSugar 2

https://github.com/PiSugar/PiSugar/wiki/PiSugar2

Web UI running on
``http://192.168.178.24:8421``

Battery percentage API
``echo "get battery" | nc -q 0 127.0.0.1 8423``