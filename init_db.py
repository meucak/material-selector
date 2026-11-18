import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "materials.db")
def create_database(db_yolu=DB_PATH):
    baglanti = sqlite3.connect(db_yolu)
    imlec = baglanti.cursor()
    imlec.execute("DROP TABLE IF EXISTS materials")
    imlec.execute(
        "CREATE TABLE materials ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT NOT NULL UNIQUE, "
        "category TEXT NOT NULL, "
        "density REAL NOT NULL, "
        "tensile_strength REAL NOT NULL, "
        "elastic_modulus REAL NOT NULL, "
        "max_temp REAL NOT NULL, "
        "corrosion_resistance INTEGER NOT NULL, "
        "cost REAL NOT NULL"
        ")"
    )
    veriler = [
        ("AISI 1020 Steel", "Metal", 7.87, 420.0, 205.0, 400.0, 3, 1.2),
        ("AISI 4140 Alloy Steel", "Metal", 7.85, 950.0, 210.0, 480.0, 4, 2.8),
        ("316L Stainless Steel", "Metal", 8.00, 580.0, 193.0, 800.0, 9, 5.5),
        ("Cast Iron (Gray)", "Metal", 7.20, 250.0, 110.0, 450.0, 4, 1.0),
        ("Aluminum 6061-T6", "Metal", 2.70, 310.0, 69.0, 200.0, 7, 3.5),
        ("Aluminum 7075-T6", "Metal", 2.81, 572.0, 72.0, 180.0, 6, 6.5),
        ("Titanium Ti-6Al-4V", "Metal", 4.43, 950.0, 114.0, 450.0, 10, 35.0),
        ("Inconel 718", "Metal", 8.19, 1240.0, 200.0, 700.0, 10, 48.0),
        ("Magnesium AZ31B", "Metal", 1.77, 260.0, 45.0, 150.0, 3, 5.0),
        ("Copper C11000", "Metal", 8.94, 220.0, 117.0, 260.0, 8, 9.5),
        ("Carbon Fiber (CFRP)", "Composite", 1.55, 1500.0, 135.0, 180.0, 10, 42.0),
        ("Glass Fiber (GFRP)", "Composite", 1.85, 650.0, 28.0, 150.0, 9, 8.0),
        ("Aramid Fiber (Kevlar)", "Composite", 1.44, 1400.0, 70.0, 160.0, 9, 28.0),
        ("PEEK Polymer", "Polymer", 1.32, 100.0, 4.0, 250.0, 10, 65.0),
        ("Nylon 6,6 (PA66)", "Polymer", 1.14, 82.0, 2.8, 120.0, 8, 4.5),
        ("ABS Polymer", "Polymer", 1.05, 45.0, 2.2, 85.0, 7, 2.5)
    ]
    imlec.executemany(
        "INSERT INTO materials (name, category, density, tensile_strength, elastic_modulus, max_temp, corrosion_resistance, cost) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        veriler
    )
    baglanti.commit()
    baglanti.close()
if __name__ == "__main__":
    create_database()
    print("Database created:", DB_PATH)
