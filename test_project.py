import pytest
from project import DB_PATH, filter_materials, format_tables, load_materials, rank_materials

def test_load_materials():
    liste = load_materials(DB_PATH)
    assert len(liste) == 16
    ilk = liste[0]
    assert "name" in ilk
    assert "elastic_modulus" in ilk
    assert "tensile_strength" in ilk
    with pytest.raises(FileNotFoundError):
        load_materials("nonexistent_materials.db")
def test_filter_materials():
    ornekler = [
        {
            "name": "Steel A",
            "category": "Metal",
            "density": 7.85,
            "tensile_strength": 900.0,
            "elastic_modulus": 210.0,
            "max_temp": 480.0,
            "corrosion_resistance": 4,
            "cost": 3.0
        },
        {
            "name": "Polymer B",
            "category": "Polymer",
            "density": 1.10,
            "tensile_strength": 50.0,
            "elastic_modulus": 2.5,
            "max_temp": 90.0,
            "corrosion_resistance": 8,
            "cost": 2.5
        },
        {
            "name": "Alloy C",
            "category": "Metal",
            "density": 4.43,
            "tensile_strength": 950.0,
            "elastic_modulus": 114.0,
            "max_temp": 450.0,
            "corrosion_resistance": 10,
            "cost": 35.0
        }
    ]
    kosullar = {
        "min_tensile": 300.0,
        "min_modulus": 100.0,
        "min_temp": 200.0,
        "max_cost": 10.0,
        "min_corrosion": None
    }
    uygunlar, elenenler = filter_materials(ornekler, kosullar)
    assert len(uygunlar) == 1
    assert uygunlar[0]["name"] == "Steel A"
    assert len(elenenler) == 2
    assert elenenler[0]["name"] == "Polymer B"
    assert "Low elastic modulus" in elenenler[0]["reasons"]
    assert "Low max temp" in elenenler[0]["reasons"]
    assert elenenler[1]["name"] == "Alloy C"
    assert elenenler[1]["reasons"] == "Over budget"
    hepsi, hicbiri = filter_materials(ornekler, {})
    assert len(hepsi) == 3
    assert len(hicbiri) == 0
def test_rank_materials():
    ornekler = [
        {
            "name": "Carbon Fiber (CFRP)",
            "category": "Composite",
            "density": 1.55,
            "tensile_strength": 1500.0,
            "elastic_modulus": 135.0,
            "max_temp": 180.0,
            "corrosion_resistance": 10,
            "cost": 42.0
        },
        {
            "name": "AISI 4140 Alloy Steel",
            "category": "Metal",
            "density": 7.85,
            "tensile_strength": 950.0,
            "elastic_modulus": 210.0,
            "max_temp": 480.0,
            "corrosion_resistance": 4,
            "cost": 2.8
        }
    ]
    havacilik = rank_materials(ornekler, "aerospace")
    assert havacilik[0]["name"] == "Carbon Fiber (CFRP)"
    assert havacilik[0]["score"] >= havacilik[1]["score"]
    tren = rank_materials(ornekler, "rail")
    assert tren[0]["name"] == "AISI 4140 Alloy Steel"
    tekli = rank_materials([ornekler[0]], "automotive")
    assert tekli[0]["score"] == 100.0
    assert rank_materials([], "rail") == []
    with pytest.raises(ValueError):
        rank_materials(ornekler, "marine")
def test_format_tables():
    sirali = [
        {
            "name": "Aluminum 6061-T6",
            "category": "Metal",
            "density": 2.7,
            "tensile_strength": 310.0,
            "elastic_modulus": 69.0,
            "specific_strength": 114.8,
            "max_temp": 200.0,
            "corrosion_resistance": 7,
            "cost": 3.5,
            "score": 85.4
        }
    ]
    elenen = [
        {
            "name": "ABS Polymer",
            "category": "Polymer",
            "reasons": "Low tensile strength, Low elastic modulus"
        }
    ]
    metin = format_tables(sirali, elenen)
    assert "Recommended Materials" in metin
    assert "Aluminum 6061-T6" in metin
    assert "Eliminated Materials" in metin
    assert "Low elastic modulus" in metin
    bos_metin = format_tables([], [])
    assert "No materials matched all engineering conditions." in bos_metin
    assert "No materials were eliminated." in bos_metin
