import httpx

HEADERS = {"User-Agent": "Mozilla/5.0"}
TR = str.maketrans("ÇĞİÖŞÜçğıöşüi", "CGIOSUCGIOSUI")

def normalize(s):
    return s.translate(TR).upper().strip()

# ---------- OPET ----------
OPET_SEHIRLER = {6: "ankara", 34: "istanbul", 934: "istanbul", 35: "izmir"}
OPET_URUNLER = {"KURS": "BENZIN", "MT_ECO": "MOTORIN", "MT_ULT": "MOTORIN_PREMIUM"}

def opet_cek(il_kodu):
    r = httpx.get("https://api.opet.com.tr/api/fuelprices/prices",
                  params={"ProvinceCode": il_kodu, "IncludeAllProducts": "true"},
                  headers=HEADERS, timeout=15)
    r.raise_for_status()
    sonuc = []
    for ilce in r.json():
        for urun in ilce["prices"]:
            kod = OPET_URUNLER.get(urun["productShortName"])
            if kod:
                sonuc.append({"firma": "opet", "sehir": OPET_SEHIRLER[il_kodu],
                              "ilce": normalize(ilce["districtName"]),
                              "urun": urun["productName"], "kod": kod, "fiyat": urun["amount"]})
    return sonuc

# ---------- SHELL ----------
SHELL_SEHIRLER = {"006": "ankara", "034": "istanbul", "035": "izmir"}
SHELL_URUNLER = {"37": "BENZIN", "34": "MOTORIN", "5": "LPG"}

def shell_cek(il_kodu):
    r = httpx.get("https://pompafiyat.turkiyeshell.com/api/Public/prices",
                  params={"citycode": il_kodu}, headers=HEADERS, timeout=20)
    r.raise_for_status()
    veri = r.json()
    isimler = {p["fepProductCode"].strip(): p["genProductName"] for p in veri["products"]}
    sonuc = []
    for grup in veri["groups"]:
        for ilce in grup["counties"]:
            for urun_kodu, fiyat in ilce["prices"].items():
                kod = SHELL_URUNLER.get(urun_kodu.strip())
                if kod and fiyat:
                    sonuc.append({"firma": "shell", "sehir": SHELL_SEHIRLER[il_kodu],
                                  "ilce": normalize(ilce["countyName"]),
                                  "urun": isimler.get(urun_kodu.strip(), kod),
                                  "kod": kod, "fiyat": fiyat})
    return sonuc

# ---------- HEPSİ ----------
# Opet yurt dışı sunucuları engelliyor, Türkiye'de sunucuya geçince aç:
# KAYNAKLAR = [(opet_cek, k) for k in OPET_SEHIRLER] + [(shell_cek, k) for k in SHELL_SEHIRLER]
KAYNAKLAR = [(shell_cek, k) for k in SHELL_SEHIRLER]
SEHIRLER = sorted(set(SHELL_SEHIRLER.values()))

if __name__ == "__main__":
    for fonk, kod in KAYNAKLAR:
        try:
            print(fonk.__name__, kod, "->", len(fonk(kod)), "kayıt")
        except Exception as e:
            print(fonk.__name__, kod, "HATA:", e)