# Copyright Alberto Donato 2019, 2026
# SPDX-License-Identifier: LGPL-3.0-or-later

import logging


def setup_log(logfile):
    logging.basicConfig(
        filename=str(logfile),
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )
