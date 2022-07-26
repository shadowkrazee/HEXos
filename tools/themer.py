#!/usr/bin/env python3
"""Compiles themes for wasp-os"""

from argparse import ArgumentParser, RawTextHelpFormatter
from importlib import import_module
from typing import Tuple

class DefaultTheme():
    """This represents the default theme.

    Import this file and extend the Theme class, only changing the variables.
    Export the resulting class as 'Theme'.
    serialize() should NEVER be overriden!
    
    # Use this to format an int as hex for use here:

webRGB = (28, 25, 23)
to565 = int(31 * (webRGB[0] / 255)), int(63 * (webRGB[1] / 255)), int(31 * (webRGB[2] / 255))
rgb =  (to565[0] << 11) + (to565[1] << 5) + (to565[2])
'{:02X}'.format(rgb)
    """
    BLE_COLOR = 0x7BEF
    SCROLL_INDICATOR_COLOR = 0x7BEF
    BATTERY_COLOR = 0x7BEF
    BATTERY_CHARGING_COLOR = 0xFFE0
    SMALL_CLOCK_COLOR = 0xE73C
    NOTIFICATION_COLOR = 0x7BEF
    BRIGHT = 0xFE8A # DARK_AMBER # HEXos
    MID = 0x6AC9 # WARM_GRAY # HEXos
    BG = 0x18C2 # WARM_D_GRAY # HEXos
    UI = 0x39FF
    SPOT1 = 0xFF00
    SPOT2 = 0xDDD0
    CONTRAST = 15

    def serialize(self) -> bytes:
        """Serializes the theme for use in wasp-os"""
        def split_bytes(x: int) -> Tuple[int, int]:
            return ((x >> 8) & 0xFF, x & 0xFF)
        theme_bytes = bytes([
            *split_bytes(self.BLE_COLOR),
            *split_bytes(self.SCROLL_INDICATOR_COLOR),
            *split_bytes(self.BATTERY_COLOR),
            *split_bytes(self.BATTERY_CHARGING_COLOR),
            *split_bytes(self.SMALL_CLOCK_COLOR),
            *split_bytes(self.NOTIFICATION_COLOR),
            *split_bytes(self.BRIGHT),
            *split_bytes(self.MID),
            *split_bytes(self.BG),
            *split_bytes(self.UI),
            *split_bytes(self.SPOT1),
            *split_bytes(self.SPOT2),
            *split_bytes(self.CONTRAST)
        ])
        return theme_bytes


if __name__ == '__main__':
    parser = ArgumentParser(
        description='''Compiles themes into a format understood by wasp-os.

For the theme to take effect, the resulting string should be put in main.py
like this:

   theme_string = THEME_STRING_GOES_HERE
''',
        epilog=''' To create a theme, import this file and extend the
DefaultTheme class, only changing the variables.

Export the resulting class as 'Theme'.

Example:
--------

theme.py:

    from themer import DefaultTheme

    class Theme(DefaultTheme):
        BLE_ICON_COLOR = 0x041F

shell:

    # NOTE: do not include .py at end of file!
    $ ./themer.py theme
    > b'\\xef{\\xef{\\xef{<\\xe7\\xef{\\xb6\\xb5\\xb6\\xbd\\xff\\xff\\xff9'

main.py:

    ...
    wasp.system.set_theme(
        b'\\xef{\\xef{\\xef{<\\xe7\\xef{\\xb6\\xb5\\xb6\\xbd\\xff\\xff\\xff9')
    ...
''',
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument('input_file', type=str, nargs=1)
    args = parser.parse_args()

    theme = DefaultTheme()
    theme = import_module(args.input_file[0]).Theme()
    print(theme.serialize())

