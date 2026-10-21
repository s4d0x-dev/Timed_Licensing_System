import hmac
import hashlib
import secrets
from Device_fingerprint import Device_ID

SECRET_KEY = bytes.fromhex("7678a6c6786d7678e678f68976a67d767c867ef6768a6786fe7686a7686ee76c")

class License_Generator:
    def __init__(self, serial: int, days: int, machine_hex_id: str, secret_key: bytes) -> None:
        self.serial = serial
        self.days = days
        self.machine_hex_id = machine_hex_id
        self.secret_key = secret_key

    def generate_license_key(self) -> str:
        serial_bytes = self.serial.to_bytes(4, "big")
        days_bytes = self.days.to_bytes(2, "big")
        fingerprint_bytes = bytes.fromhex(self.machine_hex_id)

        # Combine serial and validity days into the payload
        payload = serial_bytes + days_bytes
        
        # Generate HMAC checksum over payload + device fingerprint
        checksum = hmac.new(self.secret_key, payload + fingerprint_bytes, hashlib.sha256).digest()[:10]

        raw = payload + checksum
        hex_str = raw.hex().upper()

        return "-".join(hex_str[i:i + 4] for i in range(0, len(hex_str), 4))


class CLI:
    def run(self):
        cust_dev_ID = input("Target Device ID (Press Enter to use local): ").strip()
        devID = Device_ID()
        customer_machin_ID = cust_dev_ID if cust_dev_ID else devID.get_device_id()
        
        try:
            days = int(input("Validity Duration in Days (e.g., 30, 90): ") or "30")
        except ValueError:
            days = 30

        serial = secrets.randbelow(2**32)
        lg = License_Generator(serial=serial, days=days, machine_hex_id=customer_machin_ID, secret_key=SECRET_KEY)
        key = lg.generate_license_key()
        
        print(f"\nTarget Machine ID:  {customer_machin_ID}")
        print(f"Serial:             {serial}")
        print(f"Validity:           {days} Days")
        print(f"License Key:        {key}\n")


if __name__ == "__main__":
    CLI().run()