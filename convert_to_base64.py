import base64
import requests
import os

def convert_multiple_to_base64(urls):
    combined_text = ""
    
    for url in urls:
        # Download text file from the URL
        response = requests.get(url)
        if response.status_code == 200:
            combined_text += response.text + "\n"  
        else:
            print(f"Failed to fetch data from URL: {url}")

    # Encode combined text to base64
    encoded_bytes = base64.b64encode(combined_text.encode('utf-8'))
    encoded_text = encoded_bytes.decode('utf-8')

    # Check if content needs updating
    needs_update = True
    if os.path.exists('base64.txt'):
        with open('base64.txt', 'r') as f:
            existing_content = f.read()
            if encoded_text == existing_content:
                needs_update = False

    # Save base64-encoded text (only if changed)
    if needs_update:
        with open('base64.txt', 'w') as f:
            f.write(encoded_text)
        print("Conversion complete and changes saved.")
    else:
        print("No changes detected.")

if __name__ == "__main__":
    urls = [
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
        "https://raw.githubusercontent.com/snaCW/Config/refs/heads/main/config.txt"
    ]
    convert_multiple_to_base64(urls)
