# Профили для Happ и Incy

Три готовых профиля для двух клиентов: **Happ** (iOS) и **Incy** (Android).

## Быстрый импорт (deeplink)

Нажмите на клиенте один из ссылок ниже — профиль импортируется автоматически.

### Happ (iOS)
- **WHITELIST** (строгий белый список Минцифры): `HAPP/WHITELIST.DEEPLINK`
- **DEFAULT** (расширенный, YouTube/Telegram через прокси): `HAPP/DEFAULT.DEEPLINK`
- **JSONSUB** (минимальный шаблон без правил): `HAPP/JSONSUB.DEEPLINK`

### Incy (Android)
- **WHITELIST**: `INCY/WHITELIST.DEEPLINK`
- **DEFAULT**: `INCY/DEFAULT.DEEPLINK`
- **JSONSUB**: `INCY/JSONSUB.DEEPLINK`

## Быстрый импорт (QR-код)

Файлы `*.QR.png` содержат QR-код с deeplink. Отсканируйте камерой — клиент откроется автоматически.

## Прямые ссылки (raw content)

Если хотите использовать через подписку, вот прямые ссылки:

Happ WHITELIST:
```
https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/HAPP/WHITELIST.DEEPLINK
```

Аналогично для остальных профилей — замените имя файла.

## В чём разница профилей

| Профиль | Direct (без прокси) | Proxy (через VPN) |
|---------|--------------------|--------------------|
| WHITELIST | Только домены из белого списка Минцифры + RU IP | Всё остальное |
| DEFAULT | Все RU-категории + Apple/iCloud | YouTube, Google, Telegram |
| JSONSUB | Только private (LAN) | Всё остальное |

## Что содержат наши категории

- **ru-whitelist-extended** — основной белый список Минцифры (~1500 доменов)
- **ru-retail-extra** — сети (Ашан, Азбука Вкуса, Чижик, Магнит)
- **ru-marking** — Честный знак (crpt.ru, mdlp.crpt.ru)
- **ozon** / **wildberries** — маркетплейсы (со всеми CDN)
- **ru-banks** / **ru-payments** / **ru-finance** — банки, СБП, MirPay
- **ru-cdn** — российские CDN (VK Cloud, Selectel, Yandex Cloud)
- **ru-tv** — 1tv.ru, Первый канал, вещатели
- **ru-transport** — РЖД, Аэрофлот, Яндекс.Такси
- **ru-medical** — Госуслуги здоровья, ЕМИАС
- **ru-analytics** — Метрика, VK-аналитика, AdFox
- **category-gov-ru** — все .gov.ru
- **yandex** / **mailru** / **vk** / **ok** / **dzen** / **rutube** — крупные сервисы

## DnsHosts (прибитые IP)

В каждый профиль вшиты прибитые IP для критичных гос-сервисов (обход DNS-блокировок):

- `lkfl2.nalog.ru` → `213.24.64.175`
- `lknpd.nalog.ru` → `213.24.64.181`
- `service.nalog.ru` → `213.24.64.140`
- `nalog.gov.ru` → `37.220.164.100`
- `gosuslugi.ru` → `213.59.253.7`
- `esia.gosuslugi.ru` → `213.59.253.8`
- `lk.gosuslugi.ru` → `213.59.253.6`
- `online.sberbank.ru` → `84.252.149.51`
- `sberbank.ru` → `84.252.149.206`
- `vtb.ru` → `195.242.82.13`
- `online.vtb.ru` → `185.179.146.43`
- `id.vtb.ru` → `185.179.144.34`

Обновляются вместе с профилями.
