# System regułowy wspomagający sprzedaż sprzętu komputerowego

Projekt przedstawia prostą aplikację webową napisaną we Flasku, która symuluje sklep komputerowy. Użytkownik wybiera produkty, dodaje je do koszyka, a następnie uruchamia analizę promocji. Najważniejszym elementem projektu jest własny silnik regułowy, który sprawdza zawartość koszyka i automatycznie nalicza odpowiednie rabaty.

Aplikacja nie jest pełnym sklepem internetowym z płatnościami i kontami użytkowników. To projekt demonstracyjny pokazujący, jak można wykorzystać reguły biznesowe do wspomagania sprzedaży sprzętu komputerowego.

## Co robi aplikacja

Aplikacja umożliwia:

- wyświetlanie katalogu produktów podzielonych na kategorie,
- dodawanie produktów do koszyka,
- zmianę ilości produktów w koszyku,
- usuwanie produktów z koszyka,
- uruchomienie analizy promocji,
- naliczanie rabatów na podstawie reguł,
- rozwiązywanie konfliktu między promocjami,
- zapis wyniku analizy do bazy SQLite,
- wyświetlenie podsumowania zamówienia oraz logu działania reguł.

## Jak działa przepływ programu

1. Użytkownik wchodzi na stronę z katalogiem produktów.
2. Produkty są pobierane z bazy danych SQLite.
3. Użytkownik dodaje wybrane produkty do koszyka.
4. Koszyk jest tymczasowo przechowywany w sesji Flask.
5. Po kliknięciu przycisku `Uruchom analizę promocji` aplikacja zamienia koszyk na zestaw faktów.
6. Fakty trafiają do silnika regułowego.
7. Silnik sprawdza po kolei wszystkie reguły promocji.
8. Pasujące reguły dodają rabaty albo zmieniają koszt dostawy.
9. Jeżeli wystąpi konflikt między promocjami, system zostawia korzystniejszą promocję.
10. Wynik analizy jest zapisywany w bazie danych.
11. Użytkownik widzi podsumowanie zamówienia, aktywne promocje oraz log działania reguł.

## Reguły zaimplementowane w projekcie

| Kod | Opis reguły | Efekt |
| --- | --- | --- |
| R1 | Zakup komputera i monitora | Rabat 5% na cały koszyk |
| R2 | Zakup komputera, klawiatury i myszy | Rabat 7% na akcesoria |
| R3 | Zakup co najmniej 3 sztuk tego samego monitora | Rabat 10% na te monitory |
| R4 | Wartość koszyka powyżej 8000 zł | Dodatkowy rabat 3% |
| R5 | Zakup co najmniej 2 drukarek | Darmowa dostawa |
| R6 | Konflikt między R1 i R2 | Zostaje korzystniejsza promocja |

## Konflikt między regułami

Reguły R1 i R2 należą do tej samej grupy wykluczających się promocji. Oznacza to, że jeżeli oba warunki zostaną spełnione, system nie nalicza obu rabatów jednocześnie.

Przykład:

- w koszyku jest komputer,
- monitor,
- klawiatura,
- mysz.

Wtedy pasuje zarówno reguła R1, jak i R2. Silnik porównuje wartość rabatów i zostawia tę promocję, która daje większą korzyść. Informacja o odrzuconej regule jest zapisywana w logu jako R6.

## Technologie

Projekt korzysta z następujących technologii:

- Python,
- Flask,
- Flask-SQLAlchemy,
- SQLAlchemy,
- SQLite,
- HTML,
- CSS,
- Bootstrap 5,
- Jinja2.

## Struktura projektu

```text
projekt-system-regulowy-sklep-komputerowy-main/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── rules/
│   │   ├── base.py
│   │   ├── engine.py
│   │   └── promotions.py
│   ├── services/
│   │   ├── cart_service.py
│   │   └── pricing_service.py
│   ├── static/
│   │   └── styles.css
│   └── templates/
│       ├── base.html
│       ├── cart.html
│       ├── products.html
│       └── summary.html
├── config.py
├── requirements.txt
├── run.py
└── instance/
    └── shop.db
```

