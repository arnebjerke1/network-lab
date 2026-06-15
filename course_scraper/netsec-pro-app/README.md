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

## Innhold i denne byggingen

- Spørsmål slått sammen: **451**
- Fun facts slått sammen: **135**
- Fikset duplikate spørsmåls-ID-er: **1**
- Droppede/mangelfulle spørsmål: **0**
