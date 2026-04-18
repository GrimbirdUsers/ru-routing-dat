# ru-routing-dat

Custom `geosite.dat` + `geoip.dat` for Russian split-tunneling in Happ / Xray / v2ray / sing-box.

Combines [frayZV/simple-ru-geosite](https://github.com/frayZV/simple-ru-geosite) (regional RU domains, Apple/Google stack, VK/Yandex ecosystems) with custom categories for 2GIS, Russian TV, medical CGM devices, MOEX, banks, and per-ASN IP blocks for precise routing.

## Download URLs

**Recommended (fast CDN via jsDelivr):**
- [geosite.dat](https://cdn.jsdelivr.net/gh/GrimbirdUsers/ru-routing-dat@main/geosite.dat)
  `https://cdn.jsdelivr.net/gh/GrimbirdUsers/ru-routing-dat@main/geosite.dat`
- [geoip.dat](https://cdn.jsdelivr.net/gh/GrimbirdUsers/ru-routing-dat@main/geoip.dat)
  `https://cdn.jsdelivr.net/gh/GrimbirdUsers/ru-routing-dat@main/geoip.dat`

**Direct from GitHub:**
- `https://github.com/GrimbirdUsers/ru-routing-dat/raw/main/geosite.dat`
- `https://github.com/GrimbirdUsers/ru-routing-dat/raw/main/geoip.dat`

## geosite.dat — 38 categories, ~10 500 domain entries

### RU services (whitelist)
| Category | Entries | Coverage |
|---|---|---|
| `category-ru` | 112 | Generic .ru/.su/.рф/.moscow anchors + top services |
| `category-gov-ru` | 119 | gosuslugi, nalog, cbr, mos.ru, regional *.ru |
| `category-ru-all` | 138 | Meta: includes all RU whitelists below |
| `wildberries` | 9 | wildberries.ru, wb.ru, wbbasket, paywb, wibes |
| `ozon` | 3 | ozon.ru, ozone.ru, ozonusercontent.com |
| `yandex` | 56 | yandex.*, ya.ru, turbopages, adfox, webvisor |
| `vk` | 36 | vk.com/ru/me, userapi, vkcache, vk-cdn |
| `mailru-group` | 46 | mail.ru + ok.ru + dzen.ru + VK stack |
| `avito`, `dzen`, `rutube`, `okko`, `wink`, `ok` | 2-3 each | Media |
| `x5` | 30 | Перекрёсток, Пятёрочка, Чижик, 5post |

### Custom additions (not in upstream)
| Category | Entries |
|---|---|
| `2gis` | 3 |
| `ru-tv` | 7 (ren.tv, russia.tv, vgtrk, more.tv, premier.one, vitrina.tv) |
| `ru-medical` | 8 (Medtrum, Sinocare, POCTech, iCan, Yuwell — CGM/glucometer devices) |
| `ru-finance` | 2 (moex.com, honestmark.org) |
| `ru-transport` | 4 (pobeda.aero, routeq, youdrive, icq) |
| `ru-banks` | 29 (Sberbank, Tinkoff/T-Bank, Alfa, VTB, Gazprombank, Raiffeisen, etc.) |

### Blacklist
- `category-ban-ru`: 7029 entries (blocked-in-RU content, antifilter/refilter sourced)

### Western ecosystems
`apple` (1583), `beats` (716), `icloud` (51), `itunes` (52), `apple-update`, `apple-dev`, `apple-ads`, `apple-pki`, `apple-tvplus`, `icloudprivaterelay`, `google-play` (9), `youtube` (177), `twitch` (11), `swift` (4), `mailru` (2)

## geoip.dat — 7 categories, ~25 430 CIDR blocks

| Category | CIDRs | Purpose |
|---|---|---|
| `ru` | 25 369 (13 379 IPv4 + 11 990 IPv6) | Full Russia IP space, ~45M addresses |
| `private` | 18 | RFC1918 + link-local |
| `ru-wildberries` | 8 | AS57073 + AS201513 + AS49053 |
| `ru-yandex` | 15 | AS13238 |
| `ru-vk` | 5 | AS47541 |
| `ru-mts` | 3 | AS8359 |
| `ru-banks` | 11 | Aggregated banking ASNs |

## Usage in Happ

```json
{
  "Geositeurl": "https://cdn.jsdelivr.net/gh/GrimbirdUsers/ru-routing-dat@main/geosite.dat",
  "Geoipurl":   "https://cdn.jsdelivr.net/gh/GrimbirdUsers/ru-routing-dat@main/geoip.dat",
  "DirectSites": ["geosite:category-ru-all"],
  "DirectIp":    ["geoip:ru", "geoip:private"],
  "RouteOrder":  "block-proxy-direct"
}
```

## Usage in Xray / v2ray

```json
"routing": {
  "rules": [
    {"type":"field","outboundTag":"direct","domain":["geosite:category-ru-all"]},
    {"type":"field","outboundTag":"direct","ip":["geoip:ru","geoip:private"]}
  ]
}
```

## Updates

Automated weekly update every Sunday 03:00 MSK — checks frayZV upstream + news sources for new RU services, rebuilds and pushes to `main`.

## Sources

- [frayZV/simple-ru-geoip](https://github.com/frayZV/simple-ru-geoip) (weekly geoip base, antifilter+refilter)
- [frayZV/simple-ru-geosite](https://github.com/frayZV/simple-ru-geosite) (v2fly+antifilter geosite base)
- [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist)
- [T—Ж full whitelist](https://t-j.ru/full-whitelist/)
- [RIPE stat](https://stat.ripe.net/)

## License

Upstream sources retain their original licenses. Custom additions MIT.
