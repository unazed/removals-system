from pathlib import Path
import os


ASSET_MAP: dict[str, str] = {
    "hero-truck": "hero-truck.png",
    "logo-black": "logo-black-transparent.png",
    "logo-white": "logo-white-transparent.png",
    "customer-card": "customer-placeholder.png",
    "service-provider-card": "service-provider-placeholder.png",
    "chevron-down": ("icons", "chevron-down.svg"),
    "calendar": ("icons", "calendar.svg"),
    "table-of-contents": ("icons", "table-of-contents.svg"),
    "calendar-plus": ("icons", "calendar-plus.svg"),
    "hand-coins": ("icons", "hand-coins.svg"),
    "user": ("icons", "user.svg"),
    "log-out": ("icons", "log-out.svg")
}

for asset_name, asset_path in ASSET_MAP.items():
    if isinstance(asset_path, tuple):
        asset_path = os.path.join(*asset_path)
    ASSET_MAP[asset_name] = Path(
        os.path.join("removals_system", "assets", asset_path)
    ).as_posix()
    if not os.path.isfile(ASSET_MAP[asset_name]):
        raise FileNotFoundError(
            f"Asset file listed, but doesn't exist: {ASSET_MAP[asset_name]}"
        )