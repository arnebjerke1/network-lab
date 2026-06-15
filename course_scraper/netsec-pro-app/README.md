# NetSec-Pro Study

Dette er en mobilvennlig PWA for å øve til Palo Alto Networks **NetSec-Pro** på telefon.

## Slik åpner du appen på Samsung / Android

1. Åpne `index.html` i denne mappen via en nettadresse (for eksempel GitHub Pages senere) eller en lokal enkel webserver.
2. Åpne siden i **Chrome** på telefonen.
3. Trykk **⋮** øverst til høyre.
4. Velg **Legg til på startskjerm** / **Add to Home screen**.
5. Start appen fra ikonet på startskjermen. Den åpner i egen app-visning.

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

## Senere på GitHub Pages

Denne mappen er laget slik at den også kan hostes direkte på **GitHub Pages** senere. Når du har en URL, åpner du bare den på telefonen og gjør samme **Legg til på startskjerm**-prosess.

## Innhold i denne byggingen

- Spørsmål slått sammen: **451**
- Fun facts slått sammen: **135**
- Fikset duplikate spørsmåls-ID-er: **1**
- Droppede/mangelfulle spørsmål: **0**
