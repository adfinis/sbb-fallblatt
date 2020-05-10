# Electrical details Omega modules

## General
Each Flip-Flap Module has a PCB with discrete logic to control a synchroneous AC motor.
They have been in use since 1987.

* Protocol: Encoder Output (6 bits), 3 digital inputs
* Supply: 48V AC, 12V DC

## Pinout

### Main connector

| Pin | Function | Function | Pin |
|-----|----------|----------|-----|
| 1   | BIT2     | BIT0     | 2   |
| 3   | BIT4     | BIT5     | 4   |
| 5   | 12V GND  | BIT3     | 6   |
| 7   | START    | 12V GND  | 8   |
| 9   | ADL      | BIT1     | 10  |
| 11  | +12V DC  | +12V DC  | 12  |
| 13  | +48V AC  | +48V AC  | 14  |
| 15  | +48V AC  | +48V AC  | 16  |
| 17  | -48V AC  | -48V AC  | 18  |
| 19  | -48V AC  | -48V AC  | 20  |

### Small Faston 1

| Pin | Function |
|-----|----------|
| 1   | ADC      |

### Small Faston 2

| Pin | Function |
|-----|----------|
| 1   | START    |

### Small Faston 3

| Pin | Function |
|-----|----------|
| 1   | PE       |

## Schematics

The board has been reverse engineered with following result:

- [Schematics](./schematic/FallBlattBoard_schema.png)

## Encoder

The encoder turns together with the display and emitts a strobe signal which is used in the internal logic to stop the motor. More on this is described further down.
The signals can be read out only when the motor is disabled. Otherwise they will all read high. The transition from motor off to signals readable is given by a low pass filter of approximately 30us.

## Control

The control interface has two types of signals. Three input signals and 6 output bits from the position decoder.

The input signals are:

* ADL: line select
* ADC: column select
* START: motor start signals

You can find the waveforms (created with WaveDrom) [here](./waveform/wavedrom.png)

### Read current position

To read out the current position through the encoder bits both, ADL and ADC, are pulled low. The motor should not move. When all this is given the position is set on the encoder output bits (all signals are inverted).

### Start motor to change sheet on display

To start the motor ADL and ADC are pulled down the same way as in "Read current position". Pull START low and keep it low while releasing ADC (or ADL). The motor starts turning and START can be released.

### Stop motor

The motor can not stopped directly. It turns indefinitely until a single-shot circuit fires. This happens when the encoder strobe signal is active and ADC gets pulled low. Therefore, to stop the motor at a given position ADC must be polled continuosly. The measurement of the encoder signals, as described above, shows if the motor has stopped (current position can be read) or if it is still turning (all encoder bits are high). Wait 30us after enabling ADC before reading the value to ensure a correct reading.
