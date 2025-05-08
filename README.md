# OpenFGA-OTel


\documentclass{article}

% Language setting
% Replace `english' with e.g. `spanish' to change the document language
\usepackage[polish]{babel}

% Set page size and margins
% Replace `letterpaper' with `a4paper' for UK/EU standard size
\usepackage[letterpaper,top=2cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=1.75cm]{geometry}

% Useful packages
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage[colorlinks=true, allcolors=blue]{hyperref}
\usepackage{hyphenat}
\hyphenation{po-lski}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc} 
\usepackage{listings}
\usepackage{graphicx}
\usepackage{subcaption}


\title{Środowiska Udostępniania Usług: OpenFGA - OTel}
\author{Basia Wojtarowicz, Maciej Kopeć, Mateusz Knap, Tomasz Policht}
\date{Maj 2025}

\begin{document}

\maketitle

\section{Wprowadzenie}

Celem naszego projektu jest stworzenie dema, które zaprezentuje możliwości i cechy dwóch technologii: \textbf{OpenFGA} – systemu zarządzania autoryzacją opartego na modelu RBAC/ABAC, oraz \textbf{OpenTelemetry (Otel)} – standardu służącego do zbierania i eksportowania danych obserwowalności (tracing, metrics, logs).

Scenariusz projektu opiera się na \textit{...}, co pozwala na przedstawienie rzeczywistego zastosowania wybranych technologii. Projekt nie powiela żadnego istniejącego w internecie rozwiązania / Projekt stanowi istotne rozszerzenie przykładu z \textit{...}.

\section{Podstawy teoretyczne i stos technologiczny}

\subsection{OpenFGA}

\textbf{OpenFGA (Fine-Grained Authorization)} to otwartoźródłowa implementacja systemu autoryzacji, opracowana przez firmę Auth0. OpenFGA opiera się na koncepcji zarządzania dostępem na poziomie relacyjnym i umożliwia definiowanie złożonych polityk uprawnień z dużą dokładnością (fine-grained access control), przy wsparciu modeli takich jak \textbf{RBAC} (Role-Based Access Control) oraz \textbf{ABAC} (Attribute-Based Access Control).

\noindent Kluczowe cechy OpenFGA:

\begin{itemize}
    \item Definiowanie modeli uprawnień w formie deklaratywnej,
    \item Obsługa dynamicznych ról, grup i dziedziczenia uprawnień,
    \item Skalowalność dzięki optymalizacjom pod kątem dużych systemów,
    \item Interfejsy API umożliwiające integrację z dowolnym backendem.
\end{itemize}

\subsection{OpenTelemetry (Otel)}

\textbf{OpenTelemetry} to zestaw narzędzi, bibliotek oraz standardów służących do zapewnienia obserwowalności systemów rozproszonych. Projekt rozwijany przez \textbf{CNCF} (Cloud Native Computing Foundation) powstał z połączenia wcześniejszych inicjatyw \textbf{OpenTracing} i \textbf{OpenCensus}. OpenTelemetry udostępnia ujednolicony interfejs do zbierania trzech głównych typów danych telemetrycznych:

\begin{itemize}
    \item \textbf{Trace’y} – śledzenie przepływu zapytań przez wiele komponentów systemu,
    \item \textbf{Metryki} – pomiary dotyczące wydajności i stanu systemu,
    \item \textbf{Logi} – ustandaryzowane dzienniki zdarzeń.
\end{itemize}

Dzięki modularnej budowie Otel może być łatwo integrowany z aplikacjami mikroserwisowymi oraz eksportować dane do narzędzi takich jak \textbf{Jaeger}, \textbf{Prometheus}, \textbf{Grafana} czy \textbf{AWS CloudWatch}.

\section{Zarys demo}
Pokażemy, jak aplikacja bankowa/e-commerce korzysta z OpenFGA do autoryzacji i za pomocą OpenTelemetry możemy obserwować kto i na jakiej podstawie uzyskał do niej dostęp lub nie.

\subsection{Struktura}
\begin{enumerate}
    \item Aplikacja testowa (np. skrypt w Pythonie lub Go)
    \begin{itemize}
        \item Wysyła zapytania do OpenFGA (czy user:X ma dostęp do resource:Y),
        \item W zależności od odpowiedzi: wyświetla "Access granted"/"Access denied",
        \item Dla każdego takiego zapytania — generuje trace/span w OpenTelemetry
    \end{itemize}
    \item OpenFGA
    \begin{itemize}
        \item Uruchomiony lokalnie (np. z repo sample-stores),
        \item Załadowany model (z kontami bankowymi),
        \item Wysłane tuple z demo (np. "user:alice" jest customer)
    \end{itemize}
    \item OpenTelemetry
    \begin{itemize}
        \item Zainicjalizowane SDK (np. w Pythonie),
        \item Export danych do Jaegera
    \end{itemize}
    \item Wizualna prezentacja efektu
    \begin{itemize}
        \item w Grafanie lub Prometheusie,
        \item Prometheus zbiera dane z endpointu /metrics naszej aplikacji,
        \item Dzięki temu, w Grafanie możemy zobaczyć: ile zapytań zostało wykonanych, jak wiele z nich zakończyło się sukcesem lub odmową,czas odpowiedzi systemu, ewentualne błędy lub przeciążenia, to i kiedy próbował uzyskać dostęp do jakiego zasobu.
        
    \end{itemize}
\end{enumerate}

\section{Podział ról w zespole}
\begin{itemize}
    \item 
\end{itemize}

\end{document}
