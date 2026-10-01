import httpx, json

url = "https://pompafiyat.turkiyeshell.com/api/Public/prices?citycode=006"
veri = httpx.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20).json()

with open("shell.json", "w", encoding="utf-8") as f:
    json.dump(veri, f, ensure_ascii=False, indent=2)

print("ÜRÜNLER:")
for p in veri["products"]:
    print(" ", p["fepProductCode"].strip(), "|", p["fepProductName"], "|", p.get("genProductName"))

print("\nİLK GRUP:")
print(json.dumps(veri["groups"][0], ensure_ascii=False, indent=2)[:1500])