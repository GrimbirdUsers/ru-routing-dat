# ru-routing-dat

Собственные `geosite.dat` и `geoip.dat` для российского split-tunneling'а в **Happ**, **Incy**, **Xray**, **v2ray**, **sing-box**, **Mihomo** (Clash Meta).

Проект строится по принципу **строгого соответствия белому списку Минцифры** — только официально одобренные домены и IP-подсети, без «серых» расширений.

---

## Быстрый старт

### Happ (iOS) / Incy (Android)

Импортируйте профиль одним кликом:

| Клиент | WHITELIST | DEFAULT | JSONSUB |
|---|---|---|---|
| **Happ** | [import](https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/HAPP/WHITELIST.DEEPLINK) | [import](https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/HAPP/DEFAULT.DEEPLINK) | [import](https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/HAPP/JSONSUB.DEEPLINK) |
| **Incy** | [import](https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/INCY/WHITELIST.DEEPLINK) | [import](https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/INCY/DEFAULT.DEEPLINK) | [import](https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/INCY/JSONSUB.DEEPLINK) |

QR-коды для сканирования: смотрите папки [`HAPP/`](./HAPP/) и [`INCY/`](./INCY/).

Подробная документация профилей — [HAPP_INCY_USAGE.md](./HAPP_INCY_USAGE.md).

### Xray / v2ray / sing-box

Скачайте `.dat` файлы через CDN (jsDelivr — быстро, кэш) или напрямую с GitHub:

**jsDelivr CDN (рекомендуется):**
```
https://cdn.jsdelivr.net/gh/GrimbirdUsers/ru-routing-dat@main/geosite.dat
https://cdn.jsdelivr.net/gh/GrimbirdUsers/ru-routing-dat@main/geoip.dat
```

**Прямо с GitHub:**
```
https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/geosite.dat
https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/geoip.dat
```

---

## Три готовых профиля

| Профиль | Direct (напрямую, без VPN) | Proxy (через VPN) | Для кого |
|---|---|---|---|
| **WHITELIST** | Только белый список Минцифры + СБП + госорганы + ретейл + RU IP-подсети | Всё остальное | Максимальная приватность, для тех кто использует VPN 24/7 |
| **DEFAULT** | Всё из WHITELIST + Yandex, VK, Mail.ru, OK, Dzen, Rutube, 2GIS, Avito, X5, Okko, Wink + Apple, iCloud | YouTube, Google, Google Play, Telegram | Универсальный вариант, оптимальный баланс |
| **JSONSUB** | Только private (локальная сеть) | Всё остальное | Минимальный шаблон для подписок XrayCore JSON / Remnawave |

---

## Категории geosite (63 категории, ~11 000 доменов)

### Российский белый список Минцифры

| Категория | Доменов | Что покрывает |
|---|---|---|
| `category-ru-whitelist` | **513** | **Мета-категория: включает все whitelist-подкатегории** |
| `ru-whitelist-extended` | 146 | Основной whitelist от Минцифры (расширенный) |
| `category-gov-ru` | 119 | gosuslugi.ru, nalog.ru, cbr.ru, mos.ru, региональные gov |
| `category-ru` | 112 | Общие RU-анкоры (.ru/.su/.рф/.moscow) |

### Крупные RU-сервисы

| Категория | Доменов | Сервисы |
|---|---|---|
| `yandex` | 56 | Все домены Яндекса (ya.ru, turbopages, adfox, webvisor) |
| `mailru-group` | 46 | Mail.ru + OK.ru + Dzen.ru + VK-стек |
| `ozon` | 31 | Ozon.ru + все CDN (ozone.ru, ozonusercontent.com) |
| `vk` | 36 | VK.com/ru/me, userapi, vkcache, vk-cdn |
| `x5` | 33 | Перекрёсток, Пятёрочка, Чижик, 5post |
| `wildberries` | 11 | wildberries.ru, wb.ru, wbstatic.net, bx-cdn.ru |
| `mailru`, `avito`, `dzen`, `rutube`, `okko`, `wink`, `ok`, `2gis` | 2–3 | Медиа и сервисы |

### Финансы и платежи

