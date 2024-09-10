
<a name="WIZnet-ioNIC-micropyton_README"></a>
WIZnet-ioNIC-micropyton_README
===========================


> The W55RP20 is a System-in-Package (SiP) developed by WIZnet, integrating Raspberry Pi's RP2040 microcontroller, WIZnet's W5500 Ethernet controller, and 2MB of Flash memory into a single chip. These sections will guide you through the steps of configuring a development environment for micropython using the **W55RP20** product from WIZnet.





<a name="hardware_requirements"></a>

# Hardware requirements

| Image                                                        | Name                                                      | Etc                                                          |
| ------------------------------------------------------------ | --------------------------------------------------------- | ------------------------------------------------------------ |
| <image src= "https://docs.wiznet.io/assets/images/w55rp20-evb-pico-docs-8e041fe8924bed1c8d567c1c8b87628d.png" width="200px" height="150px"> | [**W55RP20-EVB-PICO**](https://docs.wiznet.io/Product/ioNIC/W55RP20/w55rp20-evb-pico)           | [W55RP20 Document](https://docs.wiznet.io/Product/ioNIC/W55RP20/documents_md) |

> ### Pin Diagram

The W55RP20 has internal connections between the RP2040 and W5500 via GPIO pins. The connection table is as follows:

| I/O  | Pin Name | Description                                    |
| :--- | -------- | ---------------------------------------------- |
| O    | GPIO20   | Connected to **CSn** on W5500                  |
| O    | GPIO21   | Connected to **SCLK** on W5500                 |
| I    | GPIO22   | Connected to **MISO** on W5500                 |
| O    | GPIO23   | Connected to **MOSI** on W5500                 |
| I    | GPIO24   | Connected to **INTn** on W5500                 |
| O    | GPIO25   | Connected to **RSTn** on W5500                 |


<a name="development_environment_configuration"></a>

# Development environment configuration

<a name="Building"></a>
## Building

1. Clone  
```sh
cd [user path]
git clone https://github.com/WIZnet-ioNIC/WIZnet-ioNIC-micropython.git
git submodule update --init
```

2. Build
```sh
cd WIZnet-ioNIC-micropython/ports/rp2
make BOARD=W55RP20_EVB_PICO
```

3. uf2 file writing  
   Hold down the BOOTSEL button on your W55RP20-EVB-PICO board, press and release the RUN button, and you should see a removable disk pop-up.

```sh
cp build-W55RP20_EVB_PICO/firmware.uf2 /media/[user name]/RPI-RP2
```

4. examples  
   The MicroPython examples for the W55RP20-EVB-PICO can be found at the following path. Please refer to this for guidance.  
```sh
WIZnet-ioNIC-micropython/WIZnet-ioNIC_examples
```

The pre-built bin files (WIZnet-ioNIC-micropython_Bin.zip) can be found at the following path:  
https://github.com/WIZnet-ioNIC/WIZnet-ioNIC-micropython/releases  
