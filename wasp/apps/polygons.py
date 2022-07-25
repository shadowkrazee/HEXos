# SPDX-License-Identifier: MY-LICENSE
# Copyright (C) YEAR(S), AUTHOR

import wasp
import time

class PolygonsApp():
    """A test application for the HEXos implementation of draw.regular_polygon."""
    NAME = "Polygons"

    def foreground(self, first=True):
        self.first = first
        self._draw()
        wasp.system.request_tick(1000)

    def tick(self, ticks):
        self._draw()

    def _draw(self):
        draw = wasp.watch.drawable
        if self.first:
            draw.fill()
        now = wasp.watch.rtc.get_localtime()
        hh = now[3]
        mm = now[4]
        orange = (31 << 11) + (50 << 5)
        yellow = (31 << 11) + (63 << 5)
        for angle in range(0, 360, (360//60)):
            draw.fill(0, 85, 85, 70, 70)
            draw.regular_polygon(120, 120, 30, mm % 8 + 3, angle, yellow, 3, orange)