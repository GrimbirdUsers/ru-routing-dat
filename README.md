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

| Профиль | Direct: без прокси | Proxy и прочие настройки |
|---|---|---|
| [`WHITELIST`](./HAPP/WHITELIST.JSON) | Курируемые RU-категории, госресурсы, ретейл и заданные RU/private IP | Остальное обрабатывается общей политикой профиля; DnsHosts также заданы |
| [`DEFAULT`](./HAPP/DEFAULT.JSON) | RU-категории, Apple/iCloud и другие явно заданные категории; историческая `category-ban-ru` сохранена | YouTube, Google, Google Play, Telegram указаны в ProxySites; порядок `block-proxy-direct` сохранён |
| [`JSONSUB`](./HAPP/JSONSUB.JSON) | Минимальный локальный набор private | Остальное обрабатывается общей политикой профиля; это не пустой шаблон, DNS и DnsHosts присутствуют |

Точные правила определяет JSON, а не эта краткая таблица. В DEFAULT сохранены исторические `category-ban-ru` в `DirectSites`, пересечения Direct/Proxy и `RouteOrder: block-proxy-direct`; исправления A–C от 30 сентября 2026 не меняют эту политику.

`DnsHosts` во всех профилях содержит фиксированные IP. Они оставлены без изменений и не должны считаться свежими DNS-ответами или гарантированно рабочими адресами; их ревизия относится к отдельному блоку D.

<!-- BEGIN GENERATED ROUTING TABLES -->

## Категории geosite

В текущей сборке **63 категории и 12762 записей по всем категориям**. Счётчики взяты из бинарника после include и оптимизации; это не число уникальных сайтов, поскольку категории пересекаются.

Название категории ведёт к полному исходному списку. В таблицах приведены примеры реально присутствующих правил: имя без префикса означает `domain:` (домен и поддомены), `full:` означает только точный хост; счётчики и SHA256 также доступны в [CATEGORY_STATS.md](./CATEGORY_STATS.md).

### Российские мета-категории и госресурсы

| Категория / полный список | Правил в сборке | Домены и примеры правил | Покрытие |
|---|---:|---|---|
| [`category-ru-whitelist`](./data-geosite/category-ru-whitelist) | 629 | `wildberries.ru`, `domlenta.ru`, `lenta.tech`, `ivi.tv`, `gosuslugi.ru` | Согласованный набор RU-сервисов и зависимостей через include |
| [`ru-whitelist-extended`](./data-geosite/ru-whitelist-extended) | 167 | `domlenta.ru`, `lenta.tech`, `full:lenta.digift.ru`, `ivi.tv`, `mymts.ru` | Дополнительные сервисы, включая Дом Лента, Иви, МТС, ретейл и госресурсы |
| [`category-gov-ru`](./data-geosite/category-gov-ru) | 119 | `gov.ru`, `gosuslugi.ru`, `nalog.ru`, `cbr.ru`, `mos.ru` | Государственные, региональные и связанные социальные ресурсы |
| [`category-ru`](./data-geosite/category-ru) | 111 | `ru`, `su`, `xn--p1ai`, `moscow`, `tatar` | Широкие RU-анкоры и доменные зоны; не точечный whitelist |
| [`category-ru-all`](./data-geosite/category-ru-all) | 167 | `ru`, `su`, `xn--p1ai`, `yandex.com`, `psk` | Мета-категория с широкими RU-правилами и сервисными include; не синоним whitelist |

### Крупные RU-сервисы

