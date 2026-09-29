# ru-routing-dat

Собственные `geosite.dat` и `geoip.dat` для российского split tunneling. Исходники категорий и профили Happ/Incy хранятся вместе со сборками, чтобы изменения можно было проверить.

## Принцип отбора

Это курируемый набор правил маршрутизации, а не копия официального белого списка. Подтверждение Минцифры не является обязательным условием: учитываются принадлежность сервису, технические зависимости, проверяемые источники и согласованная политика проекта.

Включение домена не гарантирует доступность у любого оператора, отсутствие VPN-детектирования или полноту покрытия приложения. Общие CDN-зоны могут обслуживать сторонних клиентов; решение направлять их напрямую распространяется на соответствующие домены и поддомены, но не добавляет автоматически IP-диапазоны провайдера.

## Файлы и импорт

| Клиент | WHITELIST | DEFAULT | JSONSUB |
|---|---|---|---|
| Happ | [deeplink](https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/HAPP/WHITELIST.DEEPLINK) | [deeplink](https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/HAPP/DEFAULT.DEEPLINK) | [deeplink](https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/HAPP/JSONSUB.DEEPLINK) |
| Incy | [deeplink](https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/INCY/WHITELIST.DEEPLINK) | [deeplink](https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/INCY/DEFAULT.DEEPLINK) | [deeplink](https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/INCY/JSONSUB.DEEPLINK) |

Файл `.DEEPLINK` содержит URI для открытия в клиенте, а не обычную HTTP-подписку. QR-коды и исходные JSON находятся в [HAPP](./HAPP/) и [INCY](./INCY/); порядок импорта описан в [инструкции](./HAPP_INCY_USAGE.md).

Готовые базы:

```text
https://cdn.jsdelivr.net/gh/GrimbirdUsers/ru-routing-dat@main/geosite.dat
https://cdn.jsdelivr.net/gh/GrimbirdUsers/ru-routing-dat@main/geoip.dat
https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/geosite.dat
https://raw.githubusercontent.com/GrimbirdUsers/ru-routing-dat/main/geoip.dat
```

CDN и клиент могут кэшировать файлы. После обновления правил обновите базу в клиенте; после изменения самого профиля импортируйте обновлённый профиль.

## Профили и границы изменений

| Профиль | Содержимое |
|---|---|
| `WHITELIST` | Курируемые RU-категории и заданные RU/private IP направляются напрямую; остальное обрабатывается общей политикой профиля |
| `DEFAULT` | Дополнительно содержит Apple/iCloud и другие явные категории; YouTube, Google, Google Play, Telegram указаны в ProxySites |
| `JSONSUB` | Минимальный локальный набор private; настройки DNS, включая DnsHosts, также присутствуют |

Точные правила определяет JSON, а не эта краткая таблица. В DEFAULT сохранены исторические `category-ban-ru` в `DirectSites`, пересечения Direct/Proxy и `RouteOrder: block-proxy-direct`; исправления A–C от 30 сентября 2026 не меняют эту политику.

`DnsHosts` во всех профилях содержит фиксированные IP. Они оставлены без изменений и не должны считаться свежими DNS-ответами или гарантированно рабочими адресами; их ревизия относится к отдельному блоку D.

## Категории и статистика

Полные счётчики автоматически формируются из текущих бинарных файлов и исходников: [CATEGORY_STATS.md](./CATEGORY_STATS.md). Это количество правил, а не уникальных сайтов во всём проекте; категории пересекаются, а правило `domain:` покрывает поддомены.

| Категория | Назначение |
|---|---|
| `category-ru-whitelist` | Мета-категория курируемых RU-сервисов и зависимостей |
| `ru-whitelist-extended` | Дополнительные сервисы, госресурсы, ретейл и утверждённые зависимости |
| `wildberries`, `ozon` | Маркетплейсы и включённые в исходники инфраструктурные домены |
| `yandex`, `vk`, `mailru-group`, `ok` | Экосистемы и зависимые сервисы; отдельной категории `mailru` нет |
| `ru-banks`, `ru-payments`, `ru-finance` | Банки, платежи и финансовые сервисы |
| `ru-retail-extra` | Лемана ПРО: `lemanapro.ru`, `lmru.tech` |
| `ru-tv` | Телевидение и СМИ, включая добавления A07/C01 |
| `ru-transport` | Транспорт, доставка и включённые в исходник сервисы; ICQ исключён |
| `ru-medical` | Домены CGM/медицинских сервисов; не полный реестр API приложений |
| `ru-cdn`, `ru-analytics` | CDN и аналитические зависимости |
| `swift` | Язык программирования Swift экосистемы Apple, не банковская сеть SWIFT |
| `twitch` | Сервисные домены Twitch |
| `twitch-ads` | Отдельно сохранённые старые 11 рекламных/служебных правил, не чистый список рекламы |

`twitch-ads` не включён в `twitch` или RU-whitelist. Ни одна из этих двух категорий не добавлена в готовые профили этим обновлением.

## Сборка и проверки

Базы собираются из собственных исходников. Сравнивать их побайтно с чужими `.dat` для определения наличия обновлений некорректно: набор категорий отличается.

```sh
domain-list-community --datapath=./data-geosite --outputdir=. --outputname=geosite.dat
geoip -c geoip-config.json
python3 scripts/build_metadata.py
python3 scripts/validate_abc.py
```

Если меняются только домены, пересобирать `geoip.dat` не требуется. При изменении DEFAULT JSON синхронизируйте производные файлы:

```sh
python3 -m pip install qrcode Pillow zxing-cpp
python3 scripts/build_default_links.py
python3 scripts/validate_abc.py --qr
```

`build_metadata.py --check` проверяет актуальность документа со счётчиками без записи. `validate_abc.py` проверяет исходники и бинарник, существование категорий в профилях, точечные правила `full:`, согласованные наборы и равенство JSON/deeplink; `--qr` дополнительно декодирует DEFAULT QR.

## История и источники

Согласованные изменения перечислены в [журнале A–C от 2026-09-30](./changes/2026-09-30-abc.md). Источники доменных наборов и правила проверки отделены от операторских гарантий.

- **RU GeoIP**: [frayZV/simple-ru-geoip](https://github.com/frayZV/simple-ru-geoip), синхронизация исходного `ru.txt`.
- **Сервисные домены**: [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community), сайты сервисов и их инфраструктурные сведения.
- **Дополнительные кандидаты**: [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist); запись в стороннем списке сама по себе не доказывает доступность у всех операторов.

Автор проекта: [GrimbirdUsers](https://github.com/GrimbirdUsers). Для предложения изменений откройте [Issue](https://github.com/GrimbirdUsers/ru-routing-dat/issues) с доменом, сценарием сбоя и техническим обоснованием; ссылка на официальное подтверждение не обязательна.
