# xrt Digital Twin Example (EPICS Integration)

This example demonstrates how to use an **xrt beamline as a digital twin**, synchronizing its state with external EPICS Process Variables (PVs).

Instead of creating its own PV device tree, the beamline listens to existing PVs and updates the model in real time.

## How it works

Beamline updates are driven by EPICS callbacks using `pyepics`:

- PVs are subscribed via:
  ```python
  epics.get_pv('pv_name', callback=...)
  ```

- The callback function (e.g. `callback_update_oe`) processes incoming values and forwards them to the viewer:
  ```python
  xrtGlow.customGlWidget.update_beamline(oeid, {argName: argValue})
  ```

- Each update triggers:
  - beamline reconfiguration
  - ray/wave propagation
  - OpenGL rendering

## Customization

You can implement your own logic inside the callback function, for example:

- convert units (e.g. degrees → radians)
- apply offsets or calibration factors
- filter or validate incoming values

This allows flexible integration with real hardware or control systems.

## Running the example

1. Start the example IOC:
   ```bash
   python simple_ioc.py
   ```

2. Launch the xrt Glow viewer:
   ```bash
   python one_crystal_glow.py
   ```

## Interacting with the system

Once running, you can update PV values externally using:

- `caput` (EPICS CLI tool)
- `epics.caput` from `pyepics`
- Control System Studio (CSS) / Phoebus

As PVs change, the beamline model in **xrtGlow** updates in real time, allowing you to observe the system behavior interactively.
