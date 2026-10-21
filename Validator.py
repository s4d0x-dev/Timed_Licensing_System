import hmac
import hashlib
from Device_fingerprint import Device_ID

devID = Device_ID()
SECRET_KEY = bytes.fromhex("7678a6c6786d7678e678f68976a67d767c867ef6768a6786fe7686a7686ee76c")

class License_Validator:
    def __init__(self, license_key: str, secret_key: bytes) -> None:
        self.license_key = license_key
        self.secret_key = secret_key

    def validate_license(self) -> dict | None:
        hex_2_str = self.license_key.replace("-", "").replace(" ", "")
        if len(hex_2_str) != 32:
            return None

        try:
            raw = bytes.fromhex(hex_2_str)
        except ValueError:
            return None

        payload = raw[:6]         # First 6 bytes (4 bytes serial + 2 bytes days)
        given_checksum = raw[6:]  # Remaining 10 bytes checksum

        fingerprint_bytes = bytes.fromhex(devID.get_device_id())
        expected_checksum = hmac.new(self.secret_key, payload + fingerprint_bytes, hashlib.sha256).digest()[:10]

        # Securely verify integrity and device match
        if not hmac.compare_digest(given_checksum, expected_checksum):
            return None

        # Extract values
        serial = int.from_bytes(payload[:4], "big")
        days = int.from_bytes(payload[4:6], "big")

        return {"serial": serial, "days": days}

class CLI:
    def run(self):
        user_license_key = input("Please insert your License Key: ")
        
        validator = License_Validator(user_license_key, SECRET_KEY)
        result = validator.validate_license()

        if result is not None:
            print("\n[+] License Validated Successfully!")
            print(f"Serial Number:  {result['serial']}")
            print(f"Valid For:      {result['days']} days\n")
            # TODO: Save expiration timestamp / activate app features locally
        else:
            print("\n[-] Invalid License Key or Device Mismatch!\n")

if __name__ == "__main__":
    CLI().run()