#!/usr/bin/env python3
"""Read protobuf databases without generated bindings; document actual build counts."""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def varint(blob, offset):
    value = shift = 0
    while True:
        byte = blob[offset]
        offset += 1
        value |= (byte & 127) << shift
        if byte < 128:
            return value, offset
        shift += 7
        if shift > 70:
            raise ValueError("Invalid protobuf varint")


def fields(blob):
    offset = 0
    while offset < len(blob):
        tag, offset = varint(blob, offset)
        number, wire = tag >> 3, tag & 7
        if wire == 0:
            value, offset = varint(blob, offset)
        elif wire == 2:
            size, offset = varint(blob, offset)
            value = blob[offset:offset + size]
            offset += size
            if len(value) != size:
                raise ValueError("Truncated protobuf")
        elif wire in (1, 5):
            size = 8 if wire == 1 else 4
            value = blob[offset:offset + size]
            offset += size
        else:
            raise ValueError(f"Unsupported protobuf wire type {wire}")
        yield number, value


def entries(path):
    result = {}
    for number, message in fields(path.read_bytes()):
        if number != 1:
            continue
        parts = list(fields(message))
        name = next(value.decode().lower() for key, value in parts if key == 1)
        assert name not in result, f"Duplicate category: {name}"
        result[name] = [value for key, value in parts if key == 2]
    return result


def geosite_rules(path):
    types = {0: "keyword", 1: "regexp", 2: "domain", 3: "full"}
    result = {}
    for name, messages in entries(path).items():
        rules = set()
        for message in messages:
            parts = dict(fields(message))
            rules.add((types[parts.get(1, 0)], parts[2].decode().lower()))
        result[name] = rules
    return result


def source_lines(path):
    return [line.split("#", 1)[0].strip() for line in path.read_text().splitlines()
            if line.split("#", 1)[0].strip()]


def render():
    lines = [
        "# Статистика сборки",
        "",
        "Сгенерировано `python3 scripts/build_metadata.py` из файлов этого checkout. "
        "Ручное редактирование счётчиков не требуется.",
        "",
        "Счётчик бинарника означает число правил после обработки include и оптимизации. "
        "Категории перекрываются; сумма не означает число уникальных сайтов или IP.",
        "",
    ]
    for filename, directory, suffix, label in (
        ("geosite.dat", "data-geosite", "", "доменных правил"),
        ("geoip.dat", "data-geoip", ".txt", "CIDR"),
    ):
        path = ROOT / filename
        data = entries(path)
        lines += [
            f"## {filename}", "",
            f"Категорий: {len(data)}. Записей по всем категориям: "
            f"{sum(map(len, data.values()))} {label}. Размер: {path.stat().st_size} байт.",
            "",
            f"SHA256: `{hashlib.sha256(path.read_bytes()).hexdigest()}`.", "",
            "| Категория | Строк исходника без комментариев | Записей в бинарнике |",
            "|---|---:|---:|",
        ]
        for name, messages in sorted(data.items()):
            source = ROOT / directory / (name + suffix)
            count = len(source_lines(source)) if source.exists() else "нет файла"
            lines.append(f"| `{name}` | {count} | {len(messages)} |")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = ROOT / "CATEGORY_STATS.md"
    text = render()
    if args.check:
        assert output.read_text() == text, "CATEGORY_STATS.md is stale"
        print("PASS: build statistics match current files")
    else:
        output.write_text(text)
        print(f"Generated {output.name}")
