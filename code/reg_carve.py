import os
import mmap

# Constants 

# Registry hive header: 72 65 67 66 == "regf"
HEADER = b"\x72\x65\x67\x66"

# UTF-16LE "ntuser": 6E 00 74 00 75 00 73 00 65 00 72
NTUSER_PATTERN = b"\x6E\x00\x74\x00\x75\x00\x73\x00\x65\x00\x72"

HEADER_SIZE = 0x1000          # 4096 bytes
FILE_LEN_OFFSET = 0x28        # offset from regf to length field
FILE_LEN_SIZE = 4             # 4-byte little-endian length


# Core logic

def carve_image(input_path: str, output_dir: str = "carved_output") -> None:
    """
    Scan a binary disk image (e.g., .img, .dd) for NTUSER.DAT-style registry hives.

    For each occurrence of:
      - HEADER (72 65 67 66) at offset N
      - 'ntuser' (UTF-16LE) somewhere in the first 4096 bytes starting at N

    Steps:
      - Read 4 bytes at offset N + 0x28 -> little-endian integer L
      - Treat L as the logical hive length (excluding the 4KB header / slack)
      - Carve bytes from N to N + 0x1000 + L (clamped to EOF)
      - Write them out as a single output file.
    """

    os.makedirs(output_dir, exist_ok=True)

    file_size = os.path.getsize(input_path)
    print(f"[+] Input image : {input_path}")
    print(f"[+] File size   : {file_size} bytes")
    print(f"[+] Output dir  : {output_dir}")
    print("[+] Scanning for NTUSER hives (regf + 'ntuser' + length @ 0x28)...")

    headers_found = 0
    carved = 0

    with open(input_path, "rb") as f:
        # Map entire file read-only; OS will handle paging
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            offset = 0

            while True:
                index = mm.find(HEADER, offset)
                if index == -1:
                    break  # no more regf headers

                headers_found += 1

                # Look at the first 4KB to decide if this is an NTUSER hive
                block_end = min(index + HEADER_SIZE, file_size)
                block = mm[index:block_end]

                if NTUSER_PATTERN in block:
                    # Ensure we can read the 4-byte length field
                    len_start = index + FILE_LEN_OFFSET
                    len_end = len_start + FILE_LEN_SIZE

                    if len_end > file_size:
                        print(f"[-] Header at 0x{index:08X}: cannot read length field (near EOF)")
                        offset = index + 1
                        continue

                    length_bytes = mm[len_start:len_end]
                    hive_rest_len = int.from_bytes(length_bytes, byteorder="little", signed=False)

                    total_len = HEADER_SIZE + hive_rest_len
                    carve_end = min(index + total_len, file_size)

                    print(
                        f"[+] Valid NTUSER hive at 0x{index:08X}: "
                        f"len_field=0x{hive_rest_len:08X}, "
                        f"total_to_carve={carve_end - index} bytes"
                    )

                    chunk = mm[index:carve_end]

                    out_name = f"ntuser_{carved}.dat"
                    out_path = os.path.join(output_dir, out_name)
                    with open(out_path, "wb") as out_f:
                        out_f.write(chunk)

                    print(f"    -> Carved hive to {out_path}")
                    carved += 1
                else:
                    print(f"[-] Header at 0x{index:08X} rejected (no 'ntuser' in first 4KB)")

                # Continue searching after this header
                offset = index + 1

    print("\n[+] Scan complete.")
    print(f"    regf headers found : {headers_found}")
    print(f"    NTUSER hives carved: {carved}")


# CLI entrypoint

if __name__ == "__main__":
    print("=== Image Carver → NTUSER.DAT extractor ===")
    input_path = input("Enter full path to the disk image file (e.g., .img, .dd): ").strip().strip('"')

    if not os.path.isfile(input_path):
        print(f"[!] File not found: {input_path}")
    else:
        carve_image(input_path, output_dir="carved_output")