| Категория / полный список | Правил в сборке | Домены и примеры правил | Покрытие |
|---|---:|---|---|
| [`wildberries`](./data-geosite/wildberries) | 16 | `wildberries.ru`, `wb.ru`, `wbcontent.net`, `wb-bank.ru`, `wibes.com` | Wildberries, WB Pay/банк, Wibes и включённые CDN |
| [`ozon`](./data-geosite/ozon) | 31 | `ozon.ru`, `ozone.ru`, `ozonusercontent.com`, `ozonbank.ru`, `o3.ru` | Ozon и включённые сервисные/CDN-домены |
| [`yandex`](./data-geosite/yandex) | 62 | `yandex.ru`, `ya.ru`, `yastatic.net`, `clstorage.net`, `full:report.ap.yandex-net.ru` | Яндекс и включённые инфраструктурные зоны, в том числе общие CDN |
| [`vk`](./data-geosite/vk) | 46 | `vk.com`, `vk.ru`, `vkuserlive.com`, `userapi.ru`, `vkpay.ru` | VK, пользовательский контент, видео и VK Pay |
| [`mailru-group`](./data-geosite/mailru-group) | 70 | `mail.ru`, `bk.ru`, `list.ru`, `mcs.st`, `bizmrg.com` | Mail.ru, почтовые и облачные домены, VK через include; отдельной mailru нет |
| [`ok`](./data-geosite/ok) | 9 | `ok.me`, `ok.ru`, `odkl.ru`, `apiok.ru`, `mycdn.me` | Одноклассники и включённые API/CDN |
| [`avito`](./data-geosite/avito) | 6 | `avito.ru`, `avito.st`, `avito.tech`, `autoteka.ru`, `domofond.ru` | Авито и включённые ресурсы |
| [`x5`](./data-geosite/x5) | 35 | `x5.ru`, `5ka.ru`, `perekrestok.ru`, `chizhik.ru`, `abonementx5.ru` | X5, Пятёрочка, Перекрёсток, Чижик и сопутствующие сервисы |
| [`dzen`](./data-geosite/dzen) | 2 | `dzen.ru`, `dzeninfra.ru` | Дзен |
| [`rutube`](./data-geosite/rutube) | 4 | `rtbcdn.ru`, `rutube.ru`, `rutube.sport`, `rutubelist.ru` | Rutube и сопутствующие ресурсы |
| [`okko`](./data-geosite/okko) | 7 | `okko.ru`, `okko.tv`, `okko.sport`, `okkoapi.tv`, `yotaplay.ru` | Okko, API и сопутствующие ресурсы |
| [`wink`](./data-geosite/wink) | 4 | `wink.ru`, `ngenix.net`, `restream.ru`, `restream-media.net` | Wink и включённые видеодомены/CDN |
| [`2gis`](./data-geosite/2gis) | 3 | `2gis.ru`, `2gis.com`, `2gis.tech` | 2ГИС; satellite.online исключён |

### Финансы и платежи

| Категория / полный список | Правил в сборке | Домены и примеры правил | Покрытие |
|---|---:|---|---|
| [`ru-banks`](./data-geosite/ru-banks) | 36 | `sberbank.ru`, `tbank.ru`, `alfabank.ru`, `vtb.ru`, `t-static.ru` | Банки и включённые банковские зависимости |
| [`ru-payments`](./data-geosite/ru-payments) | 26 | `nspk.ru`, `vkpay.ru`, `payecom.ru`, `sber.ru`, `vkpay.io` | Платёжные и идентификационные ресурсы, включая VK Pay |
| [`ru-finance`](./data-geosite/ru-finance) | 2 | `moex.com`, `honestmark.org` | Финансовые/учётные ресурсы исходного набора |

### Ретейл, маркировка и повседневные сервисы

| Категория / полный список | Правил в сборке | Домены и примеры правил | Покрытие |
|---|---:|---|---|
| [`ru-retail-extra`](./data-geosite/ru-retail-extra) | 2 | `lmru.tech`, `lemanapro.ru` | Лемана ПРО; другие сети распределены по остальным категориям |
| [`ru-marking`](./data-geosite/ru-marking) | 2 | `crpt.ru`, `xn--80ajghhoc2aj1c8b.xn--p1ai` | Честный знак и ЦРПТ |
| [`ru-tv`](./data-geosite/ru-tv) | 22 | `ren.tv`, `russia.tv`, `pnp.ru`, `vedomosti.ru`, `radioplayer.ru` | Телевидение и СМИ, включая pnp.ru и пакет C01 |
| [`ru-transport`](./data-geosite/ru-transport) | 6 | `s7.ru`, `routeq.com`, `aeroflot.ru`, `pobeda.aero`, `topdelivery.ru` | Транспорт и доставка; ICQ исключён |
| [`ru-medical`](./data-geosite/ru-medical) | 9 | `mqcgm.com`, `yuwell.com`, `icancgm.com`, `medtrum.com`, `poctech.com` | CGM и медицинские сервисы; не полный перечень API приложений |

### CDN и аналитика

