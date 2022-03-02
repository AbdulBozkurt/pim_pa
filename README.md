# pim_pa
Includes the project that implements the Diffie Hellman key-exchange with Elliptic Curves.

## Diffie Hellman Key-Exchange Implementation
The Diffie Hellman key-exchange implementation consists of a server Alice and a client Bob.
It was tested with Python 3.10.
Older versions might not work.

To start a Diffie Hellman key-exchange, first start the `alice.py` file in the folder `diffie_hellman` via `python3 ./alice.py`.
Wait until the message `Awaiting connection...` appears.
Then start the `bob.py` file next to it via `python3 ./bob.py`.

Alice should serve forever and Bob should only make one key-exchange.
If correctly started, the key-exchange, will be done fully automatically and will print information at runtime.
Verbose output can be toggled via the variable `verbose` in the file `diffie_hellman/public_constants.py`.

To stop Alice, enter `CTRL+C`.

### Troubleshooting

The server and client try to use port 10666 and ip 127.0.0.1 by default.
If this port is already in use, change the values `ip` and `port` in the file `diffie_hellman/public_constants.py`.

If Alice was recently closed and tries to restart again, it might crash with error message `OSError: [Errno 98] Address already in use`.
This is normal expected behaviour.
The OS might take a couple seconds to close the port and allow new programs to use it.
Wait a bit, try again and all should work.