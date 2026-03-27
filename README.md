# System regułowy wspomagający sprzedaż sprzętu komputerowego

Gotowy szkielet projektu Flask zgodny z założeniami z PDF:
- katalog produktów,
- koszyk w sesji,
- własny prosty silnik reguł,
- promocje zestawowe, ilościowe i progowe,
- konflikt między regułami R1 i R2,
- zapis wyników analizy do bazy SQLite.

## Reguły zaimplementowane w projekcie
- **R1** — komputer + monitor => rabat 5% na cały koszyk,
- **R2** — komputer + klawiatura + mysz => rabat 7% na akcesoria,
- **R3** — co najmniej 3 sztuki tego samego monitora => rabat 10% na te monitory,
- **R4** — koszyk powyżej 8000 zł => dodatkowe 3% rabatu,
- **R5** — co najmniej 2 drukarki => darmowa dostawa,
- **R6** — konflikt R1 i R2 rozstrzygany przez pozostawienie korzystniejszej promocji.

## Jak uruchomić
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Domyślnie aplikacja działa na SQLite i sama utworzy plik bazy w katalogu `instance/shop.db`.

## Struktura
- `app/models.py` — modele SQLAlchemy,
- `app/routes.py` — trasy Flask,
- `app/services/cart_service.py` — obsługa koszyka,
- `app/services/pricing_service.py` — analiza koszyka i zapis wyników,
- `app/rules/base.py` — klasy `Rule`, `Facts`, `RuleResult`,
- `app/rules/engine.py` — silnik wykonujący reguły,
- `app/rules/promotions.py` — definicje promocji.

## Uwaga praktyczna
Koszyk jest trzymany w sesji, a wynik analizy promocji zapisuje się w bazie jako historia koszyków. To jest prostsze niż pełny checkout, a na projekt wystarcza i dobrze wygląda na prezentacji.
