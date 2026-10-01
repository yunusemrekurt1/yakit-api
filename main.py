from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from scraper import opet_cek, SEHIRLER
import db

def guncelle():
    for kod in SEHIRLER:
        try:
            db.kaydet(opet_cek(kod))
        except Exception as e:
            print("Hata:", kod, e)
    print("Fiyatlar güncellendi")

@asynccontextmanager
async def lifespan(app):
    db.tablo_olustur()
    guncelle()
    zamanlayici = BackgroundScheduler()
    zamanlayici.add_job(guncelle, "interval", hours=6)
    zamanlayici.start()
    yield
    zamanlayici.shutdown()

app = FastAPI(title="Yakıt API", lifespan=lifespan)

def tr_buyuk(s):
    return s.replace("i", "İ").replace("ı", "I").upper()

@app.get("/")
def ana():
        return {"mesaj": "Yakıt API çalışıyor!", "sehirler": sorted(set(SEHIRLER.values()))}

@app.get("/prices")
def fiyatlar(sehir: str, ilce: str | None = None, urun: str | None = None):
    sehir = sehir.lower()
    if sehir not in SEHIRLER.values():
        raise HTTPException(404, "Şehir bulunamadı")
    return db.getir(sehir, tr_buyuk(ilce) if ilce else None, urun.upper() if urun else None)

    import httpx

@app.get("/test-shell")
def test_shell():
    try:
        r = httpx.get("https://pompafiyat.turkiyeshell.com/api/Public/prices?citycode=006",
                      headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        return {"durum": r.status_code, "ornek": r.text[:300]}
    except Exception as e:
        return {"hata": str(e)}