| Категория | Доменов | Покрытие |
|---|---|---|
| `ru-banks` | 31 | Сбер, Т-Банк (Тинькофф), Альфа, ВТБ, Газпромбанк, Райффайзен и др. |
| `ru-payments` | 36 | СБП, MirPay, ЮMoney, QIWI, национальная платёжная инфра |
| `ru-analytics` | 45 | Метрика, VK-аналитика, AdFox, admetrica |
| `ru-cdn` | 16 | VK Cloud, Selectel, Yandex Cloud (российские CDN) |
| `ru-finance` | 2 | moex.com, honestmark.org |
| `ru-marking` | 2 | Честный знак (crpt.ru, mdlp.crpt.ru) |
| `swift` | 4 | SWIFT-инфра |

### Ретейл и повседневность

| Категория | Доменов | Что |
|---|---|---|
| `ru-retail-extra` | 2 | Ашан, Азбука Вкуса, Чижик, Магнит (расширение сверх Минцифры) |
| `ru-tv` | 7 | ren.tv, russia.tv, vgtrk, more.tv, premier.one, vitrina.tv |
| `ru-transport` | 5 | pobeda.aero, routeq, youdrive, icq |
| `ru-medical` | 8 | Medtrum, Sinocare, POCTech, iCan, Yuwell (CGM/глюкометры) |

### Западные экосистемы (для DEFAULT-профиля)

| Категория | Доменов | Назначение |
|---|---|---|
| `apple` | 1583 | Apple основные |
| `icloud` | 54 | iCloud сервисы |
| `google` | 105 | Google core |
| `youtube` | 177 | YouTube (в DEFAULT — через прокси) |
| `google-play` | 8 | Play Store |
| `telegram` | 21 | Telegram (в DEFAULT — через прокси) |
| `twitch` | 11 | Twitch |
| `google-deepmind`, `google-registry`, `firebase`, `flutter`, `dart`, `golang`, `v8` и др. | 8 подкат. | Google dev-стек |
| `apple-dev`, `apple-pki`, `apple-update`, `beats` и др. | 7 подкат. | Apple вспомогательные |

### Блэклист

| Категория | Записей | Что |
|---|---|---|
| `category-ban-ru` | 7029 | Блокируемый в РФ контент (antifilter/refilter) |

---

## Категории geoip (11 категорий, ~25 000 CIDR)

| Категория | CIDR | Источник |
|---|---|---|
| `ru` | **24935** | Все российские IP-подсети (обновляется еженедельно из frayZV/simple-ru-geoip) |
| `ru-yandex` | 16 | Яндекс ASN |
| `ru-ozon` | 15 | Ozon ASN |
| `ru-analytics` | 11 | Аналитика (Метрика и др.) |
| `ru-banks` | 11 | Российские банки |
| `ru-wildberries` | 9 | Wildberries ASN |
| `ru-payments` | 7 | Платёжные системы |
| `ru-vk` | 5 | VK ASN |
| `ru-mts` | 3 | МТС |
| `ru-cdn` | 2 | Российские CDN |
| `private` | 18 | Локальные сети (RFC 1918) |

---

## Прибитые IP (DnsHosts) в профилях

Для обхода DNS-блокировок и залипаний в профили вшиты прямые IP критичных гос-сервисов:

| Домен | IP |
|---|---|
| `lkfl2.nalog.ru` | `213.24.64.175` |
| `lknpd.nalog.ru` | `213.24.64.181` |
| `service.nalog.ru` | `213.24.64.140` |
| `nalog.gov.ru` | `37.220.164.100` |
| `gosuslugi.ru` | `213.59.253.7` |
| `esia.gosuslugi.ru` | `213.59.253.8` |
| `lk.gosuslugi.ru` | `213.59.253.6` |
| `sberbank.ru` | `84.252.149.206` |
| `online.sberbank.ru` | `84.252.149.51` |
| `vtb.ru` | `195.242.82.13` |
| `online.vtb.ru` | `185.179.146.43` |
| `id.vtb.ru` | `185.179.144.34` |

IP проверены через Cloudflare DoH и Google DoH — консистентные ответы.

---

## Обновления