## Opis najważniejszych plików

### `run.py`

Plik startowy aplikacji. Tworzy aplikację Flask przez funkcję `create_app()` i uruchamia serwer w trybie debugowania.

### `config.py`

Zawiera konfigurację aplikacji, między innymi:

- klucz sesji `SECRET_KEY`,
- ścieżkę do bazy danych SQLite,
- wyłączenie śledzenia modyfikacji SQLAlchemy.

Domyślna baza danych znajduje się w katalogu `instance/shop.db`.

### `app/__init__.py`

Tworzy i konfiguruje aplikację Flask. W tym pliku dzieje się kilka ważnych rzeczy:

- inicjalizacja SQLAlchemy,
- utworzenie katalogu `instance`, jeżeli nie istnieje,
- utworzenie tabel w bazie danych,
- dodanie przykładowych produktów, jeżeli baza jest pusta,
- rejestracja filtrów szablonów,
- rejestracja tras aplikacji.

### `app/models.py`

Definiuje modele bazy danych:

- `Product` — produkt w sklepie,
- `Cart` — zapisany koszyk po analizie,
- `CartItem` — pozycja koszyka,
- `PromotionResult` — naliczona promocja,
- `RuleLog` — log działania pojedynczej reguły.

Dzięki temu aplikacja może zapisać nie tylko końcową kwotę, ale też historię tego, które reguły zostały spełnione, a które nie.

### `app/routes.py`

Zawiera główne trasy aplikacji:

- `/` — przekierowanie do katalogu produktów,
- `/products` — lista produktów,
- `/cart` — widok koszyka,
- `/cart/add/<id>` — dodanie produktu do koszyka,
- `/cart/update` — aktualizacja ilości,
- `/cart/remove/<id>` — usunięcie produktu,
- `/cart/clear` — wyczyszczenie koszyka,
- `/cart/analyze` — uruchomienie analizy promocji,
- `/summary/<id>` — podsumowanie zapisanego koszyka.

### `app/services/cart_service.py`

Odpowiada za obsługę koszyka. Koszyk jest przechowywany w sesji Flask jako słownik, gdzie kluczem jest identyfikator produktu, a wartością liczba sztuk.

Ten plik odpowiada za:

- pobieranie koszyka z sesji,
- zapisywanie koszyka do sesji,
- dodawanie produktu,
- usuwanie produktu,
- aktualizację ilości,
- liczenie wartości koszyka,
- liczenie liczby produktów w koszyku.

### `app/services/pricing_service.py`

Łączy koszyk z silnikiem regułowym. Ten plik:

- pobiera aktualne produkty z koszyka,
- tworzy obiekt faktów,
- uruchamia silnik reguł,
- zapisuje wynik analizy do bazy danych,
- zapisuje naliczone promocje i logi reguł.

### `app/rules/base.py`

Zawiera podstawowe klasy silnika regułowego:

- `Facts` — dane wejściowe dla reguł, czyli fakty o koszyku,
- `RuleResult` — wynik działania reguł, rabaty, dostawa i logi,
- `Rule` — pojedyncza reguła z warunkiem i akcją,
- `RuleLogEntry` — wpis informujący, czy reguła została spełniona.

To tutaj znajduje się również mechanizm rozwiązywania konfliktów między promocjami.

### `app/rules/engine.py`

Prosty silnik regułowy. Sortuje reguły według priorytetu, wykonuje je po kolei, a na końcu rozwiązuje konflikty między promocjami.

### `app/rules/promotions.py`

Zawiera konkretne reguły promocji. Każda reguła składa się z dwóch części:

- warunku, czyli sprawdzenia, czy promocja pasuje do koszyka,
- akcji, czyli naliczenia rabatu albo ustawienia darmowej dostawy.

Przykład: reguła R1 najpierw sprawdza, czy w koszyku jest komputer i monitor, a potem dodaje rabat 5%.

## Baza danych

Projekt używa SQLite. Baza znajduje się w pliku:

```text
instance/shop.db
```

Aplikacja sama tworzy tabele przy starcie, jeżeli jeszcze ich nie ma. Jeżeli tabela produktów jest pusta, aplikacja automatycznie dodaje przykładowe produkty komputerowe.

Przykładowe produkty to między innymi:

- komputery Lenovo i MSI,
- monitory Dell i LG,
- klawiatury Keychron i Logitech,
- myszy Logitech i Razer,
- drukarki HP i Brother.

## Jak uruchomić projekt

Najpierw utwórz środowisko wirtualne:

```bash
python3 -m venv .venv
```

Aktywuj środowisko:

```bash
source .venv/bin/activate
```

Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

Uruchom aplikację:

```bash
python run.py
```

Po uruchomieniu aplikacja powinna być dostępna pod adresem:

```text
http://127.0.0.1:5000
```

## Jak przetestować działanie reguł

### Test reguły R1

Dodaj do koszyka:

- jeden komputer,
- jeden monitor.

Efekt: system powinien naliczyć 5% rabatu na cały koszyk.

### Test reguły R2

Dodaj do koszyka:

- jeden komputer,
- jedną klawiaturę,
- jedną mysz.

Efekt: system powinien naliczyć 7% rabatu na akcesoria.

### Test reguły R3

Dodaj do koszyka:

- 3 sztuki tego samego monitora.

Efekt: system powinien naliczyć 10% rabatu na te monitory.

### Test reguły R4

Dodaj produkty za więcej niż 8000 zł.

Efekt: system powinien naliczyć dodatkowy rabat 3%.

### Test reguły R5

Dodaj do koszyka:

- 2 drukarki.

Efekt: koszt dostawy powinien wynosić 0 zł.

### Test reguły R6

Dodaj do koszyka:

- komputer,
- monitor,
- klawiaturę,
- mysz.

Efekt: system wykryje konflikt między R1 i R2, porówna rabaty i zostawi korzystniejszą promocję.

## Co widać w podsumowaniu

Po analizie promocji użytkownik trafia na stronę podsumowania. Widzi tam:

- produkty znajdujące się w koszyku,
- cenę przed rabatami,
- łączną wartość rabatów,
- koszt dostawy,
- końcową kwotę do zapłaty,
- listę aktywnych promocji,
- log działania silnika reguł.

Log jest ważny, bo pokazuje, dlaczego dana promocja została albo nie została naliczona. Dzięki temu projekt nie działa jak czarna skrzynka.

## Najważniejsza idea projektu

Najważniejsza idea projektu polega na oddzieleniu reguł biznesowych od zwykłej obsługi sklepu. Trasy Flask odpowiadają za strony i formularze, serwisy odpowiadają za koszyk oraz zapis danych, a katalog `rules` odpowiada za logikę promocji.

Dzięki temu można łatwo dodać kolejną regułę, na przykład:

- rabat dla konkretnej marki,
- rabat weekendowy,
- darmową dostawę od określonej kwoty,
- promocję na zestaw gamingowy,
- promocję dla produktów z jednej kategorii.

Wystarczy dodać nowy warunek, nową akcję i dopisać regułę w `build_rules()`.

## Ograniczenia projektu

Projekt jest wersją demonstracyjną, dlatego nie zawiera:

- logowania użytkowników,
- panelu administratora,
- płatności online,
- prawdziwego procesu składania zamówienia,
- magazynu i stanów produktów,
- testów jednostkowych.

Mimo tego dobrze pokazuje główny temat projektu, czyli działanie systemu regułowego w sklepie komputerowym.

## Podsumowanie

Projekt pokazuje, jak można zbudować prosty sklep internetowy, w którym decyzje o promocjach są podejmowane przez osobny silnik regułowy. Użytkownik dodaje produkty do koszyka, a system sprawdza zestaw warunków, nalicza rabaty, rozwiązuje konflikty i zapisuje wynik w bazie danych.

To czytelny przykład zastosowania reguł biznesowych w praktycznej aplikacji webowej.
