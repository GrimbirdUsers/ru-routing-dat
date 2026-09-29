#!/usr/bin/env python3
"""Generate detailed README tables from the actual databases and profile JSON."""
import ipaddress
import json

from build_metadata import ROOT, entries, fields, geosite_rules

BEGIN = "<!-- BEGIN GENERATED ROUTING TABLES -->"
END = "<!-- END GENERATED ROUTING TABLES -->"

GROUPS = [
    ("Российские мета-категории и госресурсы", {
        "category-ru-whitelist": "Согласованный набор RU-сервисов и зависимостей через include",
        "ru-whitelist-extended": "Дополнительные сервисы, включая Дом Лента, Иви, МТС, ретейл и госресурсы",
        "category-gov-ru": "Государственные, региональные и связанные социальные ресурсы",
        "category-ru": "Широкие RU-анкоры и доменные зоны; не точечный whitelist",
        "category-ru-all": "Мета-категория с широкими RU-правилами и сервисными include; не синоним whitelist",
    }),
    ("Крупные RU-сервисы", {
        "wildberries": "Wildberries, WB Pay/банк, Wibes и включённые CDN",
        "ozon": "Ozon и включённые сервисные/CDN-домены",
        "yandex": "Яндекс и включённые инфраструктурные зоны, в том числе общие CDN",
        "vk": "VK, пользовательский контент, видео и VK Pay",
        "mailru-group": "Mail.ru, почтовые и облачные домены, VK через include; отдельной mailru нет",
        "ok": "Одноклассники и включённые API/CDN",
        "avito": "Авито и включённые ресурсы",
        "x5": "X5, Пятёрочка, Перекрёсток, Чижик и сопутствующие сервисы",
        "dzen": "Дзен",
        "rutube": "Rutube и сопутствующие ресурсы",
        "okko": "Okko, API и сопутствующие ресурсы",
        "wink": "Wink и включённые видеодомены/CDN",
        "2gis": "2ГИС; satellite.online исключён",
    }),
    ("Финансы и платежи", {
        "ru-banks": "Банки и включённые банковские зависимости",
        "ru-payments": "Платёжные и идентификационные ресурсы, включая VK Pay",
        "ru-finance": "Финансовые/учётные ресурсы исходного набора",
    }),
    ("Ретейл, маркировка и повседневные сервисы", {
        "ru-retail-extra": "Лемана ПРО; другие сети распределены по остальным категориям",
        "ru-marking": "Честный знак и ЦРПТ",
        "ru-tv": "Телевидение и СМИ, включая pnp.ru и пакет C01",
        "ru-transport": "Транспорт и доставка; ICQ исключён",
        "ru-medical": "CGM и медицинские сервисы; не полный перечень API приложений",
    }),
    ("CDN и аналитика", {
        "ru-cdn": "CDN и сервисные зависимости; содержит общие и нероссийские зоны",
        "ru-analytics": "Метрика, AppMetrica, реклама и аналитические зависимости",
    }),
    ("Apple и инструменты разработки", {
        "apple": "Общая категория Apple",
        "apple-ads": "Рекламные ресурсы Apple",
        "apple-dev": "Разработка для экосистемы Apple",
        "apple-pki": "Сертификаты и PKI Apple",
        "apple-update": "Обновления Apple",
        "apple-tvplus": "Apple TV+",
        "icloud": "iCloud",
        "icloudprivaterelay": "iCloud Private Relay",
        "itunes": "iTunes и включённые медиаресурсы Apple",
        "beats": "Beats и связанные домены",
        "swift": "Язык программирования Swift экосистемы Apple, НЕ банковская сеть SWIFT",
        "fastlane": "Инструментарий fastlane",
    }),
    ("Google и инструменты разработки", {
        "google": "Общая категория Google с включёнными подкатегориями",
        "android": "Android",
        "google-play": "Google Play",
        "googlefcm": "Firebase Cloud Messaging и push-зависимости",
        "google-trust-services": "Сервисы доверия и сертификаты Google",
        "google-scholar": "Google Scholar",
        "google-deepmind": "Google DeepMind и включённые AI-ресурсы",
        "google-registry": "Доменные зоны и ресурсы Google Registry",
        "firebase": "Firebase",
        "flutter": "Flutter",
        "dart": "Dart",
        "golang": "Go",
        "v8": "Движок V8",
        "polymer": "Polymer",
        "opensourceinsights": "Open Source Insights / deps.dev",
        "kaggle": "Kaggle",
        "blogspot": "Региональные домены Blogspot",
    }),
    ("Видео и мессенджеры", {
        "youtube": "YouTube; указан в ProxySites DEFAULT",
        "telegram": "Telegram; указан в ProxySites DEFAULT",
        "twitch": "Сервисные домены Twitch; маршрут в готовые профили не добавлялся",
        "twitch-ads": "Сохранённый прежний рекламный/служебный набор; не включён в Twitch или whitelist",
    }),
    ("Служебные категории и список блокируемых ресурсов", {
        "private": "Локальные, служебные и зарезервированные доменные имена",
        "category-ban-ru": "Список блокируемых ресурсов; наличие категории не задаёт действие Block",
    }),
]

