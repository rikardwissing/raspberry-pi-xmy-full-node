# display Myriadcoin logo on pi sense hat and animate when detecting new block

from sense_hat import SenseHat
from time import sleep
import subprocess

sense = SenseHat()
sense.load_image("logo_refresh_8x8.png")
sense.low_light = True


def rotate_image():
    i = 0
    while i < 4*16:
        sense.set_rotation(i*90 % 360)
        i += 1
        sleep(0.1)


block_count = 0
prev_block_count = 0

while True:
    try:
        block_count = subprocess.check_output(
            ['myriadcoin/bin/myriadcoin-cli', '-rpcpassword=rpc', 'getblockcount'])
        print("Current block count: " + block_count)

        if block_count != prev_block_count:
            prev_block_count = block_count
            sense.low_light = False
            rotate_image()
            sleep(3)
            sense.low_light = True

    except:
        print('Could not parse block height')

    sleep(10)
