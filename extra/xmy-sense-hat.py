# display Myriadcoin logo on pi sense hat and animate when detecting new block

from sense_hat import SenseHat
from time import sleep
import subprocess

sense = SenseHat()
sense.load_image(
    "/home/pi/raspberry-pi-xmy-full-node-main/extra/logo_refresh_8x8.png")
sense.low_light = True


def rotate_image(rot_diff):
    i = 0
    while i < 4*16:
        i += 1
        sense.set_rotation((i*90+rot_diff) % 360)
        sleep(0.1)


block_count = 0
prev_block_count = 0

while True:
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    x = round(x, 0)
    y = round(y, 0)
    z = round(z, 0)

    rotation = 0

    if x == -1.0:
        rotation = 90

    if y == -1.0:
        rotation = 180

    if x == 1.0:
        rotation = 270

    sense.set_rotation(rotation)

    try:
        block_count = subprocess.check_output(
            ['/home/pi/myriadcoin/bin/myriadcoin-cli', '-rpcpassword=rpc', 'getblockcount'])
        print(block_count)

        if block_count != prev_block_count:
            prev_block_count = block_count
            sense.low_light = False
            rotate_image(rotation)
            sleep(3)
            sense.low_light = True

    except:
        print('Could not parse block height')

    sleep(1)
