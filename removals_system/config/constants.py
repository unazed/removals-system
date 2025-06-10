import os


ASSET_MAP: dict[str, str] = {
    "hero-truck": ("assets", "hero-truck.png"),
    "logo-black": ("assets", "logo-black-transparent.png"),
    "customer-card": ("assets", "customer-placeholder.png"),
    "service-provider-card": ("assets", "service-provider-placeholder.png")
}

for asset_name, asset_path in ASSET_MAP.items():
    ASSET_MAP[asset_name] = os.path.join("removals_system", *asset_path)
