from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from scraper import KAYNAKLAR, SEHIRLER, normalize
import db

def guncelle():
    for fonk, kod in KAYNAKLAR:
        try:
            db.kaydet(fonk(kod))
        except Exception as e:
            print("Hata:", fonk.__name__, kod, e)
    print("Fiyatlar güncellendi")

@asynccontextmanager
async def lifespan(app):
    db.tablo_olustur()
    zamanlayici = BackgroundScheduler()
    zamanlayici.add_job(guncelle, "interval", hours=6, next_run_time=datetime.now())
    zamanlayici.start()
    yield
    zamanlayici.shutdown()

app = FastAPI(title="Yakıt API", lifespan=lifespan)

@app.get("/")
def ana():
        return {"mesaj": "Yakıt API çalışıyor!", "sehirler": SEHIRLER,
            "urunler": ["BENZIN", "MOTORIN", "LPG"]}
@app.get("/prices")
def fiyatlar(sehir: str, ilce: str | None = None, urun: str | None = None, firma: str | None = None):
    sehir = normalize(sehir).lower()
    if sehir not in SEHIRLER:
        raise HTTPException(404, "Şehir bulunamadı")
    return db.getir(sehir, normalize(ilce) if ilce else None,
                    urun.upper() if urun else None, firma.lower() if firma else None)