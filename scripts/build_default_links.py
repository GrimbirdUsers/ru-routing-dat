#!/usr/bin/env python3
"""Regenerate DEFAULT derivatives only; preserve profile settings and other profiles."""
import base64
import json
from pathlib import Path

import qrcode

ROOT = Path(__file__).resolve().parents[1]

for client in ("HAPP", "INCY"):
    profile = ROOT / client / "DEFAULT.JSON"
    payload = json.loads(profile.read_text())
    compact = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()
    uri = f"{client.lower()}://routing/onadd/" + base64.b64encode(compact).decode()
    profile.with_suffix(".DEEPLINK").write_text(uri + "\n")
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=8, border=4)
    qr.add_data(uri)
    qr.make(fit=True)
    qr.make_image(fill_color="black", back_color="white").save(
        profile.with_suffix(".QR.png"))
    print(f"Generated {client}/DEFAULT: {len(uri)} URI bytes, QR version {qr.version}")
