# Install a Myriadcoin Full Node on a Headless Raspberry Pi

This tutorial will help you setup and install a Myriadcoin full node on a Raspberry Pi from start to finish.

### Hardware

Start off by getting the required components

*  Raspberry Pi with at least 2GB of RAM (might work with less RAM)
*  16GB or larger SD card that fits your choice of Raspberry Pi (My current PI uses around 10GB so a 16GB SD card works for now, but it might be too small in the future as the blockchain grows)
*  Power adapter for the Pi
*  A cool case for it (optional)

I've currently only tested this tutorial on a Raspberry Pi 4 with 4GB of RAM with a 16GB micro SD card, the complete setup cost me about $50. If a cheaper model of the Raspberry Pi is used you could probably get the price down quite a bit. I am currently trying to find a Raspberry Pi Zero W to test it on, which could make a $15 setup possible.

### Prepare the SD card

Before we boot up the Pi we need to prepare the SD card.

1. Download Raspberry Pi Imager from https://www.raspberrypi.org/software/
2. Mount the SD card to your computer
3. Start Raspberry Pi Imager and install Raspberry Pi OS Lite on your SD card
4. Open up the SD card in your computers explorer (you might need to remount the the SD card to make it show up)
5. If you plan to connect to the Pi remotely you need to create an empty file called `ssh` on the SD card
6. If you want the Pi to connect to your wifi you should create a file called `wpa_supplicant.conf` on the SD card. Then paste the following into it (replacing `NETWORK-NAME` and `NETWORK-PASSWORD` with your wifi network name and password):
   ```
   country=US
   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
   update_config=1
   
   network={
       ssid="NETWORK-NAME"
       psk="NETWORK-PASSWORD"
   }
   ```
7. Save the file and unmount the SD card
8. Insert the SD card into the Raspberry Pi and boot it up
9. After the Pi has booted you should be able to ping it using ´ping raspberrypi`

Congratulations you now have your Raspberry Pi up and running and connected to the internet.

### Connect to the Pi remotely

This step is optional and are only required if you do not want to connect the Pi to a keyboard and monitor. These instructions are also made specifically if you have an ssh client available in your terminal. You can use other SSH clients and adapt the intructions to them. 

1. Make sure you followed the instruction of how to enable ssh in the previous step when setting up the SD card
2. Open up a terminal
3. Connect to the Pi using `ssh pi@raspberrypi` (pi is the username hence the pi@)
4. Use password `raspberry` once you are prompted 
5. You should now see this or similar: `pi@raspberrypi:~ $`

You have now successfully connected to the Raspberry Pi from another computer and ready to install Myriadcoin. Great job!

### Install and run Myriadcoin Core

1. Download Myriadcoin Core: `wget https://github.com/myriadteam/myriadcoin/releases/download/v0.18.1.0/myriadcoin-0.18.1.0-arm-linux-gnueabihf.tar.gz`
2. Extract the downloaded archive: `tar xzfv ./myriadcoin-0.18.1.0-arm-linux-gnueabihf.tar.gz`
3. Rename the extracted folder: `mv myriadcoin-0.18.1 myriadcoin`
4. Create a data directory for the Myriadcoin blockchain: `mkdir myriadcoin-data`
5. Open a text editor to create a service `nano myriadcoin.service` and copy the following into it
   ```
   [Unit]
   Description=Myriadcoin
   After=network.target
   
   [Service]
   ExecStart=/home/pi/myriadcoin/bin/myriadcoind -datadir=/home/pi/myriadcoin-data -debuglogfile=/home/pi/myriadcoind.log -rpcpassword=rpc -port=10888 -disablewallet -listen -discover -upnp
   StandardOutput=inherit
   StandardError=inherit
   Restart=always
   User=pi
   
   [Install]
   WantedBy=multi-user.target
   ```
6. Save the file using Ctrl+O (make sure the file is saved as `myriadcoin.service`)
7. Exit the text editor by using Ctrl+X
8. Create a symlink of the service: `sudo ln -s /home/pi/myriadcoin.service /etc/systemd/system/myriadcoin.service`
9. Start the service: `sudo systemctl start myriadcoin`
10. Make sure it runs using `htop`
11. Exit htop using Ctrl+C
12. Activate the service so it starts everytime the Pi boots `sudo systemctl enable myriadcoin`
13. If you want you can monitor the log by running `tail -f myriadcoind.log`

If your router supports UPnP Myriadcoin Core should open the correct ports and make your node public. If you find that after it has fully synced that it's still not public, you might need to configure your router manually to forward TCP port 10880 to the Pi.
