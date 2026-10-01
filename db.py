import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
import sqlite3
from datetime import datetime

DB = "fuel.db"

def tablo_olustur():
    with sqlite3.connect(DB) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS prices (
            firma TEXT, sehir TEXT, ilce TEXT, urun TEXT, kod TEXT,
            fiyat REAL, guncelleme TEXT,
            PRIMARY KEY (firma, sehir, ilce, kod))""")

def kaydet(kayitlar):
        simdi = datetime.now(ZoneInfo("Europe/Istanbul")).isoformat(timespec="seconds")
    with sqlite3.connect(DB) as db:
        db.executemany("""INSERT OR REPLACE INTO prices VALUES
            (:firma, :sehir, :ilce, :urun, :kod, :fiyat, :guncelleme)""",
            [{**k, "guncelleme": simdi} for k in kayitlar])

def getir(sehir, ilce=None, kod=None, firma=None):
    q, p = "SELECT * FROM prices WHERE sehir = ?", [sehir]
    for alan, deger in (("ilce", ilce), ("kod", kod), ("firma", firma)):
        if deger:
            q += f" AND {alan} = ?"
            p.append(deger)
    q += " ORDER BY ilce, fiyat"
    with sqlite3.connect(DB) as db:
        db.row_factory = sqlite3.Row
        return [dict(r) for r in db.execute(q, p)]