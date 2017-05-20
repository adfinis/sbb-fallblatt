# Protocol new module

## Gereral

Protocol: `RS485`<br>
Baudrate: `19200 8N1`

## Message Structure

`<BREAK> FF <COMMAND> <ADDR> ( < VALUE1> ( <VALUE2> ..) ) `

- `BREAK` Every message needs to start with an break
- `FF`: Start Byte
- `ADDR`: Module address
- `CMD`: Command
- `DATA`: Data to send. If multiple, sendt to following modules

## Commands

Commands are in HEX

| Command   | Write    | Read     | Description   |
|-----------|----------|----------|---------------|
| DISP/RDB  |   `C0`   |   `D0`   | Set/Get Position |
| STAT      |   `C1`   |   `D1`   | Read: Get status |
| RESET/VER |   `C4`   |   `D4`   | Read: Get firmware version |
| ZERO      |   `C5`   |          | Move to zero point |
| STEP      |   `C6`   |          | Move motor a step (1 blade) forward |
| PULSE     |   `C7`   |          | Move motor a pusle forward |
| TEST      |   `C8`   |          | |
| CTRL      |   `C9`   |   `D9`   | |
| NULL/POS  |   `CA`   |   `DA`   | |
| WIN       |   `CB`   |   `DB`   | Used for calibration |
| CALB      |   `CC`   |   `DC`   | Calibrate |
| TYPE      |   `CD`   |   `DD`   | Set/get type |
| ADDR      |   `CE`   |   `DE`   | Set/get address |
| SNBR      |   `CF`   |   `DF`   | Set/get serial number |



### `DISP` Set Position
`FF C0 <ADDR> <POS>`<br>

pos is position in bytes

#### Example
Address: 29, Position: 20<br>
`FF CO 1D 14 `

### `RDB` Get position
`FF DO <ADDR>`

The module answer 1 bit with position as bytes

#### Example
Address: 29 , Module Position: 30<br>
`FF DO 1D`<br>
Response: <br>
`1E`

### `TYPE` Get device Type
`FF DD <ADDR>`

The module answer 1 bit with type

#### Types

| Int | Hex | Type                 | #Blades |
|-----|-----|----------------------|---------|
| 1   | 01  | Hour/Alphanummeric   | 40      |
| 2   | 02  | Minute               | 62      |

#### Example
Address: 29 , Module Type: Hour<br>
`FF DD 1D`<br>
Response: <br>
`01`


### `SNBR` Get serial number
`FF DF <ADDR>`<br>
The module answers with 4 bytes containing the serial number

#### Example
Address: 29 , Module Serial number: 43516<br>
`FF DF 1D`<br>
Response: <br>
`01 88 3f 00`


### `ZERO` Move motor to null position
`FF C6 <ADDR>`

Note: on hour modules, zero is "0." and on minute modules "31"

#### Example
Address: 29
`FF C6 1D`<br>


### `STEP` Move motor one blade
`FF C6 <ADDR>`

If not moving correctly, number of `PULSE` for a step can be changed in calibration.

#### Example
Address: 29
`FF C6 1D`<br>


### `PULSE` Move motor one pulse
`FF C6 <ADDR>`<br>

A few pulses are required to complete a `STEP`.

#### Example
Address: 29<br>
`FF C7 1D`


### `VER` Get firmware version
`FF D4 <ADDR>`

The module answers with 2 bytes containing the version number


### `CALB` Calibrate the device
`FF CC <ADDR>`

The calibration sets how many pulses are required for moving to next blade and set blade number. Use with caution.

#### Procedure

* Send calibrate command
  * `FF CC <ADDR>`
* Send `STEP` until blade change
  * `FF C6 <ADDR>`
* Now send `PULSE` until next blade falls
  * `FF C7 <ADDR>`
* Now send `WIN` with the blade number to set code to current blade
  * `FF CB <ADDR> <POS>`


### `ADDR` Change address of module
`FF CE <OLD_ADDR> <NEW_ADDR>`

Changes address of the module. There is no response

#### Example
Old Address: 29
New Address: 30
`FF CE 1D 1E`<br>
