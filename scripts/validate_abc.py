#!/usr/bin/env python3
"""Regression tests for the approved 2026-09-30 A/B/C changes."""
import argparse
import base64
import json
import re
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import unquote

from build_metadata import ROOT, entries, geosite_rules, render, source_lines
from readme_tables import updated_readme

# Explicit scope approved by the owner. Exact-host exceptions use full:.
APPROVED = {
    "A01": "wbcontent.net",
    "A05": "xn--90aivcdt6dxbc.xn--p1ai",
    "A07": "pnp.ru",
    "B01": "lenta.tech full:lenta.digift.ru",
    "B02": "ivi.tv",
    "B03": "vkontakte.com vkuserlive.com",
    "B04": "cdn-vk.net vkcdnservice.com userapi.ru vktech-static.ru",
    "B05": "vkpay.ru vkpay.com vkpay.app vkpay.io",
    "B06": "okkoapi.tv",
    "B07": "tvgateway.ru yotaplay.ru okko.ru",
    "B08": "appsmail.ru attachmail.ru cdnmail.ru mrgcdn.ru smailru.net vmailru.net bizmrg.com mcs.st",
    "B09": "bk.ru list.ru inbox.ru internet.ru xmail.ru",
    "B10": "apiok.ru insideok.ru odkl.ru odnoklassniki.ru ok.me oktech.ru",
    "B11": "t-static.ru data-tscbank.ru tbank-online.com t-bank-app.ru",
    "B12": "mymts.ru mts-ws.net",
    "B13": "abonementx5.ru x5media.ru",
    "B14": "restream.ru",
    "B15": "rutube.sport",
    "B16": "ya.cc clck.ru",
    "B17": "yccdn.ru yndx.net static-storage.net yastatic-net.ru full:report.ap.yandex-net.ru clstorage.net",
    "B18": "payecom.ru platiecom.ru megamarket.tech",
    "B19": "paywb.ru wb-bank.ru wbstatic.ru wibes.com",
    "B20": "2gis.tech",
    "C01": "vedomosti.ru otr-online.ru tvc.ru tv3.ru mirtv.ru tnt-online.ru ctc.ru spastv.ru 5-tv.ru friday.ru domashniy.ru muz-tv.ru 360.ru radioplayer.ru",
    "C02": "lizaalert.org sirius.online full:m.47news.ru",
    "C03": "okmarket.ru burgerkingrus.ru rskrf.ru rsv.ru myrosmol.ru tvoyhod.online inspector.ru",
    "C04": "goskey.ru",
    "C05": "rustore.ru kion.ru mtsmusic.ru av.ru victoria-group.ru ertelecom.ru dom.ru",
    "C06": "s7.ru topdelivery.ru mcclinics.ru libreview.ru dnevnik.ru express.ms sferum.ru gibdd.ru",
}


def norm(line):
    core = line.split()[0]
    kind, value = core.split(":", 1) if ":" in core else ("domain", core)
    return kind, value.lower()


def expand(name, source, stack=()):
    assert name not in stack, f"Include cycle: {stack + (name,)}"
    assert name in source, f"Missing include: {name}"
    result = set()
    for line in source[name]:
        kind, value = norm(line)
        if kind == "include":
            # Current repository has no filtered include directives.
            assert "@" not in value, "Filtered includes require an attribute-aware parser"
            result.update(expand(value, source, stack + (name,)))
        else:
            result.add((kind, value))
    return result


def covered(rule, pool):
    kind, value = rule
    if rule in pool:
        return True
    if kind not in ("domain", "full"):
        return False
    labels = value.split(".")
    return any(("domain", ".".join(labels[i:])) in pool for i in range(len(labels)))


def baseline_checks(ref, data):
    def old(path):
        return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{ref}:{path}"])

    unchanged = ["geoip.dat", "geoip-config.json"]
    unchanged += [str(p.relative_to(ROOT)) for p in (ROOT / "data-geoip").glob("*")]
    for client in ("HAPP", "INCY"):
        for profile in ("WHITELIST", "JSONSUB"):
            unchanged += [f"{client}/{profile}.{suffix}"
                          for suffix in ("JSON", "DEEPLINK", "QR.png")]
        path = f"{client}/DEFAULT.JSON"
        before = json.loads(old(path))
        after = json.loads((ROOT / path).read_text())
        before["DirectSites"].remove("geosite:mailru")
        before["LastUpdated"] = after["LastUpdated"]
        assert before == after, f"Unexpected profile change: {path}"
    for path in unchanged:
        assert old(path) == (ROOT / path).read_bytes(), f"Unexpected change: {path}"
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "baseline.dat"
        path.write_bytes(old("geosite.dat"))
        previous = geosite_rules(path)
    wl_before = previous["category-ru-whitelist"]
    wl_after = data["category-ru-whitelist"]
    approved = {norm(v) for group in APPROVED.values() for v in group.split()}
    additions = {r for r in wl_after if not covered(r, wl_before)}
    removals = {r for r in wl_before if not covered(r, wl_after)}
    assert additions <= approved, f"Unapproved additions: {additions - approved}"
    allowed_removals = {("domain", v) for v in
                        ("satellite.online", "explain.rf", "obyasnyaem.rf",
                         "inme.pressure", "icq.com")}
    assert removals <= allowed_removals, f"Unapproved removals: {removals - allowed_removals}"
    assert data["twitch-ads"] == previous["twitch"]
    for category in ("category-ban-ru", "google", "google-play", "youtube",
                     "telegram", "apple", "private"):
        assert data[category] == previous[category], f"Unexpected change: {category}"
    print(f"PASS: baseline {ref}: whitelist {len(wl_before)} -> {len(wl_after)}, "
          f"{len(additions)} new coverage rules, {len(removals)} removed")
    print("PASS: GeoIP, WHITELIST/JSONSUB files and block D profile settings unchanged")
    print("PASS: legacy Twitch set preserved exactly in twitch-ads")


