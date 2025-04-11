#!/usr/bin/env python3
import json
import requests
from datetime import datetime

# JSON 文件路径
DATA_FILE = "data/sources.json"

def load_sources():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_sources(sources):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(sources, f, ensure_ascii=False, indent=2)

def test_interface(url):
    try:
        # 请求超时时间设为10秒
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except Exception:
        return False

def main():
    sources = load_sources()
    for source in sources:
        is_ok = test_interface(source["url"])
        source["status"] = 1 if is_ok else 0
        source["last_test_time"] = datetime.utcnow().isoformat() + "Z"
        print(f"{source['name']}: {'正常' if is_ok else '失效'}")
    save_sources(sources)

if __name__ == "__main__":
    main()
