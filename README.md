# subway_stuff

Ok this is the train stuff this is the bulk of the code you should need.

Extra steps:
1) Need an MTA API Key (info here: https://www.mta.info/developers)
2) I used a raspberry pi 3 model b, a LED 64 x 32 screen (https://github.com/adafruit/rpi-rgb-led-matrix/blob/master/README.md has good info), and a 5V power source. I also used a utensil sorter box with the partitions removed to mount and hold the whole thing...in retrospect with more time I would have 3d printed a case haha
3) Since I did this the first time they changed all the info on how to get something to run at startup. Now best bet is to use systemd https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#systemd
4) Find/pick your train stations (stations.json file), and your bus stations (check out mta developers website with files for the borough you want), decide your walk time if you want to make sure you don't see trains you cannot physically make, etc etc
5) You also may have to generate a 10x10 pixel icon for your train symbol if you decide to use a LED screen as your display
6) Yay!
