# OctoPrint-Awesome-Karmen-LED

Control APA102 LEDs attached to Raspberry Pi.

## Requirements

- Raspberry pi with octoprint
- APA102 LED attached to rpi

## Wiring

- rpi is 3.3v and APA102 is 5v device. Correct solution would be usage of level shifter as described [here](https://github.com/tinue/apa102-pi#wiring). But from our experience it works just fine without level shifting.

### Connect

- LED 5v <-> rpi 5v (in case of just one or two leds; longer strip needs separate power source or it may end up with demaged rpi)
- LED ground <-> rpi ground
- LED data <-> rpi SPI MOSI
- LED clock <-> rpi SPI SCLK

## Installation

- Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/fragaria/karmen-led-octoprint-plugin/archive/master.zip

- Enable SPI interface on RPI [(official documentation)](https://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/)
  - On desktop use "Raspberry Pi Configuration" dialog *or*
  - From terminal run `sudo raspi-config` and in `Interfacing options` enable `P4 SPI` *or*
  - Edit `sudo nano /boot/config.txt` and uncomment `dtparam=spi=on` line.

## Usage

Plugin has two modes of operation - API and automatic. Modes can be switched in plugin's settings.

### API mode

To turn LEDs on send POST request to `/api/plugin/awesome_karmen_led` with json body `{"command": "set_led", "color":[<R>, <G>, <B>]}` where `<R>`,`<G>` and `<B>` are numbers from 0 to 255.

Example:

``` bash
curl http://<rpi_hostname_or_ip>/api/plugin/awesome_karmen_led --header "X-Api-Key: <YOURAPIKEY>" -X POST -d '{"command": "set_led", "color":[255, 255, 255]}' -H "Content-Type: application/json"
```

### Auto mode

Colors are changed automaticaly by connection and print events.
