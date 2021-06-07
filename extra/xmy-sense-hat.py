# display Myriadcoin logo on pi sense hat and animate when detecting new block

from sense_hat import SenseHat
from time import sleep
import subprocess
import json

sense = SenseHat()

algo_colors = [(246, 108, 190), (253, 149, 30), (253, 239, 65),
               (113, 221, 150), (131, 233, 237), (134, 183, 240), (175, 72, 218)]


def load_logo():
    sense.load_image(
        "/home/pi/raspberry-pi-xmy-full-node-main/extra/logo_refresh_8x8.png")


def rotate_image(rot_diff):
    i = 0
    while i < 4*16:
        i += 1
        sense.set_rotation((i*90+rot_diff) % 360)
        sleep(0.1)


def algo_flash(algo_id):
    sense.clear(algo_colors[algo_id])
    sleep(3)
    load_logo()


sense.low_light = True
load_logo()

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
            ['/home/pi/myriadcoin/bin/myriadcoin-cli', '-rpcpassword=rpc', 'getblockcount']).strip()
        print(block_count)

        if block_count != prev_block_count:
            prev_block_count = block_count

            block_hash = subprocess.check_output(
                ['/home/pi/myriadcoin/bin/myriadcoin-cli', '-rpcpassword=rpc', 'getbestblockhash']).strip()
            block_info = subprocess.check_output(
                ['/home/pi/myriadcoin/bin/myriadcoin-cli', '-rpcpassword=rpc', 'getblock', block_hash]).strip()
            block_info = json.loads(block_info)

            print(block_info['pow_algo'])

            sense.low_light = False

            rotate_image(rotation)
            algo_flash(block_info['pow_algo_id'])
            sleep(3)

            sense.low_light = True

    except:
        print('Could not parse block height')

    sleep(1)
