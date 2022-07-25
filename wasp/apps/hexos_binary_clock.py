# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Daniel Thompson

"""HEXos Binary clock
~~~~~~~~~~~~~~~~

Shows a time (as HH:MM) together with a battery meter and the date.

.. figure:: res/ClockApp.png
    :width: 179
"""

import wasp
import gc

MONTH = 'JanFebMarAprMayJunJulAugSepOctNovDec'

class HexosBinaryClockApp():
    """Simple digital clock application."""
    NAME = 'HEXos Binary Clock'
    ORANGE = (31 << 11) + (40 << 5)
    YELLOW = (30 << 11) + (61 << 5)

    def foreground(self, radius=30):
        """Activate the application.

        Configure the status bar, redraw the display and request a periodic
        tick callback every second.
        """
        wasp.system.bar.clock = True
        self._radius = radius
        self._draw(True)
        
        wasp.system.request_tick(1000)

    def sleep(self):
        """Prepare to enter the low power mode.

        :returns: True, which tells the system manager not to automatically
                  switch to the default application before sleeping.
        """
        return True

    def wake(self):
        """Return from low power mode.

        Time will have changes whilst we have been asleep so we must
        udpate the display (but there is no need for a full redraw because
        the display RAM is preserved during a sleep.
        """
        self._draw(True)

    def tick(self, ticks):
        """Periodic callback to update the display."""
        self._draw()
        # DEBUG # redraw every tick
        # self._draw(True)
        # print()

    def preview(self):
        """Provide a preview for the watch face selection."""
        wasp.system.bar.clock = False
        self._draw(True)

    def _day_string(self, now):
        """Produce a string representing the current day"""
        # Format the month as text
        month = now[1] - 1
        month = MONTH[month*3:(month+1)*3]

        return '{} {} {}'.format(now[2], month, now[0])

    def _draw(self, redraw=False):
        """Draw or lazily update the display.

        The updates are as lazy by default and avoid spending time redrawing
        if the time on display has not changed. However if redraw is set to
        True then a full redraw is be performed.
        """
        draw = wasp.watch.drawable
        now = wasp.watch.rtc.get_localtime()
        wasp.system.bar.update()

        # Draw the changeable parts of the watch face
        # Colon blinks every second
        self._draw_colon(draw, now[5])
        # if the minute changes, redraw the right hex
        if redraw or self._mm != now[4]:
            self._draw_minutes(draw, now[4])
        # If the hour changes, redraw the left hex and the dateString
        if redraw or self._hh != now[3]:
            self._draw_hours(draw, now[3])
            draw.set_color(self.ORANGE)
            draw.string(self._day_string(now), 0, 200, width=240)
            draw.set_color(0)

        # Record the minute that is currently being displayed
        self._hh = now[3]
        self._mm = now[4]

    def _draw_colon(self, draw, ss):
        fill = None if ss % 2 == 0 else self.ORANGE
        # Fill the colon area with black and redraw the colon
        r = 8
        draw.fill(0, 115 - r // 2, 95 - r // 2, r * 2, 40 + (r * 2))
        draw.regular_polygon(120, 100, 8, 6, 0, self.YELLOW, 2, fill)
        draw.regular_polygon(120, 140, 8, 6, 0, self.YELLOW, 2, fill)
        pass

    def _draw_minutes(self, draw, mm):
        r = self._radius
        draw.fill(0,round(185 - r * 1.6), round(120 - r * 1.8), 8 + r*3, 18 + r*3)
        for i, angle in enumerate(range(360, 0, (-360//6))):
            # dump out a binary string for the current minute value
            bits = "{:06b}".format(mm)
            fill = 0 if (bits[::-1])[i] == "0" else self.ORANGE
            x, y = draw.rel_pos(185,120,draw.offset_angle(angle, 150), r)
            # draw.line(185, 120, x, y, 2, 31)
            draw.regular_polygon(x, y, r, 3, draw.offset_angle(angle, 120), self.YELLOW, 3, fill)
            # break

    def _draw_hours(self, draw, hh):
        r = self._radius
        draw.fill(0,round(55 - r * 1.6), round(120 - r * 1.8), 8 + r*3, 18 + r*3)
        for i, angle in enumerate(range(360, 0, (-360//6))):
            # dump out a binary string for the current minute value
            bits = "{:06b}".format(hh)
            fill = 0 if (bits[::-1])[i] == "0" else self.ORANGE
            x, y = draw.rel_pos(55,120,draw.offset_angle(angle, 150), r)
            # draw.line(55, 120, x, y, 2, 31)
            draw.regular_polygon(x, y, r, 3, draw.offset_angle(angle, 120), self.YELLOW, 3, fill)
            # break
