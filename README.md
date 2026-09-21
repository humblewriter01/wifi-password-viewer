# Saved Wi-Fi Password Viewer

A small Windows utility that retrieves the password for a Wi-Fi network **this computer has already connected to and saved**. It does not access, crack, or attack networks the device hasn't already joined.

## What it actually does

Windows stores a "profile" (including the password, if you chose to save it) for every Wi-Fi network you connect to. This script wraps the built-in `netsh wlan` command to:

1. List every saved Wi-Fi profile on the current machine
2. Let you pick one by SSID
3. Reveal the saved password for that profile, in clear text

This is the same information you could get manually by running `netsh wlan show profile name="SSID" key=clear` yourself, or by digging through Windows' Network and Sharing Center UI. The script just automates it.

## What it does **not** do

This is not a Wi-Fi hacking / cracking tool, and it has intentionally **not** been extended into one. It cannot and will not:

- Access, join, or reveal passwords for networks this device has never connected to
- Capture or crack WPA/WPA2 handshakes
- Deauthenticate other devices from a network
- Sniff or inject packets on networks you don't control

If you're looking to get into offensive security / ethical hacking, the legitimate path is a structured, hands-on program (e.g. OSCP, eJPT, or a home lab with your own router) — not scripts aimed at networks you don't own or have explicit written permission to test.

## Legitimate use cases

- Recovering a Wi-Fi password your own device has saved, to share it with another device or write it down
- IT/helpdesk staff recovering a saved profile's credentials on a machine they administer, with authorization
- Personal device migration/backup

## Requirements

- Windows (uses the built-in `netsh` command — there is no macOS/Linux equivalent for this script)
- Python 3.9+

## Usage

```bash
python wifi_password_viewer.py
```

You'll see a numbered list of saved networks, then be prompted to enter the exact SSID you want the password for.

## Legal / ethical note

Only run this against your own devices, or devices/networks you are explicitly authorized to administer. Using saved-credential or network tools against systems you don't own or lack permission to access is illegal in most jurisdictions (e.g., under the U.S. Computer Fraud and Abuse Act and equivalent laws elsewhere), regardless of how the tool works technically.

## License

No license specified.
