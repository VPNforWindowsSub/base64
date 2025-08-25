import base64
import requests
import os
import glob
import binascii
from datetime import datetime, timezone # Import datetime utilities

MAX_FILE_SIZE_MB = 1
OUTPUT_FILENAME_TEMPLATE = 'base64_{:03}.txt'

MAX_B64_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
TARGET_RAW_SIZE = int(MAX_B64_SIZE_BYTES * 0.75)

def fetch_content_lines(plain_text_urls, base64_urls):
    """
    Fetches content from two lists of URLs.
    - Plain text URLs are read as is.
    - Base64 URLs are decoded first.
    Returns a single, unified list of plain text lines.
    """
    all_lines = []
    with requests.Session() as session:
        print("\n--- Fetching Plain Text URLs ---")
        for i, url in enumerate(plain_text_urls, 1):
            try:
                print(f"[{i}/{len(plain_text_urls)}] Fetching from: {url}")
                response = session.get(url, timeout=15)
                response.raise_for_status()
                
                lines = [line for line in response.text.splitlines() if line.strip()]
                if lines:
                    all_lines.extend(lines)
                else:
                    print(f"  -> Warning: No content found at {url}")

            except requests.exceptions.RequestException as e:
                print(f"  -> Error: Failed to fetch data from {url}. Reason: {e}")

        print("\n--- Fetching and Decoding Base64 URLs ---")
        for i, url in enumerate(base64_urls, 1):
            try:
                print(f"[{i}/{len(base64_urls)}] Fetching from: {url}")
                response = session.get(url, timeout=15)
                response.raise_for_status()
                
                b64_content = response.text.strip()
                decoded_bytes = base64.b64decode(b64_content)
                decoded_text = decoded_bytes.decode('utf-8')

                lines = [line for line in decoded_text.splitlines() if line.strip()]
                if lines:
                    all_lines.extend(lines)
                else:
                    print(f"  -> Warning: Decoded content was empty for {url}")

            except requests.exceptions.RequestException as e:
                print(f"  -> Error: Failed to fetch data from {url}. Reason: {e}")
            except (binascii.Error, UnicodeDecodeError) as e:
                print(f"  -> Error: Failed to decode Base64 content from {url}. It might not be valid Base64. Reason: {e}")

    return all_lines

def cleanup_old_files():
    print("\nCleaning up old output files...")
    old_files = glob.glob('base64_*.txt')
    if not old_files:
        print("No old files to clean up.")
        return
        
    for f in old_files:
        try:
            os.remove(f)
            print(f"  -> Deleted {f}")
        except OSError as e:
            print(f"  -> Error deleting file {f}: {e}")


def process_and_write_chunks(lines):
    if not lines:
        print("\nNo content to process. Exiting.")
        return

    print(f"\nTotal lines fetched: {len(lines)}. Grouping into chunks...")
    
    generation_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
    timestamp_comment = f"# Generated on: {generation_time}"
    
    chunks = []
    current_chunk_lines = [timestamp_comment] # Start each chunk with the timestamp comment.
    current_chunk_size = len(timestamp_comment.encode('utf-8')) + 1

    for line in lines:
        line_size = len(line.encode('utf-8')) + 1
        
        if current_chunk_size + line_size > TARGET_RAW_SIZE and len(current_chunk_lines) > 1:
            chunks.append("\n".join(current_chunk_lines))
            current_chunk_lines = [timestamp_comment, line]
            current_chunk_size = (len(timestamp_comment.encode('utf-8')) + 1) + line_size
        else:
            current_chunk_lines.append(line)
            current_chunk_size += line_size

    if len(current_chunk_lines) > 1: 
        chunks.append("\n".join(current_chunk_lines))

    print(f"Content has been split into {len(chunks)} chunks.")
    print("Encoding and saving files...")

    for i, chunk_text in enumerate(chunks, 1):
        encoded_bytes = base64.b64encode(chunk_text.encode('utf-8'))
        encoded_text = encoded_bytes.decode('utf-8')
        
        filename = OUTPUT_FILENAME_TEMPLATE.format(i)
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(encoded_text)
            
            final_size_kb = os.path.getsize(filename) / 1024
            print(f"  -> Saved {filename} ({final_size_kb:.2f} KB)")
        except IOError as e:
            print(f"  -> Error: Could not write to file {filename}. Reason: {e}")

