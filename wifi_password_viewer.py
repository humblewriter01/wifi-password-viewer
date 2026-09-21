"""
Saved Wi-Fi Password Viewer (Windows)

Retrieves the password for a Wi-Fi network that this computer has
already connected to and saved a profile for. It does NOT access,
crack, or attack any network you have not already connected to.

Legitimate uses:
  - You forgot the password to a Wi-Fi network your own device
    already knows, and you want to share it with another device.
  - IT / helpdesk recovering a saved profile's credentials on a
    machine you administer, with authorization.

This relies entirely on Windows' built-in `netsh wlan` command and
only surfaces information already stored on this machine by Windows
itself. It will not reveal passwords for networks you have never
connected to on this device.
"""

import subprocess
import sys
import re


def run_netsh(args: list[str]) -> str:
    """Run a netsh command and return its stdout, raising on failure."""
    result = subprocess.run(
        ["netsh", *args],
        capture_output=True,
        text=True,
        shell=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "netsh command failed")
    return result.stdout


def list_saved_profiles() -> list[str]:
    """Return the names of all saved Wi-Fi profiles on this machine."""
    output = run_netsh(["wlan", "show", "profiles"])
    return re.findall(r"All User Profile\s*:\s*(.+)", output)


def get_profile_password(ssid: str) -> str | None:
    """Return the saved password for a given SSID, or None if unset/open."""
    output = run_netsh(["wlan", "show", "profile", f"name={ssid}", "key=clear"])
    match = re.search(r"Key Content\s*:\s*(.+)", output)
    return match.group(1).strip() if match else None


def main() -> None:
    if sys.platform != "win32":
        print("This tool relies on Windows' netsh command and only runs on Windows.")
        sys.exit(1)

    try:
        profiles = list_saved_profiles()
    except RuntimeError as exc:
        print(f"Could not list saved Wi-Fi profiles: {exc}")
        sys.exit(1)

    if not profiles:
        print("No saved Wi-Fi profiles found on this machine.")
        sys.exit(0)

    print("Saved Wi-Fi profiles on this machine:")
    for i, name in enumerate(profiles, start=1):
        print(f"  {i}. {name}")

    choice = input("\nEnter the exact SSID you'd like the saved password for: ").strip()
    if choice not in profiles:
        print(f"'{choice}' is not a saved profile on this machine.")
        sys.exit(1)

    try:
        password = get_profile_password(choice)
    except RuntimeError as exc:
        print(f"Could not read profile '{choice}': {exc}")
        sys.exit(1)

    if password:
        print(f"\nSSID: {choice}\nPassword: {password}")
    else:
        print(f"\nSSID: {choice}\nNo password stored (open network, or key not saved in clear text).")


if __name__ == "__main__":
    main()
  
