# Datavalidering med Pandera

## Om projektet

Det här projektet handlar om datavalidering i Python med Pandera.

Jag använder orderdata från CSV-filer och kontrollerar datan innan den används för analys. Jag testar både giltiga och ogiltiga data.

Exempel på kontroller är:

* obligatoriska kolumner
* saknade värden
* datatyper
* datum
* positiva värden
* rabatt mellan 0 och 1
* tillåtna produktkategorier

Om valideringen misslyckas körs inte analysen.

## Jämförelse med Pandas

Jag har också gjort en enklare manuell validering med Pandas.

Syftet är att jämföra hur samma problem kan lösas med Pandas och vad Pandera tillför.

Pandera samlar reglerna i ett schema och kan visa detaljer om vilka värden som inte klarar valideringen. Pandas ger större frihet och kan vara enklare för mindre och mer specifika kontroller.

## Projektstruktur

```text
pandera_data_validation/
├── data/
├── tests/
│   ├── conftest.py
│   └── test_validation.py
├── validate_orders.py
├── manual_validation.py
├── analysis.py
├── main.py
├── requirements.txt
└── README.md
```

## Installation

Skapa och aktivera en virtuell miljö och installera paketen:

```bash
python -m pip install -r requirements.txt
```

## Köra programmet

Giltig data:

```bash
python main.py data/valid_orders.csv
```

Ogiltig data:

```bash
python main.py data/invalid_orders.csv
```

Manuell validering:

```bash
python manual_validation.py data/invalid_orders.csv
```

## Test

Testerna körs med pytest:

```bash
python -m pytest -v
```

Alla 3 tester ska gå igenom.

## Källor

* Pandera: https://pandera.readthedocs.io/
* Pandas: https://pandas.pydata.org/docs/
* pytest: https://docs.pytest.org/

```
```
