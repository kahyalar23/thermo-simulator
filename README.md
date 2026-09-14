# Thermodynamic Cycle Simulator

ITÜ İnşaat & Makine Mühendisliği için termodinamik çevrim simülatörü.

## Özellikler

- **Carnot Çevrimi**: İdeal tersine çevrilebilir çevrim (iki havza arasında)
- **Brayton Çevrimi**: Gaz türbinü çevrimi (sabit basınçta ısı alışverişi)
- **Rankine Çevrimi**: Bugücü çevrim (faize dönüşen çalışmanın faz değişimi)

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

```bash
# Hepsi için test çalıştır
python main.py --cycle all

# Sadece Carnot
python main.py --cycle carnot --T_hot 800 --T_cold 300

# Brayton
python main.py --cycle brayton --T_in 1200 --pr 10

# Rankine
python main.py --cycle rankine --p_high 10 --p_low 0.05
```

## Çıktı

- Isikverimli ve verimlilik hesaplamalari
- T-s (sıcaklık-entropi) ve P-v (basınç-hacim) diagramları
- Tablo formatında durum noktalari

## Proje Yapısı

```
thermo-simulator/
├── main.py              # CLI giriş noktası
├── cycles/
│   ├── carnot.py        # Carnot çevrimi
│   ├── brayton.py       # Brayton çevrimi
│   └── rankine.py       # Rankine çevrimi
├── utils/
│   └── plots.py         # Visualizasyon fonksiyonlari
├── tests/
│   └── test_cycles.py   # Unit testleri
└── pyproject.toml
```
