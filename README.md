# garmin-xhd-18-python
A python middleware for the Garmin GMR 18 xHD radar I wrote, its features are only minimal as I only had the device under my possession for only a short time.
The software is based on [radar_pi](https://github.com/opencpn-radar-pi/radar_pi)
 
## Current features
- send on/off command
- read spoke data from network and decode packet
- plot image from data ([example](https://github.com/nonascii/garmin-xhd-18-python/blob/main/plot_result.jpg))

I plan to implement more features based on the available documentation([1](https://github.com/opencpn-radar-pi/radar_pi/blob/master/doc/GarminEthernetData.ods),[2](https://github.com/opencpn-radar-pi/radar_pi/blob/master/example/garminxhd_txon_txoff.pcap.gz),[3](https://github.com/opencpn-radar-pi/radar_pi/blob/master/example/garmin_xhd.pcap.gz)) but to test them I will need at remote access to a linux system connected with the radar, if you are interested in the development of this project send me a message.
