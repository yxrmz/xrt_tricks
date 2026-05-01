# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 20:58:28 2026

@author: Roman Chernikov
"""

from caproto.server import PVGroup, pvproperty, ioc_arg_parser, run


class TSTIOC(PVGroup):
    mirror1_pitch = pvproperty(
        name="MIRROR1:Pitch",
        value=0.1,
        dtype=float,
    )

    mirror1_height = pvproperty(
        name="MIRROR1:Height",
        value=0.0,
        dtype=float,
    )


if __name__ == "__main__":
    ioc_options, run_options = ioc_arg_parser(
        default_prefix="TST:",
        desc="Simple caproto IOC for xrt digital twin testing",
    )

    ioc = TSTIOC(**ioc_options)
    run(ioc.pvdb, **run_options)
