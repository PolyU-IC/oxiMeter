#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 23:39:52 2022

@author: icwhchoy
"""
# -*- coding: utf-8 -*-
# https://play.google.com/store/apps/details?id=com.vphealthy.oximeter&hl=en&gl=US
# https://m.tb.cn/h.fp1LnsS?tk=KcUd2Sre93W%E3%80%8CBluetooth


import sys
import asyncio
import platform

from bleak import BleakClient

NFY_UUID = "f1080002-0451-4000-b000-000000000000"
REQ_UUID = "f1080003-0451-4000-b000-000000000000"

ADDRESS = (
    "fb:e2:5e:24:16:38"  # <--- Using Windows or Linux
    if platform.system() != "Darwin"
    else "8656E488-1990-E5D7-A113-B8790C5966FA"  # <--- Using macOS
)

def printdata(data):
    print("{:03d} {:03d} {:03d} {:03d} SPO2:{:03d}% HB:{:03d} NRV:{:03d} PI:{:f}".format(
        data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]/10))


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    printdata(data)
#    print("{0}: {1}".format(sender, data))


async def main(address, char_uuid):
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")

#  - Custom service SVC of device DEV has 2 characteristics
#  - Sending value VAL to characteristic REQ triggers a notification NFY

        await client.write_gatt_char(REQ_UUID, b"\xa0")
        await client.write_gatt_char(REQ_UUID, b"\x1f")
        
        # await client.write_gatt_char(REQ_UUID, b"\xab")
        # await client.write_gatt_char(REQ_UUID, b"\x00")
        # await client.write_gatt_char(REQ_UUID, b"\x03")
        # await client.write_gatt_char(REQ_UUID, b"\xff")
        # await client.write_gatt_char(REQ_UUID, b"\x30")
        # await client.write_gatt_char(REQ_UUID, b"\x80")
#        print("Result:", result)        

        await asyncio.sleep(0.1)
        await client.start_notify(char_uuid, notification_handler)
        await asyncio.sleep(5.0)
        await client.stop_notify(char_uuid)

if __name__ == "__main__":
    asyncio.run(
        main(
            sys.argv[1] if len(sys.argv) > 1 else ADDRESS,
            sys.argv[2] if len(sys.argv) > 2 else NFY_UUID,
        )
    )
else:
    result=[b'\x90\x02\x03\x01cZ3_\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        b'\x90\x02\x03\x01bZ\x1eR\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        b'\x90\x02\x03\x01bZ"R\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        b'\x90\x02\x03\x01aZ\x10U\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        b'\x90\x02\x03\x01bY%X\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        b'\x90\x02\x03\x01bY\x1eT\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        b'\x90\x02\x03\x01bY*S\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        b'\x90\x02\x03\x01bY!L\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        b'\x90\x02\x03\x01bY(\\\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        b'\x90\x02\x03\x01bY\x1e\\\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00']
    for i in range(len(result)):
        printdata(result[i])
