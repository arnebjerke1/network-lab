# NetSec-Pro Study

Dette er en mobilvennlig PWA for å øve til Palo Alto Networks **NetSec-Pro** på telefon.

## 📲 Installer som Android-app

> **Direkte link:** [https://arnebjerke1.github.io/network-lab/](https://arnebjerke1.github.io/network-lab/)

### Steg-for-steg på Android (Chrome)

1. Åpne linken over i **Chrome** på Android-telefonen din.
2. Chrome viser automatisk en banner nederst: **"Legg til NetSec-Pro på startskjermen"** – trykk på den.  
   *(Hvis banneren ikke dukker opp: trykk **⋮** øverst til høyre → **Legg til på startskjerm** / **Add to Home screen**.)*
3. Bekreft med **Legg til** / **Add**.
4. Appen vises nå som et eget ikon på startskjermen og åpner **uten** nettleser-UI – akkurat som en vanlig app.

> Appen lastes ned lokalt via service worker og **fungerer offline** etter første åpning.

## Offline og lagring

- Fremdrift, poeng, streak og review-liste lagres i **nettleserens localStorage** på enheten.
- Etter første innlasting lagres appens filer lokalt via service worker, så den fungerer **offline**.
- Hvis du lukker Chrome helt, får du fortsatt en tydelig **Resume**-knapp når du åpner appen igjen.

## Seksjoner og review

- **Sections** viser domenene i rekkefølgen **D1 → D6**.
- For hvert domene kan du starte en runde på **5**, **10** eller **alle** spørsmålene i akkurat den seksjonen.
- **Review** samler spørsmål du svarte feil på. De blir liggende der til du svarer riktig på dem igjen, eller til du trykker **Clear review list**.
- Statistikksiden viser også hvor mange spørsmål som fortsatt står til review.

## Om domeneinndelingen

Kildematerialet er tagget som **D1–D6** for å gjøre øvingen mer finfordelt:

- D1: Network Security Fundamentals
- D2: NGFW & SASE Solution Functionality
- D3: Platform Solutions, Services & Tools
- D4: NGFW & SASE Maintenance & Configuration
- D5: Infrastructure Management & CDSS
- D6: Connectivity & Security

Den offisielle blueprinten er nyere og mer komprimert, men appen beholder D5 og D6 som egne studiedeler fordi spørsmålsbanken allerede bruker disse taggene.

## CCNP Security SCOR (Cisco)

Velg **CCNP SCOR · Cisco** øverst i appen for å bytte til spørsmålene for Cisco 350-701. NetSec-Pro- og SCOR-fremdrift lagres separat, så den eksisterende Palo Alto-statistikken og review-listen beholdes.

SCOR-banken inneholder **703 spørsmål** fra PDF-en:

- **566** single-choice
- **111** multiple-choice (med krav om riktig antall valg)
- **26** drag-and-drop

Du kan starte en tilfeldig runde på 5 eller 10 spørsmål, ta hele banken, øve per seksjon, fortsette en lagret runde, gå gjennom feilsvarte spørsmål og se statistikk. Drag-and-drop kan brukes med dra/slipp eller ved å trykke på et element og deretter en kategori. Bildene skilles også i dataene: for eksempel er `page-011-01.png` oppgaven og `page-011-02.png` fasiten. Appen viser oppgavebildet først og fasitbildet etter at du har svart. Oppgaver der bildet ikke kunne tolkes sikkert er merket for gjennomgang og kan hoppes over til review.

Alle spørsmål med teksten «Refer to the exhibit» viser bildeutdrag fra PDF-en i appen; bildene følger også med i offline-cachen.

SCOR-fremdriften bruker localStorage-nøkkelen `ccnp_scor_study_v1`, uavhengig av NetSec-Pro. Etter første innlasting fungerer SCOR-banken og tilhørende bilder offline.

### Oppdatering av SCOR-spørsmålene

Fra rotmappen til repoet kan parseren kjøres på nytt slik:

```sh
python course_scraper/scor_parser.py
```

Parseren leser `course_scraper/920062385-SCOR-PDF.pdf`, skriver `netsec-pro-app/scor-questions.js` og bildeutdrag til `netsec-pro-app/scor-exhibits/`, og oppdaterer `course_scraper/scor_parse_report.md`. Parseravhengigheten `pypdf` er oppført i `course_scraper/requirements.txt`.

## Innhold i denne byggingen

- Spørsmål slått sammen: **451**
- Fun facts slått sammen: **135**
- Fikset duplikate spørsmåls-ID-er: **1**
- Droppede/mangelfulle spørsmål: **0**
