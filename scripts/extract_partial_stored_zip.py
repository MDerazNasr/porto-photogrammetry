#!/usr/bin/env python3
"""Extract selected stored entries from a partial streaming ZIP download.

Dropbox's shared-folder ZIP uses data descriptors and stores JPEGs without
compression. This helper is intentionally narrow: it validates the local
header, descriptor sizes, and CRC before writing requested entries.
"""

from __future__ import annotations

import argparse
import binascii
import struct
from pathlib import Path


LOCAL = b"PK\x03\x04"
DESCRIPTOR = b"PK\x07\x08"


def extract(archive: Path, output: Path, wanted: set[str]) -> list[str]:
    data = archive.read_bytes()
    output.mkdir(parents=True, exist_ok=True)
    extracted: list[str] = []
    offset = 0
    while wanted:
        offset = data.find(LOCAL, offset)
        if offset < 0 or offset + 30 > len(data):
            break
        fields = struct.unpack_from("<IHHHHHIIIHH", data, offset)
        _, _, flags, method, _, _, _, compressed_size, _, name_len, extra_len = fields
        name_start = offset + 30
        name_end = name_start + name_len
        payload_start = name_end + extra_len
        if payload_start > len(data):
            break
        name = data[name_start:name_end].decode("utf-8")
        descriptor = -1
        if flags & 0x08:
            candidate = data.find(DESCRIPTOR, payload_start)
            while candidate >= 0 and candidate + 16 <= len(data):
                candidate_size = struct.unpack_from("<I", data, candidate + 8)[0]
                if candidate_size == candidate - payload_start:
                    descriptor = candidate
                    break
                candidate = data.find(DESCRIPTOR, candidate + 1)
            if descriptor < 0:
                break
            next_offset = descriptor + 16
        else:
            next_offset = payload_start + compressed_size
        if name in wanted:
            if method != 0 or not flags & 0x08:
                raise ValueError(f"unsupported ZIP entry encoding for {name}")
            crc, compressed_size, uncompressed_size = struct.unpack_from(
                "<III", data, descriptor + 4
            )
            payload = data[payload_start:descriptor]
            if len(payload) != compressed_size or len(payload) != uncompressed_size:
                raise ValueError(f"size mismatch for {name}")
            if binascii.crc32(payload) & 0xFFFFFFFF != crc:
                raise ValueError(f"CRC mismatch for {name}")
            destination = output / Path(name).name
            destination.write_bytes(payload)
            wanted.remove(name)
            extracted.append(name)
        offset = next_offset
    return extracted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("entries", nargs="+")
    args = parser.parse_args()
    wanted = set(args.entries)
    extracted = extract(args.archive, args.output, wanted)
    for name in extracted:
        print(name)
    if wanted:
        raise SystemExit("missing entries: " + ", ".join(sorted(wanted)))


if __name__ == "__main__":
    main()
