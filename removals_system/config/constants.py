import os


ASSET_MAP = {
    "hero-truck": ("assets", "hero-truck.png"),
    "logo-black": ("assets", "logo-black-transparent.png"),
    "chevron-down": ("assets", "icons", "chevron-down.svg")
}

for asset_name, asset_path in ASSET_MAP.items():
    ASSET_MAP[asset_name] = os.path.join("removals_system", *asset_path)