PREFERRED = {
    "category-ru-whitelist": "wildberries.ru domlenta.ru lenta.tech ivi.tv gosuslugi.ru",
    "ru-whitelist-extended": "domlenta.ru lenta.tech lenta.digift.ru ivi.tv mymts.ru",
    "category-gov-ru": "gov.ru gosuslugi.ru nalog.ru cbr.ru mos.ru",
    "category-ru": "ru su xn--p1ai moscow tatar",
    "category-ru-all": "ru su xn--p1ai wildberries.com yandex.com",
    "wildberries": "wildberries.ru wb.ru wbcontent.net wb-bank.ru wibes.com",
    "ozon": "ozon.ru ozone.ru ozonusercontent.com ozonbank.ru",
    "yandex": "yandex.ru ya.ru yastatic.net clstorage.net report.ap.yandex-net.ru",
    "vk": "vk.com vk.ru vkuserlive.com userapi.ru vkpay.ru",
    "mailru-group": "mail.ru bk.ru list.ru mcs.st bizmrg.com",
    "x5": "x5.ru 5ka.ru perekrestok.ru chizhik.ru abonementx5.ru",
    "ru-tv": "ren.tv russia.tv pnp.ru vedomosti.ru radioplayer.ru",
    "ru-banks": "sberbank.ru tbank.ru alfabank.ru vtb.ru t-static.ru",
    "ru-payments": "nspk.ru sbp.nspk.ru yoomoney.ru vkpay.ru payecom.ru",
    "ru-cdn": "ngenix.net cdnvideo.ru storage.googleapis.com cdnnow.ru dadata.ru",
    "ru-analytics": "appmetrica.yandex.ru mc.yandex.ru adfox.ru webvisor.com",
    "apple": "apple.com apple.com.cn apple.co",
    "icloud": "icloud.com icloud.com.cn",
    "google": "google.com googleapis.com gstatic.com",
    "google-play": "play.google.com android.clients.google.com",
    "youtube": "youtube.com youtu.be googlevideo.com ytimg.com",
    "telegram": "telegram.org t.me telegram.me telegra.ph",
    "twitch": "twitch.tv ttvnw.net jtvnw.net twitchcdn.net live-video.net",
}

IP_LABELS = {
    "ru": "RU-сети из frayZV/simple-ru-geoip; разрешена регулярная синхронизация ru.txt",
    "private": "Локальные и служебные IPv4/IPv6-сети",
    "ru-yandex": "Ручной набор Яндекс",
    "ru-ozon": "Ручной набор Ozon",
    "ru-analytics": "Ручной набор аналитики",
    "ru-banks": "Ручной банковский набор",
    "ru-wildberries": "Ручной набор Wildberries",
    "ru-payments": "Ручной платёжный набор",
    "ru-vk": "Ручной набор VK",
    "ru-mts": "Ручной набор МТС",
    "ru-cdn": "Ручной набор CDN",
    "ru-avito": "Ручной набор Авито",
}


def code(value):
    return "`" + value.replace("|", "&#124;").replace("`", "&#96;") + "`"


def examples(name, rules):
    chosen = []
    for value in PREFERRED.get(name, "").split():
        match = next((r for r in rules if r[1] == value), None)
        if match and match not in chosen:
            chosen.append(match)
    for rule in sorted(rules, key=lambda r: (r[0] not in ("domain", "full"), len(r[1]), r[1])):
        if rule not in chosen and len(chosen) < 5:
            chosen.append(rule)
    return ", ".join(code(value if kind == "domain" else f"{kind}:{value}")
                     for kind, value in chosen)


