#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Creation:    06.06.2017
# Last Update: 21.07.2017
#
# Copyright (c) 2017 by Ole Weidner <https://oleweidner.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from i2crelay import I2CRelay

import click

@click.command()
@click.option('--i2c-type', type=int, default=1,    help='The I2C bus type (0 or 1)')
@click.option('--i2c-addr', type=str, default=0x20, help='The I2C device address, e.g. 0x20')
@click.option('--relay',    type=int,               help='The relay to switch (0..8) on or off')
@click.argument('cmds',     type=str, nargs=-1)
def main(i2c_type, i2c_addr, relay, cmds):
    """Control a PCF8574 I2C relay board.
    """

    # Convert string to hex
    i2c_addr = int(i2c_addr, 16)

    # Parse the command string
    for c in cmds:
        validate_command(c)

    try:
        r1 = I2CRelay(i2c_type, i2c_addr)

        for c in cmds:
            n,o = c.split(":")
            if o.lower() == "on":
                r1.switch_on(int(n))
            elif o.lower() == "off":
                r1.switch_off(int(n))

    except KeyboardInterrupt:
        print("Execution stopped by user")
        r1.switch_all_off()


def validate_command(c):
    n = None
    o = None

    try:
        # split realy number and operation
        n,o = c.split(":")
        # convert realy number to integer
        n = int(n)
    except:
        raise TypeError("Invalid command: %s", c)

    if type(n) != int:
        raise TypeError("Invalid command: %s", c)
    if o.lower() not in ['on', 'off', 'toggle']:
        raise TypeError("Invalid command: %s", c)
