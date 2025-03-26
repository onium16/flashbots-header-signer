
## Flashbots Header Signer

This module provides a utility for creating signed headers to interact with the Flashbots service. It helps address issues with Web3 version compatibility when making requests to Flashbots.

### Problem Description

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

### How It Works

Flashbots requires correctly signed headers to send transactions. This module provides an easy-to-use interface to generate these signed headers while handling different Web3 versions seamlessly.

### Installation

 Install your package directly from GitHub:

```bash 
pip install git+https://github.com/onium16/flashbots-header-signer.git
```

### Requirements

Install the required dependencies via pip:

```bash
pip install -r requirements.txt
```

### Installation for test

Example for Web3 6.x.x
```bash
pip install -r tests/requirements_6.txt
```
Example for Web3 7.x.x
```bash
pip install -r tests/requirements_7.txt
```

### Usage Example (Basic)

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
Result:

```bash

Generated headers: {'Content-Type': 'application/json', 'X-Flashbots-Signature': '0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf:0x97a2015ef4e0360724deb78837826161d242cf16ac4d349078f8dd9b36b7db9e37748978438f57e8b5e10782126b07a6533b6b9362a3f9bfaa15f7c159ea6d731b'}

```


### Usage Example (Advanced)

```python
# example.py

import asyncio
import logging

import aiohttp
from flashbots_header_signer import FlashbotsHeaderSigner
from eth_account import Account

# Configure logging
logging.basicConfig(
                    level=logging.DEBUG,
                    format="%(asctime)s [%(levelname)s] Line: %(lineno)d - %(message)s"
                    )
logger = logging.getLogger(__name__)

def _generate_private_key():
    """
    Generates a new Ethereum private key and address.
    
    Returns:
        private_key (str): The newly generated Ethereum private key in hexadecimal format.
        address (str): The Ethereum address associated with the private key.
    """
    account = Account.create()

    # Access the private key correctly using _private_key
    private_key = account._private_key.hex()
    address = account.address

    logger.debug(f"New private key: {private_key[:5]+'...'+private_key[-5:]}")
    logger.debug(f"New address: {address[:5]+'...'+address[-5:]}")
    
    return private_key, address

async def main():
    try:
        # Generate private key and address
        FLASHBOTS_PRIVATE_KEY = "0x0000000000000000000000000000000000000000000000000000000000000001"
        # FLASHBOTS_PRIVATE_KEY, FLASHBOTS_ADDRESS = _generate_private_key()
        
        # Pass the private key to FlashbotsHeaderSigner
        signer = FlashbotsHeaderSigner(private_key=FLASHBOTS_PRIVATE_KEY, log_level="DEBUG")
        
        url = "https://relay.flashbots.net/"

        tx_body = '{"jsonrpc": "2.0", "id": 1, "method": "eth_sendBundle", "params": [{"txs": ["0x0", "0x0", "0x0"], "blockNumber": "0x151962a", "minTimestamp": 0, "maxTimestamp": 0, "revertingTxHashes": []}]}'

        try:
            # Generate Flashbots header (this method is not async but involves no async operations)
            headers_json = signer.generate_flashbots_header(tx_body)
            logger.debug(f"Generated headers: {headers_json}")

        except TypeError as e:
            logger.error(f"Error generating Flashbots header: {e}")
            return
        except Exception as e:
            logger.error(f"Unexpected error during header generation: {e}")
            return

        try:
            # Send the request to Flashbots (this is async and should be awaited)
            response = await signer.send_request(url, headers_json, tx_body)
            logger.info(f"Final Response: {response}")
        except aiohttp.ClientError as e:
            logger.error(f"HTTP error occurred while sending the request: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while sending the request: {e}")

    except ValueError as e:
        logger.error(f"ValueError: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in main function: {e}")



if __name__ == "__main__":
    asyncio.run(main())

```

### Expected Output:

    ```
    Web3 6.x.x Output:

    Using Web3 version: 6.20.3
    Signing with Web3 6.x: Hello, EIP-191!
    keccak_res: 0xb5d15353a83fd0dbce1f514c755961efd5a535ebe1ac66a465647467e206d842
    SignableMessage: SignableMessage(version=b'E', header=b'Ethereum Signed Message:\n66', body=b'0xb5d15353a83fd0dbce1f514c755961efd5a535ebe1ac66a465647467e206d842')
    Signature: 0xDe518f63B0776867407A09039D5426B0f04Fe299:0xdb41be864a2d50dd3e72d3c45091287de4298edd6b6adeae2f84615d146c46372fd7245e248b70d37598344e89f110a1c5790b4ca3562665a51a557d966fb0ea1c
    ```
    ```
    Web3 7.x.x Output:

    Using Web3 version: 7.6.1
    Signing with Web3 7.x: Hello, EIP-191!
    keccak_res: 0xb5d15353a83fd0dbce1f514c755961efd5a535ebe1ac66a465647467e206d842
    SignableMessage: SignableMessage(version=b'E', header=b'Ethereum Signed Message:\n66', body=b'0xb5d15353a83fd0dbce1f514c755961efd5a535ebe1ac66a465647467e206d842')
    Signature: 0xDe518f63B0776867407A09039D5426B0f04Fe299:0xdb41be864a2d50dd3e72d3c45091287de4298edd6b6adeae2f84615d146c46372fd7245e248b70d37598344e89f110a1c5790b4ca3562665a51a557d966fb0ea1c
    ```


### Web3 Compatibility

This module automatically detects and handles Web3 versions `6.x.x` and `7.x.x`, signing the message accordingly. Make sure you have the correct version of Web3 installed for the desired compatibility.

### Official Documentation

For more details on how Flashbots works, visit:  
[Flashbots Documentation](https://flashbots.net)

### License

This project is open-source and can be freely used in any project. You are welcome to integrate and modify it as needed.  
Source code is available on GitHub: [Flashbots Header Signer](https://github.com/onium16/flashbot_sign_header.git)

---

author: SeriouS

email: onium16@gmail.com