def render_tables():
    data = geosite_rules(ROOT / "geosite.dat")
    counts = entries(ROOT / "geosite.dat")
    lines = [
        "## Категории geosite", "",
        f"В текущей сборке **{len(data)} категории и {sum(map(len, counts.values()))} "
        "записей по всем категориям**. Счётчики взяты из бинарника после include "
        "и оптимизации; это не число уникальных сайтов, поскольку категории пересекаются.", "",
        "Название категории ведёт к полному исходному списку. В таблицах приведены "
        "примеры реально присутствующих правил: имя без префикса означает `domain:` "
        "(домен и поддомены), `full:` означает только точный хост; "
        "счётчики и SHA256 также доступны в [CATEGORY_STATS.md](./CATEGORY_STATS.md).", "",
    ]
    used = set()
    for heading, categories in GROUPS:
        lines += [f"### {heading}", "",
                  "| Категория / полный список | Правил в сборке | Домены и примеры правил | Покрытие |",
                  "|---|---:|---|---|"]
        for name, description in categories.items():
            assert name in data, f"README category missing from build: {name}"
            assert name not in used
            used.add(name)
            lines.append(
                f"| [{code(name)}](./data-geosite/{name}) | {len(counts[name])} | "
                f"{examples(name, data[name])} | {description} |")
        lines.append("")
    assert used == set(data), f"Add README descriptions for: {set(data) - used}"
    lines += [
        "`category-ban-ru` исторически стоит в DirectSites DEFAULT; это сохранённая "
        "настройка блока D, а не рекомендация блокировать или проксировать всю категорию. "
        "`twitch-ads` содержит также служебные правила и не является чистым рекламным фильтром.", "",
        "## Категории geoip", "",
    ]
    ipdata = entries(ROOT / "geoip.dat")
    lines += [
        f"В текущей сборке **{len(ipdata)} категорий и {sum(map(len, ipdata.values()))} CIDR**. "
        "Одна сеть может встречаться в нескольких категориях; полные списки доступны по названиям.", "",
        "| Категория / полный список | CIDR в сборке | IPv4 / IPv6 | Примеры сетей | Назначение |",
        "|---|---:|---:|---|---|",
    ]
    for name, messages in sorted(ipdata.items(), key=lambda x: (x[0] != "ru", x[0])):
        networks = []
        for message in messages:
            parts = dict(fields(message))
            networks.append(ipaddress.ip_network(
                (ipaddress.ip_address(parts[1]), parts.get(2, 0))))
        v4 = sum(n.version == 4 for n in networks)
        v6 = len(networks) - v4
        sample = ", ".join(code(str(n)) for n in networks[:3])
        lines.append(
            f"| [{code(name)}](./data-geoip/{name}.txt) | {len(messages)} | "
            f"{v4} / {v6} | {sample} | {IP_LABELS[name]} |")
    lines += [
        "", "Ручные наборы не означают полного покрытия ASN или исключительного "
        "использования каждой сети одним сервисом. В изменениях A–C GeoIP оставлен без изменений.", "",
        "## Прибитые IP: DnsHosts", "",
        "Таблица сформирована непосредственно из шести JSON-профилей Happ/Incy. "
        "Это сохранённые статические значения, а не свежая DNS-проверка; "
        "актуальность и исправления адресов относятся к отдельному блоку D.", "",
        "| Домен | IP в DnsHosts | Где задан |",
        "|---|---|---|",
    ]
    profiles = sorted(ROOT.glob("*/*.JSON"))
    pins = {}
    for path in profiles:
        for domain, address in json.loads(path.read_text()).get("DnsHosts", {}).items():
            if not isinstance(address, str):
                address = json.dumps(address, ensure_ascii=False)
            pins.setdefault((domain, address), []).append(str(path.relative_to(ROOT)))
    for (domain, address), owners in pins.items():
        where = f"Все {len(profiles)} профилей" if len(owners) == len(profiles) else ", ".join(owners)
        lines.append(f"| {code(domain)} | {code(address)} | {where} |")
    return "\n".join(lines) + "\n"


def updated_readme():
    current = (ROOT / "README.md").read_text()
    assert current.count(BEGIN) == current.count(END) == 1, "README table markers missing/duplicated"
    before, rest = current.split(BEGIN, 1)
    _, after = rest.split(END, 1)
    return before + BEGIN + "\n\n" + render_tables() + "\n" + END + after