def validate(qr=False, baseline=None):
    source = {p.name: source_lines(p) for p in (ROOT / "data-geosite").iterdir()
              if p.is_file()}
    data = geosite_rules(ROOT / "geosite.dat")
    assert set(source) == set(data), "Source/binary category mismatch"
    for name in source:
        original = expand(name, source)
        assert all(covered(r, data[name]) for r in original), f"Uncompiled source: {name}"
        assert all(covered(r, original) for r in data[name]), f"Unexpected binary rule: {name}"
    whitelist = data["category-ru-whitelist"]
    for group, values in APPROVED.items():
        for value in values.split():
            assert covered(norm(value), whitelist), f"Missing {group}: {value}"
    for value in ("satellite.online", "explain.rf", "obyasnyaem.rf", "inme.pressure"):
        assert not covered(("full", value), whitelist), f"Removed domain still covered: {value}"
    assert not covered(("full", "icq.com"), data["ru-transport"])
    for exact in ("lenta.digift.ru", "m.47news.ru", "report.ap.yandex-net.ru"):
        assert ("full", exact) in whitelist
        assert not covered(("full", "unapproved." + exact), whitelist)
        assert not covered(("full", exact.split(".", 1)[1]), whitelist)
    # Approved 2026-10-05: YouTube Google dependencies (changes/2026-10-05-youtube.md).
    assert ("full", "jnn-pa.googleapis.com") in data["youtube"]
    assert not covered(("full", "other.jnn-pa.googleapis.com"), data["youtube"])
    assert not covered(("full", "www.googleapis.com"), data["youtube"])
    assert covered(("full", "redirector.gvt1.com"), data["youtube"])
    assert len(data["twitch"]) == 34
    assert len(data["twitch-ads"]) == 11
    for root in ("twitch.tv", "ttvnw.net", "jtvnw.net", "twitchcdn.net", "live-video.net"):
        assert covered(("domain", root), data["twitch"])
        assert not covered(("domain", root), whitelist)
    ipcats = entries(ROOT / "geoip.dat")
    profiles = sorted(ROOT.glob("*/*.JSON"))
    assert len(profiles) == 6
    for path in profiles:
        profile = json.loads(path.read_text())
        for kind, name in re.findall(r"\b(geosite|geoip):([\w-]+)", path.read_text()):
            assert name.lower() in (data if kind == "geosite" else ipcats), (path, name)
        link = path.with_suffix(".DEEPLINK").read_text().strip()
        assert link.startswith(path.parent.name.lower() + "://routing/onadd/")
        payload = unquote(link.split("/onadd/", 1)[1])
        assert json.loads(base64.b64decode(payload)) == profile, path
        assert "geosite:twitch" not in path.read_text()
        assert "geosite:twitch-ads" not in path.read_text()
        if qr and path.stem == "DEFAULT":
            import zxingcpp
            from PIL import Image
            codes = zxingcpp.read_barcodes(Image.open(path.with_suffix(".QR.png")))
            assert len(codes) == 1 and codes[0].text == link, f"QR mismatch: {path}"
    assert (ROOT / "CATEGORY_STATS.md").read_text() == render()
    assert (ROOT / "README.md").read_text() == updated_readme(), "README tables are stale"
    print(f"PASS: {len(data)} geosite categories match effective source")
    print(f"PASS: {sum(len(v.split()) for v in APPROVED.values())} approved domain rules covered")
    print(f"PASS: {len(whitelist)} compiled whitelist rules; exact-host boundaries retained")
    print("PASS: removals, Twitch split, 6 profile references/deeplinks, build statistics and README tables")
    print("PASS: YouTube dependencies jnn-pa.googleapis.com (exact) and gvt1.com retained")
    if qr:
        print("PASS: both DEFAULT QR codes decode to their current deeplinks")
    if baseline:
        baseline_checks(baseline, data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--qr", action="store_true")
    parser.add_argument("--baseline", help="Optional git ref to check the approved change scope")
    args = parser.parse_args()
    validate(args.qr, args.baseline)
