import os
import json
from datetime import datetime, timedelta


APP_NAME = "SmartShot"
TRIAL_DAYS = 7

LICENSE_FILE = os.path.join(
    os.getenv("APPDATA"),
    APP_NAME,
    "license.json"
)


def _today():
    return datetime.now().date()


def _ensure_dir():
    os.makedirs(os.path.dirname(LICENSE_FILE), exist_ok=True)


def load_license():
    print("Reading license from:", LICENSE_FILE)

    if not os.path.exists(LICENSE_FILE):
        return None

    with open(LICENSE_FILE, "r") as f:
        return json.load(f)


def save_license(data):
    _ensure_dir()
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def initialize_trial():
    """
    Call once on app startup.
    Creates license.json on first run.
    """
    if os.path.exists(LICENSE_FILE):
        return

    data = {
        "install_date": _today().isoformat(),
        "trial_days": TRIAL_DAYS,
        "activated": False,
        "license_key": None
    }

    save_license(data)


def days_left():
    data = load_license()
    if not data:
        return 0

    install_date = datetime.fromisoformat(data["install_date"]).date()
    expiry_date = install_date + timedelta(days=data["trial_days"])

    remaining = (expiry_date - _today()).days
    return max(remaining, 0)


def is_trial_valid():
    """
    Returns True if:
    - activated OR
    - still within trial period
    """
    data = load_license()
    if not data:
        return False

    if data.get("activated"):
        return True

    return days_left() > 0

def activate_license(license_key: str) -> bool:
    """
    v1 activation:
    - simple local validation
    - unlock permanently
    """
    if not license_key or len(license_key.strip()) < 10:
        return False

    data = load_license()
    if not data:
        return False

    data["activated"] = True
    data["license_key"] = license_key.strip()
    save_license(data)
    return True


def is_activated():
    data = load_license()
    return bool(data and data.get("activated"))
