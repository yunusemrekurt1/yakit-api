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
    simdi = datetime.now().isoformat(timespec="seconds")
    with sqlite3.connect(DB) as db:
        db.executemany("""INSERT OR REPLACE INTO prices VALUES
            (:firma, :sehir, :ilce, :urun, :kod, :fiyat, :guncelleme)""",
            [{**k, "guncelleme": simdi} for k in kayitlar])

def getir(sehir, ilce=None, kod=None):
    q, p = "SELECT * FROM prices WHERE sehir = ?", [sehir]
    if ilce:
        q += " AND ilce = ?"; p.append(ilce)
    if kod:
        q += " AND kod = ?"; p.append(kod)
    with sqlite3.connect(DB) as db:
        db.row_factory = sqlite3.Row
        return [dict(r) for r in db.execute(q, p)]