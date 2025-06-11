import os


ASSET_MAP: dict[str, str] = {
    "hero-truck": "hero-truck.png",
    "logo-black": "logo-black-transparent.png",
    "customer-card": "customer-placeholder.png",
    "service-provider-card": "service-provider-placeholder.png",
    "chevron-down": ("icons", "chevron-down.svg"),
    "calendar": ("icons", "calendar.svg")
}

for asset_name, asset_path in ASSET_MAP.items():
    if isinstance(asset_path, tuple):
        asset_path = os.path.join(*asset_path)
    ASSET_MAP[asset_name] = os.path.join("removals_system", "assets", asset_path)