if __name__ == "__main__":
    plain_text_urls = [
        "https://raw.githubusercontent.com/dimzon/scaling-sniffle/main/all-sort.txt",
        "https://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/V2RAY_SUB.txt",
        "https://raw.githubusercontent.com/Space-00/V2ray-configs/refs/heads/main/config.txt",
        "https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/all.txt",
        "https://raw.githubusercontent.com/asakura42/vss/master/output.txt",
        "https://raw.githubusercontent.com/qjlxg/ss/refs/heads/master/list_raw.txt",
        "https://raw.githubusercontent.com/asdsadsddas123/freevpn/refs/heads/main/README.md",
        "https://raw.githubusercontent.com/asdsadsddas123/clashnodedfree/refs/heads/main/README.md",
        "https://raw.githubusercontent.com/asdsadsddas123/tizi/refs/heads/main/README.md",
        "https://raw.githubusercontent.com/asdsadsddas123/freev2raynode/refs/heads/main/README.md",
        "https://raw.githubusercontent.com/asdsadsddas123/fanqiang/refs/heads/main/README.md",
        "https://raw.githubusercontent.com/asdsadsddas123/shadowsocksfree/refs/heads/main/README.md",
        "https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/refs/heads/master/collected-proxies/row-url/actives.txt",
        "https://raw.githubusercontent.com/gfpcom/free-proxy-list/refs/heads/main/list/ss.txt",
        "https://raw.githubusercontent.com/gfpcom/free-proxy-list/refs/heads/main/list/vmess.txt",
        "https://raw.githubusercontent.com/LalatinaHub/Mineral/refs/heads/master/result/nodes",
        "https://raw.githubusercontent.com/snaCW/Config/refs/heads/main/config.txt",
        "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/refs/heads/main/configtg.txt",
        "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/V2Ray-Config-By-EbraSha-All-Type.txt",
        "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/refs/heads/main/all_configs.txt",
        "https://raw.githubusercontent.com/miladtahanian/V2RayCFGDumper/main/config.txt",
        "https://raw.githubusercontent.com/nyeinkokoaung404/V2ray-Configs/refs/heads/main/All_Configs_Sub.txt",
        "https://raw.githubusercontent.com/SonzaiEkkusu/V2RayDumper/refs/heads/main/config.txt",
        "https://raw.githubusercontent.com/theGreatPeter/v2rayNodes/refs/heads/main/nodes.txt",
        "https://raw.githubusercontent.com/SamanGho/v2ray_collector/refs/heads/main/v2tel_links1.txt",
        "https://raw.githubusercontent.com/SamanGho/v2ray_collector/refs/heads/main/v2tel_links2.txt",
        "https://raw.githubusercontent.com/ShatakVPN/ConfigForge/main/configs/all.txt"
    ]
    
    base64_urls = [
        "https://raw.githubusercontent.com/darknessm427/V2ray-Sub-Collector/refs/heads/main/Sort-By-Protocol/Darkness_vless.txt",
        "https://raw.githubusercontent.com/darknessm427/V2ray-Sub-Collector/refs/heads/main/Sort-By-Protocol/Darkness_vmess.txt",
        "https://raw.githubusercontent.com/darknessm427/V2ray-Sub-Collector/refs/heads/main/Sort-By-Protocol/Darkness_ss.txt",
        "https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/main/submerge/converted.txt",
        "https://raw.githubusercontent.com/VPNforWindowsSub/base64/refs/heads/main/base64file.txt"
    ]
    
    cleanup_old_files()
    all_lines = fetch_content_lines(plain_text_urls, base64_urls)
    process_and_write_chunks(all_lines)

    print("\nProcess complete.")