| Категория / полный список | Правил в сборке | Домены и примеры правил | Покрытие |
|---|---:|---|---|
| [`ru-cdn`](./data-geosite/ru-cdn) | 15 | `ngenix.net`, `cdnvideo.ru`, `storage.googleapis.com`, `cdnnow.ru`, `dadata.ru` | CDN и сервисные зависимости; содержит общие и нероссийские зоны |
| [`ru-analytics`](./data-geosite/ru-analytics) | 38 | `appmetrica.yandex.ru`, `mc.yandex.ru`, `adfox.ru`, `webvisor.com`, `mindbox.ru` | Метрика, AppMetrica, реклама и аналитические зависимости |

### Apple и инструменты разработки

| Категория / полный список | Правил в сборке | Домены и примеры правил | Покрытие |
|---|---:|---|---|
| [`apple`](./data-geosite/apple) | 1583 | `apple.com`, `apple.com.cn`, `apple.co`, `apple`, `mac.eu` | Общая категория Apple |
| [`apple-ads`](./data-geosite/apple-ads) | 4 | `qwapi.com`, `iad.apple.com`, `iadsdk.apple.com`, `api-adservices.apple.com` | Рекламные ресурсы Apple |
| [`apple-dev`](./data-geosite/apple-dev) | 37 | `cups.org`, `swift.org`, `swiftui.cn`, `webkit.org`, `carekit.org` | Разработка для экосистемы Apple |
| [`apple-pki`](./data-geosite/apple-pki) | 9 | `full:crl.apple.com`, `full:ocsp.apple.com`, `full:certs.apple.com`, `full:ocsp2.apple.com`, `full:valid.apple.com` | Сертификаты и PKI Apple |
| [`apple-update`](./data-geosite/apple-update) | 21 | `gg.apple.com`, `gs.apple.com`, `ig.apple.com`, `xp.apple.com`, `skl.apple.com` | Обновления Apple |
| [`apple-tvplus`](./data-geosite/apple-tvplus) | 8 | `tv.apple.com`, `full:tv.applemusic.com`, `full:hls.itunes.apple.com`, `full:hls-amt.itunes.apple.com`, `full:np-edge.itunes.apple.com` | Apple TV+ |
| [`icloud`](./data-geosite/icloud) | 51 | `icloud.com`, `icloud.com.cn`, `me.com`, `icloud.ch`, `icloud.de` | iCloud |
| [`icloudprivaterelay`](./data-geosite/icloudprivaterelay) | 3 | `mask.icloud.com`, `mask-h2.icloud.com`, `mask-api.icloud.com` | iCloud Private Relay |
| [`itunes`](./data-geosite/itunes) | 52 | `itun.es`, `itunes.ca`, `itunes.co`, `itunes.hk`, `itunes.mx` | iTunes и включённые медиаресурсы Apple |
| [`beats`](./data-geosite/beats) | 716 | `ubnw.net`, `beats1.cc`, `beats1.cn`, `beats1.tv`, `beats4.cn` | Beats и связанные домены |
| [`swift`](./data-geosite/swift) | 4 | `swift.org`, `swiftui.cn`, `appleswift.com`, `swiftui.com.cn` | Язык программирования Swift экосистемы Apple, НЕ банковская сеть SWIFT |
| [`fastlane`](./data-geosite/fastlane) | 2 | `fastlane.ci`, `fastlane.tools` | Инструментарий fastlane |

### Google и инструменты разработки

