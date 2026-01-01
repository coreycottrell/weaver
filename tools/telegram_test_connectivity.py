#!/usr/bin/env python3
"""
Test Telegram API connectivity with alternate IPs.
Bypasses DNS issues by connecting directly to working IP addresses.

Usage: python3 telegram_test_connectivity.py
"""

import socket
import urllib3.util.connection as urllib3_connection

# Working Telegram IPs (bypassing blocked 149.154.167.220)
WORKING_IPS = [
    "149.154.175.50",   # Best: 14.6ms
    "91.108.4.170",     # Backup: 115ms
    "91.108.56.130",    # Backup: 239ms
]

_dns_override = {}

def patched_create_connection(address, *args, **kwargs):
    """Create connection with DNS override."""
    from urllib3.util.connection import create_connection as orig_create
    host, port = address
    if host in _dns_override:
        host = _dns_override[host]
    return orig_create((host, port), *args, **kwargs)


def test_connectivity():
    """Test connectivity to each Telegram IP."""
    import requests

    # Apply DNS override patch
    original_create = urllib3_connection.create_connection
    urllib3_connection.create_connection = patched_create_connection

    print("Testing Telegram API connectivity...")
    print("=" * 50)

    for ip in WORKING_IPS:
        print(f"\nTrying {ip}...")
        _dns_override['api.telegram.org'] = ip

        try:
            # Simple GET to check connectivity (doesn't need token)
            response = requests.get(
                "https://api.telegram.org/",
                timeout=10
            )
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text[:100]}...")
            print(f"  SUCCESS - IP {ip} is reachable!")

            # Restore and return first working IP
            urllib3_connection.create_connection = original_create
            return ip

        except requests.exceptions.SSLError as e:
            print(f"  SSL Error: {e}")
        except requests.exceptions.Timeout:
            print(f"  Timeout")
        except requests.exceptions.ConnectionError as e:
            print(f"  Connection Error: {e}")
        except Exception as e:
            print(f"  Error: {type(e).__name__}: {e}")

    urllib3_connection.create_connection = original_create
    print("\nAll IPs failed!")
    return None


if __name__ == "__main__":
    working_ip = test_connectivity()
    if working_ip:
        print(f"\n{'=' * 50}")
        print(f"WORKING IP FOUND: {working_ip}")
        print(f"{'=' * 50}")