- **geoip.dat**: еженедельно (по воскресеньям 03:00 MSK) — cron синхронизирует `data-geoip/ru.txt` с апстримом [frayZV/simple-ru-geoip](https://github.com/frayZV/simple-ru-geoip)
- **geosite.dat**: пересобирается при добавлении новых Минцифры-подтверждённых доменов
- **Профили Happ/Incy**: обновляются при изменениях категорий (обычно 1 раз в неделю)

Проверить последний релиз: [Releases](https://github.com/GrimbirdUsers/ru-routing-dat/releases)

---

## Использование в конфигах

### Xray / v2ray (routing.rules)

```json
{
  "type": "field",
  "domain": ["geosite:category-ru-whitelist"],
  "outboundTag": "direct"
}
```

```json
{
  "type": "field",
  "ip": ["geoip:ru"],
  "outboundTag": "direct"
}
```

### sing-box (route.rules)

```json
{
  "geosite": "category-ru-whitelist",
  "outbound": "direct"
}
```

### Mihomo (Clash Meta)

```yaml
rules:
  - GEOSITE,category-ru-whitelist,DIRECT
  - GEOIP,ru,DIRECT
```

---

## Структура репозитория

```
├── geosite.dat             # Скомпилированный geosite (~260 KB)
├── geoip.dat               # Скомпилированный geoip (~400 KB)
├── data-geosite/           # Исходники: 63 файла с доменами
├── data-geoip/             # Исходники: 11 файлов с CIDR
├── HAPP/                   # Профили для Happ (iOS): JSON + DEEPLINK + QR
├── INCY/                   # Профили для Incy (Android): JSON + DEEPLINK + QR
├── geoip-config.json       # Конфиг сборки geoip
├── HAPP_INCY_USAGE.md      # Детальная инструкция по профилям
└── README.md               # Этот файл
```

---

## Философия проекта

**Только Минцифры-подтверждённые домены.** Никаких «серых» расширений типа сторонних новостных сайтов, форумов, региональных gov-доменов без явного включения в белый список. Это гарантирует что VPN-детектор Wildberries, Ozon, банков не даст ложных срабатываний.

**Гранулярные категории.** Вместо одного `whitelist` — 63 категории geosite и 11 geoip. Можно точечно управлять маршрутизацией: направить Ozon direct, а YouTube через прокси; Wildberries direct, а Google через прокси.

**Полное покрытие ретейла и СМИ РФ.** Ашан, Азбука Вкуса, Чижик, Delimobil, Belkacar, Достависта, 1tv, dumatv — то что часто пропускают в универсальных списках.

---

## Сравнение с аналогами

| | ru-routing-dat | v2fly/domain-list-community | hydraponique/roscomvpn-geosite |
|---|---|---|---|
| Философия | Только Минцифры | Общий | Расширенный (много «серых» доменов) |
| Категорий geosite | 63 | ~500 | ~25 |
| Категорий geoip | 11 | 200+ | 3 |
| Обновление ru.txt | Еженедельно (cron) | Периодически | Ежедневно |
| Профили Happ/Incy | ✅ 6 готовых | ❌ | ✅ (общие) |
| DnsHosts | ✅ 12 записей | ❌ | ✅ 2 записи |
| Гранулярность RU-сервисов | Высокая (по сервисам) | Средняя | Низкая (один whitelist) |

---

## Источники

- Основа RU IP: [frayZV/simple-ru-geoip](https://github.com/frayZV/simple-ru-geoip) (заморожен frayZV/simple-ru-geosite — не используется)
- Дополнительные проверки: [hydraponique/roscomvpn-geosite](https://github.com/hydraponique/roscomvpn-geosite), [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist)
- Официальный список: [Приказ Минцифры России](https://digital.gov.ru/) о белом списке ресурсов
- Категория `category-ban-ru`: [antifilter.download](https://antifilter.download/)

---

## Лицензия и авторство

Собирается автоматически, свободно к использованию. Домены и IP взяты из открытых источников. Автор: [GrimbirdUsers](https://github.com/GrimbirdUsers).

Обнаружили ошибку или хотите добавить домен? Откройте [Issue](https://github.com/GrimbirdUsers/ru-routing-dat/issues) с обоснованием и ссылкой на Минцифры-подтверждение.
