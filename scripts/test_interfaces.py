#!/usr/bin/env python3
import json
import requests
from datetime import datetime
import shutil
import os

# JSON 文件路径
DATA_FILE = "data/sources.json"
DOCS_FILE = "docs/data.json"

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
        print(f"{source['name']}: {'✅ 正常' if is_ok else '❌ 失效'}")

    save_sources(sources)

    # ✅ 复制结果用于 GitHub Pages 页面展示
    os.makedirs("docs", exist_ok=True)
    shutil.copy(DATA_FILE, DOCS_FILE)

    # ✅ 统计信息
    total = len(sources)
    success = sum(1 for s in sources if s["status"] == 1)
    fail = total - success
    success_rate = round((success / total) * 100, 2) if total > 0 else 0.0

    print("\n📊 接口测试统计")
    print(f"接口总数: {total}")
    print(f"成功数量: {success}")
    print(f"失败数量: {fail}")
    print(f"成功率: {success_rate}%")

if __name__ == "__main__":
    main()
