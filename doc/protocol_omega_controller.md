# Protocol Omega controller

## Gereral

Protocol: `RS422` <br>
Baudrate: `9600`  <br>
bytesize:  `7`    <br>
parity:    `even` <br>
stopbits:  `1`


## Message structure

`<SOH> ({ADDR-TYPE: DC1|DC2} [ADDR]) <STX> ([DATA...]) <EOT>`

* `SOH`: required, begin of message
* `ADDR-TYPE`: optional, address type:
  * `DC1`: Group addressing, deprecated
  * `DC2`: Single adressing
* `ADDR`: optional, unit address
* `STX`: required, begin of payload
* `DATA`: optional, data to send
* `EOT`: required, end of message

All chars in `<>` are ascii-command chars.

## Command char mapping

| Command | Dec | Hex |
|---------|-----|-----|
| SOH     | 1   | 01  |
| STX     | 2   | 02  |
| EOT     | 3   | 03  |
| DC1     | 17  | 11  |
| DC2     | 18  | 12  |
| HOME    | 8   | 08  |
| RIGHT   | 24  | 18  |
| LEFT    | 25  | 19  |
| CLEAR   | 12  | 0C  |
