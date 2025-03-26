# conftest.py

import pytest
from flashbots_header_signer import FlashbotsHeaderSigner


private_key_true = "0x0000000000000000000000000000000000000000000000000000000000000001"

headers_true =  '{"Content-Type": "application/json", "X-Flashbots-Signature": "0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf:0x97a2015ef4e0360724deb78837826161d242cf16ac4d349078f8dd9b36b7db9e37748978438f57e8b5e10782126b07a6533b6b9362a3f9bfaa15f7c159ea6d731b"}'

tx_body_true ='{"jsonrpc": "2.0", "id": 1, "method": "eth_sendBundle", "params": [{"txs": ["0x0", "0x0", "0x0"], "blockNumber": "0x151962a", "minTimestamp": 0, "maxTimestamp": 0, "revertingTxHashes": []}]}'

url_true = "https://relay.flashbots.net/"
url_test = "https://tests_flashbots_net"

mock_post_response_success = '{"id": 1, "result": {"bundleHash": "0x9000000000000000000000000000000000000000000000000000000000000009"}, "jsonrpc": "2.0"}'

# Mock response for an API error (400 Bad Request)
mock_response_error_400 = '''{
                "error": {
                    "code": -32000,
                    "message": "Invalid transaction"
                }
            }'''

# Mock response for 403 Forbidden
mock_response_error_403 = '''{
                "error": {
                    "code": -32003,
                    "message": "Forbidden access"
                }
            }'''

# Mock response for 502 Bad Gateway
mock_response_error_502 = '''{
    "error": {
        "code": -32002,
        "message": "Bad gateway error"
    }
}'''


@pytest.fixture
def flashbots_data():
    return {
        "private_key_true": private_key_true,
        "headers_true": headers_true,
        "tx_body_true": tx_body_true,
        "response_true": mock_post_response_success,
        "url_true": url_true,
        "mock_response_error_400": mock_response_error_400,
        "mock_response_error_403": mock_response_error_403,
        "mock_response_error_502": mock_response_error_502
    }