| Категория / полный список | Правил в сборке | Домены и примеры правил | Покрытие |
|---|---:|---|---|
| [`google`](./data-geosite/google) | 933 | `google.com`, `googleapis.com`, `gstatic.com`, `gle`, `goo` | Общая категория Google с включёнными подкатегориями |
| [`android`](./data-geosite/android) | 4 | `android`, `android.com`, `androidify.com`, `full:android.googlesource.com` | Android |
| [`google-play`](./data-geosite/google-play) | 9 | `play.google.com`, `googleplay.com`, `play.googleapis.com`, `xn--ngstr-lra8j.com`, `play-fe.googleapis.com` | Google Play |
| [`googlefcm`](./data-geosite/googlefcm) | 12 | `full:mtalk.google.com`, `full:mtalk4.google.com`, `full:mtalk-dev.google.com`, `full:alt1-mtalk.google.com`, `full:alt2-mtalk.google.com` | Firebase Cloud Messaging и push-зависимости |
| [`google-trust-services`](./data-geosite/google-trust-services) | 12 | `pki.goog`, `full:c.pki.goog`, `full:i.pki.goog`, `full:o.pki.goog`, `full:crl.pki.goog` | Сервисы доверия и сертификаты Google |
| [`google-scholar`](./data-geosite/google-scholar) | 76 | `full:scholar.google.ae`, `full:scholar.google.at`, `full:scholar.google.be`, `full:scholar.google.bg`, `full:scholar.google.ca` | Google Scholar |
| [`google-deepmind`](./data-geosite/google-deepmind) | 39 | `ai.studio`, `labs.google`, `opal.google`, `deepmind.com`, `jules.google` | Google DeepMind и включённые AI-ресурсы |
| [`google-registry`](./data-geosite/google-registry) | 13 | `crr.com`, `get.app`, `get.dev`, `get.how`, `get.new` | Доменные зоны и ресурсы Google Registry |
| [`firebase`](./data-geosite/firebase) | 20 | `firebase.io`, `firebase.com`, `firebaseio.com`, `crashlytics.com`, `firebaseapp.com` | Firebase |
| [`flutter`](./data-geosite/flutter) | 3 | `pub.dev`, `flutter.dev`, `flutterapp.com` | Flutter |
| [`dart`](./data-geosite/dart) | 3 | `dart.dev`, `dartpad.dev`, `dartlang.org` | Dart |
| [`golang`](./data-geosite/golang) | 8 | `go.dev`, `godoc.org`, `golang.com`, `golang.net`, `golang.org` | Go |
| [`v8`](./data-geosite/v8) | 2 | `v8.dev`, `v8project.org` | Движок V8 |
| [`polymer`](./data-geosite/polymer) | 2 | `polymerproject.org`, `polymer-project.org` | Polymer |
| [`opensourceinsights`](./data-geosite/opensourceinsights) | 4 | `deps.dev`, `deps.info`, `opensourceinsight.dev`, `opensourceinsights.dev` | Open Source Insights / deps.dev |
| [`kaggle`](./data-geosite/kaggle) | 4 | `kaggle.io`, `kaggle.com`, `kaggle.net`, `kaggleusercontent.com` | Kaggle |
| [`blogspot`](./data-geosite/blogspot) | 76 | `blogger.com`, `blogspot.ae`, `blogspot.al`, `blogspot.am`, `blogspot.ba` | Региональные домены Blogspot |

### Видео и мессенджеры

| Категория / полный список | Правил в сборке | Домены и примеры правил | Покрытие |
|---|---:|---|---|
| [`youtube`](./data-geosite/youtube) | 179 | `youtube.com`, `youtu.be`, `googlevideo.com`, `ytimg.com`, `yt.be` | YouTube; указан в ProxySites DEFAULT |
| [`telegram`](./data-geosite/telegram) | 21 | `telegram.org`, `t.me`, `telegram.me`, `telegra.ph`, `tx.me` | Telegram; указан в ProxySites DEFAULT |
| [`twitch`](./data-geosite/twitch) | 34 | `twitch.tv`, `ttvnw.net`, `jtvnw.net`, `twitchcdn.net`, `live-video.net` | Сервисные домены Twitch; маршрут в готовые профили не добавлялся |
| [`twitch-ads`](./data-geosite/twitch-ads) | 11 | `kouch.tv`, `full:ads.twitch.tv`, `full:auth.brandis.us`, `doubleclick.net`, `full:spade.twitch.tv` | Сохранённый прежний рекламный/служебный набор; не включён в Twitch или whitelist |

### Служебные категории и список блокируемых ресурсов

| Категория / полный список | Правил в сборке | Домены и примеры правил | Покрытие |
|---|---:|---|---|
| [`private`](./data-geosite/private) | 132 | `lan`, `test`, `local`, `ts.net`, `example` | Локальные, служебные и зарезервированные доменные имена |
| [`category-ban-ru`](./data-geosite/category-ban-ru) | 7029 | `ej.ru`, `og.ru`, `689.ru`, `7ik.ru`, `coe.ru` | Список блокируемых ресурсов; наличие категории не задаёт действие Block |

