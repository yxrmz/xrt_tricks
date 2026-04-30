# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 16:12:50 2026

@author: Roman Chernikov
"""

from softioc import softioc, builder, asyncio_dispatcher

dispatcher = asyncio_dispatcher.AsyncioDispatcher()

# 1. Set the record prefix (the device name)
builder.SetDeviceName("TST")

# 2. Create the PV
ao_pitch = builder.aOut('MIRROR1:Pitch', initial_value=0.1)
ao_height = builder.aOut('MIRROR1:Height', initial_value=0.0)

# 3. Start the IOC
builder.LoadDatabase()
softioc.iocInit(dispatcher)

# Optional: Keep the IOC running with an interactive shell
softioc.interactive_ioc(globals())
