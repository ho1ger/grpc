# GRPC Demo in Python 

We have three different client/server pairs:

- No authentication
- Server-side authentication
- Mutual (Server + Client) authentication

Run `genStuff` to generate the python files from the proto file and keys and certs for CA, Server, Client.

The server implements simple math functions that the client calls in different ways.

To try something else, the client can also send a file to the server which returns its hash.