`category-ban-ru` исторически стоит в DirectSites DEFAULT; это сохранённая настройка блока D, а не рекомендация блокировать или проксировать всю категорию. `twitch-ads` содержит также служебные правила и не является чистым рекламным фильтром.

## Категории geoip

В текущей сборке **12 категорий и 25192 CIDR**. Одна сеть может встречаться в нескольких категориях; полные списки доступны по названиям.

| Категория / полный список | CIDR в сборке | IPv4 / IPv6 | Примеры сетей | Назначение |
|---|---:|---:|---|---|
| [`ru`](./data-geoip/ru.txt) | 25093 | 12943 / 12150 | `2.16.20.0/23`, `2.16.53.0/24`, `2.16.103.0/24` | RU-сети из frayZV/simple-ru-geoip; разрешена регулярная синхронизация ru.txt |
| [`private`](./data-geoip/private.txt) | 18 | 14 / 4 | `0.0.0.0/8`, `10.0.0.0/8`, `100.64.0.0/10` | Локальные и служебные IPv4/IPv6-сети |
| [`ru-analytics`](./data-geoip/ru-analytics.txt) | 11 | 11 / 0 | `84.252.128.0/20`, `88.212.201.0/24`, `89.221.236.0/22` | Ручной набор аналитики |
| [`ru-avito`](./data-geoip/ru-avito.txt) | 3 | 3 / 0 | `176.114.120.0/21`, `185.89.12.0/24`, `185.89.14.0/23` | Ручной набор Авито |
| [`ru-banks`](./data-geoip/ru-banks.txt) | 11 | 11 / 0 | `91.194.224.0/22`, `91.215.88.0/22`, `193.0.68.0/23` | Ручной банковский набор |
| [`ru-cdn`](./data-geoip/ru-cdn.txt) | 2 | 2 / 0 | `84.201.128.0/18`, `212.193.155.0/24` | Ручной набор CDN |
| [`ru-mts`](./data-geoip/ru-mts.txt) | 3 | 3 / 0 | `83.149.0.0/17`, `195.34.0.0/17`, `213.87.0.0/17` | Ручной набор МТС |
| [`ru-ozon`](./data-geoip/ru-ozon.txt) | 15 | 15 / 0 | `5.45.64.0/21`, `31.31.205.0/24`, `31.130.140.0/22` | Ручной набор Ozon |
| [`ru-payments`](./data-geoip/ru-payments.txt) | 7 | 7 / 0 | `62.76.205.0/24`, `84.252.149.0/24`, `151.236.81.0/24` | Ручной платёжный набор |
| [`ru-vk`](./data-geoip/ru-vk.txt) | 5 | 5 / 0 | `87.240.128.0/18`, `91.207.4.0/22`, `93.186.224.0/20` | Ручной набор VK |
| [`ru-wildberries`](./data-geoip/ru-wildberries.txt) | 8 | 8 / 0 | `85.198.76.0/22`, `91.230.107.0/24`, `176.101.88.0/24` | Ручной набор Wildberries |
| [`ru-yandex`](./data-geoip/ru-yandex.txt) | 16 | 15 / 1 | `5.45.192.0/18`, `5.255.192.0/18`, `37.9.64.0/18` | Ручной набор Яндекс |

Ручные наборы не означают полного покрытия ASN или исключительного использования каждой сети одним сервисом. В изменениях A–C GeoIP оставлен без изменений.

## Прибитые IP: DnsHosts

Таблица сформирована непосредственно из шести JSON-профилей Happ/Incy. Это сохранённые статические значения, а не свежая DNS-проверка; актуальность и исправления адресов относятся к отдельному блоку D.

| Домен | IP в DnsHosts | Где задан |
|---|---|---|
| `lkfl2.nalog.ru` | `213.24.64.175` | Все 6 профилей |
| `lknpd.nalog.ru` | `213.24.64.181` | Все 6 профилей |
| `service.nalog.ru` | `213.24.64.140` | Все 6 профилей |
| `nalog.gov.ru` | `37.220.164.100` | Все 6 профилей |
| `gosuslugi.ru` | `213.59.253.7` | Все 6 профилей |
| `esia.gosuslugi.ru` | `213.59.253.8` | Все 6 профилей |
| `lk.gosuslugi.ru` | `213.59.253.6` | Все 6 профилей |
| `online.sberbank.ru` | `84.252.149.51` | Все 6 профилей |
| `sberbank.ru` | `84.252.149.206` | Все 6 профилей |
| `vtb.ru` | `195.242.82.13` | Все 6 профилей |
| `online.vtb.ru` | `185.179.146.43` | Все 6 профилей |
| `id.vtb.ru` | `185.179.144.34` | Все 6 профилей |

