# Device-Locked License Key System

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![Status](https://img.shields.io/badge/status-active-success)

**Author:** S4D0X-dev (Mr. FBA)

A lightweight, zero-dependency license key system written in pure Python. It binds license keys to a specific machine using hardware/OS fingerprints and embeds a customizable **validity duration (in days)** directly inside the key.

## How it works

1. **Fingerprint the device.** `Device_fingerprint.py` generates a deterministic short ID for the host machine using its MAC address, hostname, and OS name.
2. **Generate a license.** `Generator.py` bundles a random serial number and an expiration period (e.g., 30 or 90 days), then signs them together with the device ID using an HMAC-SHA256 checksum. 
3. **Validate a license.** `Validator.py` checks the key's integrity, confirms it matches the current machine's fingerprint, and extracts the embedded serial number and remaining validity days[cite: 4].

Because the checksum incorporates the device fingerprint, a license generated for one PC will fail on another.

## Files

| File | Purpose |
|---|---|
| `Device_fingerprint.py` | Computes an 8-character hex device ID from `uuid.getnode()`, `platform.node()`, and `platform.system()`, hashed via SHA-256[cite: 4]. |
| `Generator.py` | CLI tool to generate a time-bound license key for a target machine ID, serial, and days count. |
| `Validator.py` | CLI tool to check key validity, verify device compatibility, and read out the embedded serial and validity duration. |

## Usage

### 1. Get the device ID on the target machine

```bash
python Device_fingerprint.py