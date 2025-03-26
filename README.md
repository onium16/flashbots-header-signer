# Flashbots Header Signer v.0.1.0

This module provides a utility for creating signed headers to interact with the Flashbots service. It helps address issues with Web3 version compatibility when making requests to Flashbots.

## Problem Description

Developers frequently encounter the following error when interacting with Flashbots:

```json
{
  "id": 1,
  "error": {
    "code": -32600,
    "message": "error in signature check 0xYOURADDRESS"
  },
  "jsonrpc": "2.0"
}
```

This error usually occurs due to improper message signing or Web3 version inconsistencies. This module was created to resolve these issues by ensuring correct message formatting and signing.

## How It Works

Flashbots requires correctly signed headers to send transactions. This module provides an easy-to-use interface to generate these signed headers while handling different Web3 versions seamlessly.

## Installation from Pip

Install package directly from Pip:

```bash
pip install flashbots-header-signer
```

## Installation from Github

Install package directly from GitHub:

```bash
pip install git+https://github.com/onium16/flashbots-header-signer.git
```

## Requirements

Install the required dependencies via pip:

```bash
pip install -r requirements.txt
```

## Installation for Test

Example for Web3 6.x.x:

```bash
pip install -r tests/requirements_6.txt
```

Example for Web3 7.x.x:

```bash
pip install -r tests/requirements_7.txt
```

## Usage Example (Basic)

```python
from flashbots_header_signer import FlashbotsHeaderSigner

FLASHBOTS_PRIVATE_KEY = "0x0000000000000000000000000000000000000000000000000000000000000001"

# URL for the Flashbots relay
url = "https://relay.flashbots.net/"

# Pass the private key to FlashbotsHeaderSigner
signer = FlashbotsHeaderSigner(private_key=FLASHBOTS_PRIVATE_KEY, log_level="DEBUG")

# Tx data in string format
tx_body = '{"jsonrpc": "2.0", "id": 1, "method": "eth_sendBundle", "params": [{"txs": ["0x0", "0x0", "0x0"], "blockNumber": "0x151962a", "minTimestamp": 0, "maxTimestamp": 0, "revertingTxHashes": []}]}'

# Generate Flashbots header (this method is not async but involves no async operations)
headers_json = signer.generate_flashbots_header(tx_body)
print(f"Generated headers: {headers_json}")
```

### Result:

```bash
Generated headers: {'Content-Type': 'application/json', 'X-Flashbots-Signature': '0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf:0x97a2015ef4e0360724deb78837826161d242cf16ac4d349078f8dd9b36b7db9e37748978438f57e8b5e10782126b07a6533b6b9362a3f9bfaa15f7c159ea6d731b'}
```

## Web3 Compatibility

This module automatically detects and handles Web3 versions `6.x.x` and `7.x.x`, signing the message accordingly.

## License

This project is open-source.\
GitHub Repository: [Flashbots Header Signer](https://github.com/onium16/flashbot_sign_header.git)


---

author: SeriouS

email: onium16@gmail.com

github: https://github.com/onium16