<!-- END GENERATED ROUTING TABLES -->

## Использование в конфигах

Примеры ниже показывают подключение категорий, а не полную конфигурацию клиента. Имена outbound и порядок правил должны соответствовать вашему конфигу.

### Xray / v2ray

В `routing.rules` можно использовать доменную категорию и отдельно RU IP. Эти правила следует размещать с учётом уже существующих исключений и правил Proxy/Block.

```json
[
  {
    "type": "field",
    "domain": ["geosite:category-ru-whitelist"],
    "outboundTag": "direct"
  },
  {
    "type": "field",
    "ip": ["geoip:ru"],
    "outboundTag": "direct"
  }
]
```

### Mihomo

Для конфигурации с поддержкой и настроенной загрузкой geodata категории используются в `rules`. Это пример подключения, а не изменение готовых профилей Happ/Incy.

```yaml
rules:
  - GEOSITE,category-ru-whitelist,DIRECT
  - GEOIP,ru,DIRECT
```

## Структура репозитория

```text
├── geosite.dat                 # Собственная сборка доменных категорий
├── geoip.dat                   # Собственная сборка IP-категорий
├── data-geosite/               # Полные исходные списки доменов и include
├── data-geoip/                 # Полные исходные списки CIDR
├── HAPP/                      # JSON, deeplink и QR профилей Happ
├── INCY/                      # JSON, deeplink и QR профилей Incy
├── geoip-config.json           # Конфигурация сборки GeoIP
├── CATEGORY_STATS.md           # Полная статистика и SHA256 сборок
├── HAPP_INCY_USAGE.md           # Инструкция по профилям
├── changes/                   # Согласованные изменения
├── scripts/build_metadata.py   # Обновление статистики и таблиц README
├── scripts/readme_tables.py    # Генератор подробных таблиц
├── scripts/build_default_links.py
└── scripts/validate_abc.py      # Проверки правил, профилей и документации
```

## Обновления

Еженедельная проверка назначена на воскресенье, 03:00 МСК. Она использует актуальный `main`, сохраняет согласованные A–C и не изменяет блок D.

Автоматически разрешена синхронизация `data-geoip/ru.txt` и пересборка собственной `geoip.dat`; остальные IP-категории сохраняются. Новые домены и изменения маршрутов выносятся на согласование независимо от наличия подтверждения Минцифры; без реального изменения данных не создаются пустые коммиты и релизы.

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

`build_metadata.py` одновременно обновляет `CATEGORY_STATS.md` и подробные таблицы README: категории, примеры доменов, CIDR и DnsHosts. Ручные разделы README сохраняются; `--check` проверяет актуальность обоих документов без записи.

`validate_abc.py` проверяет исходники и бинарник, существование категорий в профилях, точечные правила `full:`, согласованные наборы, равенство JSON/deeplink и таблицы README. Флаг `--qr` дополнительно декодирует DEFAULT QR.

## История и источники

Согласованные изменения перечислены в [журнале A–C от 2026-09-30](./changes/2026-09-30-abc.md) и [дополнении YouTube от 2026-10-05](./changes/2026-10-05-youtube.md). Источники доменных наборов и правила проверки отделены от операторских гарантий.

- **RU GeoIP**: [frayZV/simple-ru-geoip](https://github.com/frayZV/simple-ru-geoip), синхронизация исходного `ru.txt`.
- **Сервисные домены**: [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community), сайты сервисов и их инфраструктурные сведения.
- **Дополнительные кандидаты**: [hxehex/russia-mobile-internet-whitelist](https://github.com/hxehex/russia-mobile-internet-whitelist); запись в стороннем списке сама по себе не доказывает доступность у всех операторов.

Автор проекта: [GrimbirdUsers](https://github.com/GrimbirdUsers). Для предложения изменений откройте [Issue](https://github.com/GrimbirdUsers/ru-routing-dat/issues) с доменом, сценарием сбоя и техническим обоснованием; ссылка на официальное подтверждение не обязательна.
