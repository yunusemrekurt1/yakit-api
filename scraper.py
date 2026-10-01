import httpx

SEHIRLER = {6: "ankara", 34: "istanbul", 934: "istanbul", 35: "izmir"}
def opet_cek(il_kodu):
    url = "https://api.opet.com.tr/api/fuelprices/prices"
    params = {"ProvinceCode": il_kodu, "IncludeAllProducts": "true"}
    r = httpx.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    r.raise_for_status()

    sonuc = []
    for ilce in r.json():
        for urun in ilce["prices"]:
            sonuc.append({
                "firma": "opet",
                "sehir": SEHIRLER[il_kodu],
                "ilce": ilce["districtName"],
                "urun": urun["productName"],
                "kod": urun["productShortName"],
                "fiyat": urun["amount"],
            })
    return sonuc

if __name__ == "__main__":
    for kod in SEHIRLER:
        veri = opet_cek(kod)
        print(SEHIRLER[kod], "->", len(veri), "kayıt | örnek:", veri[0])