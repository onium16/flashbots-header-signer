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
