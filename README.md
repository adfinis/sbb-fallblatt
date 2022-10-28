# SBB split flap displays

[![License](https://img.shields.io/github/license/adfinis/sbb-fallblatt.svg?style=flat-square)](LICENSE)

Documentation and code for interfacing with SBB split flap display modules.

## General

Most documentation in this repository is taken from old original documents or
reverse engineered. It is far from being complete. If you have any additional
information which you'd like to share, please contact us or even create a pull
request.

## Documentation

There are 2 types of single modules in this repo called old and new ones. The
old ones do not have an integrated RS485 controller while the new ones do.

For complete units there only seems to exist an "Omega controller" which
appears to to talk to old modules only.

### New Modules

* [Electrical details](./doc/electrical_new_module.md)
* [Communication protocol](./doc/protocol_new_modules.md)
* [Char<->Blade mapping](./doc/char_mapping.md)

### Old Modules

* [Electrical details](./doc_omega_module/electrical_omega_module.md)
* [Char<->Blade mapping](./doc_omega_module/char_mapping.md)

### Omega Controller

* [Electrical details](./doc/electrical_omega_controller.md)
* [Communication protocol](./doc/protocol_omega_controller.md)

## Components

### Panel Simulator

The `panel_mock.py` script can be used to simulate an alphanumerical panel
with variable width.

Setup:

```python
>>> from sbb_fallblatt import sbb_rs485, panel_mock
>>> from multiprocessing import Process
>>> mock_panel = panel_mock.MockPanel(10, 21)
>>> mockthread = Process(target=mock_panel.run)
>>> panel_control = sbb_rs485.PanelAlphanumControl(addresses=list(range(10,21)), port=mock_panel.get_serial_port())
>>> panel_control.connect()
>>> mockthread.start()
>>> panel_control.set_text("test01")
>>> panel_control.get_text()
'test01     '
>>> panel_control.get_serial_number(10)
b'\x01\x88?\x00'
>>> mock_panel.stop()
>>> mockthread.kill()
>>> mockthread.join()

```

### Clock

```python
>>> import time
>>> from datetime import datetime
>>> from multiprocessing import Process
>>> from sbb_fallblatt import sbb_rs485, panel_mock
>>>
>>> mock_panel = panel_mock.MockPanel(10, 12)
>>> mockthread = Process(target=mock_panel.run)
>>> mockthread.start()
>>>
>>> clock = sbb_rs485.PanelClockControl(addr_hour=10, addr_min=11, port=mock_panel.get_serial_port())
>>> clock.connect()

>>> clock.set_time(15, 35) # or use clock.set_time_now()
>>>
>>> clock.get_hour()
15
>>> clock.get_minute()
35
>>> clock.set_time(22, 9)
>>> clock.get_time()
(22, 9)
>>>
>>> mock_panel.stop()
>>> mockthread.kill()
>>> mockthread.join()

```
