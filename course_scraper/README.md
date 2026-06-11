# PCNSP Course Scraper & Quiz Generator

Automatisk innsamling av spørsmål fra Palo Alto Networks PCNSP-kurset og generering av en interaktiv HTML-quiz.

---

## Mappestruktur

```
course_scraper/
├── scraper.py          # Nettleser-agent som samler spørsmål fra kurset
├── quiz_generator.py   # Genererer HTML-quiz fra innsamlede spørsmål
├── requirements.txt    # Python-avhengigheter
├── questions.json      # Genereres av scraper.py (ikke inkludert i repo)
└── quiz.html           # Genereres av quiz_generator.py (ikke inkludert i repo)
```

---

## Oppsett

### 1. Installer avhengigheter

```bash
cd course_scraper
pip install -r requirements.txt
playwright install chromium
```

### 2. Sett inn påloggingsopplysninger

```bash
export PALO_EMAIL="din@epost.com"
export PALO_PASSWORD="ditt-passord"
```

> **Windows (PowerShell):**
> ```powershell
> $env:PALO_EMAIL="din@epost.com"
> $env:PALO_PASSWORD="ditt-passord"
> ```

---

## Bruk

### Steg 1 – Kjør scraper

```bash
python scraper.py
```

- Åpner en synlig Chromium-nettleser
- Logger automatisk inn på `learn.paloaltonetworks.com`
- Navigerer gjennom hele PCNSP-læringsbanen
- Samler alle spørsmål og riktige svar
- Lagrer resultatet til `questions.json`

**Kjør uten synlig nettleser (headless):**
```bash
HEADLESS=true python scraper.py
```

**Logg inn manuelt** (om automatisk innlogging feiler):  
Start scriptet uten å sette `PALO_EMAIL`/`PALO_PASSWORD` – nettleseren åpnes og du logger inn selv, deretter trykker du Enter i terminalen.

---

### Steg 2 – Generer quiz

```bash
python quiz_generator.py
```

Genererer `quiz.html` – åpne filen direkte i nettleseren din:

```bash
# macOS
open quiz.html

# Linux
xdg-open quiz.html

# Windows
start quiz.html
```

---

## Quiz-funksjoner

- **Flervalg støttes** (ett eller flere riktige svar)
- Velg svar og trykk **Sjekk svar**
- Riktige svar vises i **grønt** ✓
- Feil valgte svar vises i **rødt** ✗
- Fremdriftslinje øverst
- Sluttresultat med prosentpoeng
- "Ta quizen på nytt"-knapp

---

## Merk

- Scriptet er avhengig av HTML-strukturen til læringsplattformen. Oppdateringer på plattformen kan kreve justering av selektorer i `scraper.py`.
- Spørsmål og svar tilhører Palo Alto Networks – kun til personlig studiebruk.
