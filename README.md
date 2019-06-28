# Ergo testnet faucet

This is implementation of Ergo testnet faucet on Python 3. It requires additional ergo-rest-signer service for signing transactions. There is only web interface.


## Build and run

Build with Docker:

    sudo docker build -t faucet .

Run with Docker:

    sudo docker container run -d \
        -p 33333:33333 \
        -e SECRET_KEY=<YOUR_FLASK_SECRET_KEY> \
        -e SIGNER_URI=http://signer:5000 \
        -e SK=<YOUR_FAUCET_ADDRESS_SECRET_KEY> \
        faucet

where:

- `YOUR_FLASK_SECRET_KEY`: secret key for robust session's ids generation (see [Flask Sessions](http://flask.pocoo.org/docs/1.0/quickstart/#sessions))
- `SIGNER_URI`: transactions signer address
- `YOUR_FAUCET_ADDRESS_SECRET_KEY`: secret key of faucet address (address would be derived from that key, so no need to pass it)
