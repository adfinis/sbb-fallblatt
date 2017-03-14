# SBB split flap displays

Documentation and code for interfacing with SBB split flap display modules.

## General

Most documentation in this repository is taken from old original documens or reverse engineered. It is far from being complete. If you have any additional informations which you like to share, please contact us or even create an pull request.

## Documentation

There are 2 types of single modules, in this repo called old and new ones. The old ones do not have an integrated RS485 controller while the new ones do.

For complete units there only seems to exist a "Omega controller" which seems to to talk to old modules only.

### New modules

- [Electrical details](./doc/electrical_new_module.md)
- [Communication protocol](./doc/protocol_new_modules.md)
- [Char<->Blade mapping](./doc/char_mapping.md)


### Old modules

- TBD

### Omega controller

- [Electrical details](./doc/electrical_omega_controller.md)
- [Communication protocol](./doc/protocol_omega_controller.md)
