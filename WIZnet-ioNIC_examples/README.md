# W55RP20 Micropython Examples

## SNTP Client

**File:** `sntp.py`

This script retrieves the current time by running on the W55RP20 device through Thonny.

## Redis Client

**File:** `redis_client.py`

**Dependency:** `picoredis.py`

When run on the W55RP20 through Thonny, this script connects to a Redis server and performs a few operations:

1. **Ping Command**: Sends an empty `ping` request and another with the string "os" to the Redis server. The server responds with `PONG` and `os` respectively.
2. **Set Command**: Creates a key named `pico` with the value `test from pico` on the Redis server.
3. **Get Command**: Retrieves the value of the `pico` key from the Redis server and prints it, verifying that the key was properly stored.

For more details on available Redis commands, please visit the official documentation: [Redis Commands](https://redis.io/docs/latest/commands/).

## iPerf Server for W55RP20-EVB-Pico

**File:** `iperf3.py`

When executed as a server process, this script performs the following actions:

1. Obtains an IP address via DHCP
2. Opens and listens on port 5201

### Performance Note

Due to the nature of MicroPython execution, the test results may show lower performance compared to the board's actual capabilities. This is an inherent limitation of the interpreted language environment.

### Recommendation for Accurate Performance Testing

For more accurate iPerf test results that reflect the true performance of the W55RP20-EVB-Pico board, we recommend using the C language implementation.

Please refer to the following repository for a C-based iPerf implementation:

[WIZnet-PICO-IPERF-C](https://github.com/WIZnet-ioNIC/WIZnet-PICO-IPERF-C/)

This C implementation will provide more representative performance metrics for the W55RP20-EVB-Pico board.



## Windows iPerf3 Test Script for W55RP20

 **File:** `iperf3_test.py`

This script is designed to test the `iperf3.py` running on the W55RP20 board from a Windows environment.

### Purpose

The primary purpose of this script is to facilitate iPerf3 testing between a Windows machine and a W55RP20 board running the `iperf3.py` script.

### Usage Instructions

To use this script, follow these steps:

1. Ensure the `iperf3.py` script is running on your W55RP20 board.
2. Note the IP address displayed by the W55RP20 board.
3. Open a command prompt or PowerShell window on your Windows machine.
4. Navigate to the directory containing this script.
5. Run the script using the following command format:
