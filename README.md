# OpenFGA-OTel

## Środowiska Udostępniania Usług: OpenFGA - OTel

**Autorzy:** Basia Wojtarowicz, Maciej Kopeć, Mateusz Knap, Tomasz Policht  
**Data:** Maj 2025

## Wprowadzenie

Celem naszego projektu jest stworzenie dema, które zaprezentuje możliwości i cechy dwóch technologii: **OpenFGA** – systemu zarządzania autoryzacją opartego na modelu RBAC/ABAC, oraz **OpenTelemetry (Otel)** – standardu służącego do zbierania i eksportowania danych obserwowalności (tracing, metrics, logs).

Scenariusz projektu opiera się na _..._, co pozwala na przedstawienie rzeczywistego zastosowania wybranych technologii. Projekt nie powiela żadnego istniejącego w internecie rozwiązania / Projekt stanowi istotne rozszerzenie przykładu z _..._.


## Podstawy teoretyczne i stos technologiczny

### OpenFGA

**OpenFGA (Fine-Grained Authorization)** to otwartoźródłowa implementacja systemu autoryzacji, opracowana przez firmę Auth0. OpenFGA opiera się na koncepcji zarządzania dostępem na poziomie relacyjnym i umożliwia definiowanie złożonych polityk uprawnień z dużą dokładnością (fine-grained access control), przy wsparciu modeli takich jak **RBAC** (Role-Based Access Control) oraz **ABAC** (Attribute-Based Access Control).

**Kluczowe cechy OpenFGA:**

- Definiowanie modeli uprawnień w formie deklaratywnej,
- Obsługa dynamicznych ról, grup i dziedziczenia uprawnień,
- Skalowalność dzięki optymalizacjom pod kątem dużych systemów,
- Interfejsy API umożliwiające integrację z dowolnym backendem.

### OpenTelemetry (Otel)

**OpenTelemetry** to zestaw narzędzi, bibliotek oraz standardów służących do zapewnienia obserwowalności systemów rozproszonych. Projekt rozwijany przez **CNCF** (Cloud Native Computing Foundation) powstał z połączenia wcześniejszych inicjatyw **OpenTracing** i **OpenCensus**. OpenTelemetry udostępnia ujednolicony interfejs do zbierania trzech głównych typów danych telemetrycznych:

- **Trace’y** – śledzenie przepływu zapytań przez wiele komponentów systemu,
- **Metryki** – pomiary dotyczące wydajności i stanu systemu,
- **Logi** – ustandaryzowane dzienniki zdarzeń.

Dzięki modularnej budowie Otel może być łatwo integrowany z aplikacjami mikroserwisowymi oraz eksportować dane do narzędzi takich jak **Jaeger**, **Prometheus**, **Grafana** czy **AWS CloudWatch**.


## Zarys demo

Pokażemy, jak aplikacja bankowa/e-commerce korzysta z OpenFGA do autoryzacji i za pomocą OpenTelemetry możemy obserwować kto i na jakiej podstawie uzyskał do niej dostęp lub nie.

### Struktura

1. **Aplikacja testowa** (np. skrypt w Pythonie lub Go)
   - Wysyła zapytania do OpenFGA (czy `user:X` ma dostęp do `resource:Y`),
   - W zależności od odpowiedzi: wyświetla _"Access granted"_ / _"Access denied"_,
   - Dla każdego takiego zapytania — generuje trace/span w OpenTelemetry.

2. **OpenFGA**
   - Uruchomiony lokalnie (np. z repo sample-stores),
   - Załadowany model (z kontami bankowymi),
   - Wysłane tuple z demo (np. `"user:alice"` jest customer).

3. **OpenTelemetry**
   - Zainicjalizowane SDK (np. w Pythonie),
   - Export danych do Jaegera.

4. **Wizualna prezentacja efektu**
   - W Grafanie lub Prometheusie,
   - Prometheus zbiera dane z endpointu `/metrics` naszej aplikacji,
   - Dzięki temu, w Grafanie możemy zobaczyć:
     - ile zapytań zostało wykonanych,
     - jak wiele z nich zakończyło się sukcesem lub odmową,
     - czas odpowiedzi systemu,
     - ewentualne błędy lub przeciążenia,
     - kto i kiedy próbował uzyskać dostęp do jakiego zasobu.


## Podział ról w zespole

- *(Sekcja do uzupełnienia)*
