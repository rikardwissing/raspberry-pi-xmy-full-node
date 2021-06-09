# Install a Myriadcoin Full Node on a Headless Raspberry Pi

![image](https://user-images.githubusercontent.com/22580571/119530875-b6ca2a80-bd83-11eb-8648-0b2c5251037e.png)

This tutorial will help you setup and install a Myriadcoin full node on a Raspberry Pi from start to finish.

### Hardware

Start off by getting the required components

- A Raspberry Pi with at least 512MB of RAM (2GB is recommended though)
- 16GB or larger SD card that fits your choice of Raspberry Pi (My current PI uses around 10GB so a 16GB SD card works for now, but it might be too small in the future as the blockchain grows)
- Power adapter for the Pi
- A cool case for it, check out the 3d printable ones below (optional)
- A Sense HAT for a sweet light display (optional)

When writing this tutorial I tested it on a Raspberry Pi 4 with 4GB of RAM with a 16GB micro SD card, that complete setup cost me about $50. I have now tested it on more and cheaper models with great success. See the table below for all the devices that has currently been tested.

#### Tested devices

##### Current models

| Device                 | RAM   | CPU        | Estimated cost | Note                                                                    |
| ---------------------- | ----- | ---------- | -------------: | ------------------------------------------------------------------------|
| Raspberry Pi 4 Model B | 4GB   | 4x1.5GHz   | $50            | No issues, works like a charm. Recommended!                             |
| Raspberry Pi Zero      | 512MB | 700MHz     | $15            | Follow ARM v6 instructions below. Takes a couple of days to compile and sync |

##### Older models

| Device                 | RAM   | CPU        | Estimated cost | Note                                                                    |
| ---------------------- | ----- | ---------- | -------------: | ------------------------------------------------------------------------|
| Raspberry Pi 3 Model B | 1GB   | 4x1.2GHz   | N/A            | Needs to use some Swap but works great                                       |
| Raspberry Pi 1 Model B | 512MB | 700MHz     | N/A            | Follow ARM v6 instructions below. Takes a couple of days to compile and sync |

### Prepare the SD card

Before we boot up the Pi we need to prepare the SD card.

1. Download Raspberry Pi Imager from https://www.raspberrypi.org/software/
2. Mount the SD card to your computer
3. Start Raspberry Pi Imager and install Raspberry Pi OS Lite on your SD card
4. Open up the SD card in your computers explorer (you might need to remount the SD card to make it show up)
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
   
   Remember that certain flavors of the Pi, like the Pi 1 and the Pi Zero W, only supports 2.4Ghz wifi networks

7. Save the file and unmount the SD card
8. Insert the SD card into the Raspberry Pi and boot it up
9. After the Pi has booted you should be able to ping it using `ping raspberrypi`

Congratulations you now have your Raspberry Pi up and running and connected to the internet.

### Connect to the Pi remotely

This step is optional and is only required if you do not want to connect the Pi to a keyboard and monitor. These instructions are also made specifically if you have an ssh client available in your terminal. You can use other SSH clients and adapt the intructions to them.

1. Make sure you followed the instructions of how to enable ssh in the previous step when setting up the SD card
2. Open up a terminal
3. Connect to the Pi using `ssh pi@raspberrypi` (pi is the username hence the pi@)
4. Use password `raspberry` once you are prompted
5. You should now see this or similar: `pi@raspberrypi:~ $`

You have now successfully connected to the Raspberry Pi from another computer and are ready to install Myriadcoin. Great job!

### Install and run Myriadcoin Core

#### Automatic install

1. Run `wget -qO- https://github.com/rikardwissing/raspberry-pi-xmy-full-node/archive/refs/heads/main.tar.gz | tar xzfv -`
2. Then run `sudo raspberry-pi-xmy-full-node-main/auto-install` (see special instructions if using an ARM v6 device)
3. You can monitor the log by running `tail -f myriadcoind.log`
4. To monitor processes and network usage you can use bashtop by running `bashtop-master/bashtop`

##### Special instructions for ARM v6 CPU (Raspberry Pi Zero or Pi 1)

If you have an ARM v6 device (like the Pi Zero or Pi 1) you need to run `sudo raspberry-pi-xmy-full-node-main/run-detached auto-install-arm6` (it will compile myriadcoin from source). It will run in a detached screen, so to see progress you need to run `sudo screen -r` (detach from screen with Ctrl+A d)

Bashtop is a bit to CPU intensive for these devices so the script installs htop instead. Simply run `htop` to monitor processes.

#### Manual install

(Manual install does not work on Raspberry Pi Zero or 1, see automatic installation for those devices)

1. Download and extract Myriadcoin Core: `mkdir -p myriadcoin && wget -qO- https://github.com/myriadteam/myriadcoin/releases/download/v0.18.1.0/myriadcoin-0.18.1.0-arm-linux-gnueabihf.tar.gz | tar xzfv - -C myriadcoin --strip-components=1`
2. Create a data directory for the Myriadcoin blockchain: `mkdir myriadcoin-data`
3. Open a text editor to create a service `nano myriadcoin.service` and copy the following into it

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

   If you run on a device with a low amount of RAM you might want to test to increase the swap file or experiment with the following params `-blocksonly -maxmempool=100 -dbcache=20 -maxorphantx=10 -maxsigcachesize=4 -rpcthreads=1`

4. Save the file using Ctrl+O (make sure the file is saved as `myriadcoin.service`)
5. Exit the text editor by using Ctrl+X
6. Create a symlink of the service: `sudo ln -s /home/pi/myriadcoin.service /etc/systemd/system/myriadcoin.service`
7. Start the service: `sudo systemctl start myriadcoin`
8. Make sure it runs using `htop`
9. Exit htop using Ctrl+C
10. Activate the service so it starts everytime the Pi boots `sudo systemctl enable myriadcoin`
11. If you want you can monitor the log by running `tail -f myriadcoind.log`

If your router supports UPnP Myriadcoin Core should open the correct ports and make your node public. If you find that after it has fully synced that it's still not public, you might need to configure your router manually to forward TCP port 10888 to the Pi.

### Extra

#### 3D prints

In the `extra/3d_prints` folder you'll find some sweet Myriadcoin branded Raspberry Pi cases.

They are modified versions of [Malalo's](https://www.thingiverse.com/thing:3723561) and [Make's](https://www.thingiverse.com/thing:1173084) designs.

| Device                 | Image | Note  |
| ---------------------- | ----- | ----- |
| Raspberry Pi 3         | <img src="https://user-images.githubusercontent.com/22580571/121431769-1fb3c400-c97a-11eb-8bb4-ba6e32a02318.jpg" width="150"> | The sweet light display is provided by the Sense HAT script. See more on that below. |
| Raspberry Pi Zero      | <img src="https://user-images.githubusercontent.com/22580571/121431750-19bde300-c97a-11eb-941b-49fa8cdacdfd.jpg" width="150"> | Isn't this just the cutest thing ever? |


#### Sense HAT

If you have a Sense HAT I have prepared a script that displays the Myriadcoin logo and flashes in different colors when a new block has been found.

1. Get a Sense HAT (https://www.raspberrypi.org/products/sense-hat/)
2. Run `sudo raspberry-pi-xmy-full-node-main/install-sense-hat`

| Algo      | Color          |
| --------- | -------------- |
| SHA256D   | ![#71DD96](https://via.placeholder.com/15/71DD96/000000?text=+) `#71DD96 (113, 221, 150)` |
| Scrypt    | ![#FD951E](https://via.placeholder.com/15/FD951E/000000?text=+) `#FD951E (253, 149, 30)`  |
| Groestl   | ![#FDEF41](https://via.placeholder.com/15/FDEF41/000000?text=+) `#FDEF41 (253, 239, 65)`  |
| ~~Skein~~ (swapped) | ![#F6BEBE](https://via.placeholder.com/15/F6BEBE/000000?text=+) `#F6BEBE (246, 108, 190)` |
| ~~Qubit~~ (swapped) | ![#83E9ED](https://via.placeholder.com/15/83E9ED/000000?text=+) `#83E9ED (131, 233, 237)` |
| Yescrypt  | ![#86B7F0](https://via.placeholder.com/15/86B7F0/000000?text=+) `#86B7F0 (134, 183, 240)` |
| Argon2d   | ![#AF48DA](https://via.placeholder.com/15/AF48DA/000000?text=+) `#AF48DA (175, 72, 218)`  |
