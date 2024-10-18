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
