import hashlib
import platform
import uuid

class Device_ID:
    def __init__(self) -> None:
        pass

    @staticmethod
    def _get_device_fingerprint() -> bytes:
        raw = f"{uuid.getnode()}|{platform.node()}|{platform.system()}".encode()
        degist = hashlib.sha256(raw).digest()
        return degist[:4]
    
    def get_device_id(self) -> str:
        return self._get_device_fingerprint().hex().upper()

if __name__ == "__main__":
    devID = Device_ID()
    print("Your Device ID:", devID.get_device_id())