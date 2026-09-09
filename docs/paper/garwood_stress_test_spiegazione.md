# Il test di Garwood/Roccetti applicato a RQ2 — spiegazione e risultati

Questo documento spiega cos'è il test proposto dal prof (Roccetti, "An AI for diseases or a sick
AI?", *Frontiers in Artificial Intelligence*, 2026, doi: 10.3389/frai.2026.1961525 — al momento
un *Author's Proof* non ancora pubblicato definitivamente), perché si applica ai nostri dati, cosa
abbiamo scoperto implementandolo, e i risultati completi. **Non è ancora inserito nel paper**:
decidete voi se/come usarlo dopo aver letto questo documento.

Script: `src/scripts/19_garwood_stress_test.py`. Output:
`dataset/processed/garwood_stress_test_spikes.csv`,
`dataset/processed/garwood_stress_test_event_study.csv`,
`docs/paper/tables/table21_garwood_stress_test.csv`.

## 1. Il problema che il test vuole risolvere

Il paper del prof parte da un'osservazione semplice: quando un dataset è enorme (milioni di
record) ma l'evento che si sta misurando è raro, il calcolo standard dell'errore standard di Wald

```
SE = sqrt( p(1-p) / N )
```

si restringe quasi a zero solo perché N è enorme — non perché la stima sia davvero precisa. Il
risultato è un p-value "ultra-significativo" che riflette la scala del database, non la solidità
del segnale biologico. Il rimedio proposto: invece di misurare l'incertezza con la formula di Wald
(che assume una distribuzione Normale), la si misura con la formula esatta di Poisson — che dipende
**solo dal numero di eventi osservati n**, non dal denominatore N — e si confronta la stima
osservata non con zero, ma con il **limite inferiore esatto dell'intervallo di confidenza di
Garwood** (Garwood, 1936) costruito sullo stesso conteggio n. Se lo scarto tra stima e limite
inferiore, misurato in errori standard di Poisson, non supera 1,96, il segnale "brillante" prodotto
dal dataset enorme si rivela strutturalmente fragile.

## 2. Perché è rilevante per il nostro paper

Le nostre "storie di picco/crollo" (RQ2) e l'Event Study condividono esattamente la stessa
struttura del problema che il prof attacca: un **conteggio raro** (le nascite di un nome in un
anno, n) su un **denominatore enorme** (le nascite totali quell'anno/sesso/paese, N — dell'ordine
di 1-2 milioni per gli USA). Attualmente, i 17 casi picco/crollo verificati non hanno **nessun test
di significatività formale** — solo una soglia-rapporto grezza più verifica di plausibilità web e
concordanza geografica. È il punto più esposto del paper alla critica "è solo un artefatto di scala
enorme che fa sembrare un rumore statistico un segnale reale?". Applicare questo test lì colma
esattamente quel buco.

## 3. La formula, e il fatto algebrico chiave

Dato un conteggio osservato n (eventi) su un denominatore T (popolazione o persona-anni), il paper
del prof dimostra che il denominatore **si cancella completamente** nella formula del punteggio Z
(la loro Eq. 5-6):

```
Z(n) = ( n − χ²(0,025; 2n)/2 ) / sqrt(n)
```

dove χ²(0,025; 2n) è il quantile 2,5% della distribuzione chi-quadrato con 2n gradi di libertà. **Z
dipende solo da n**, non da N/T — è esattamente perché il denominatore enorme "sparisce" dal calcolo
che il test smaschera l'illusione di precisione. Lo abbiamo implementato con
`scipy.stats.chi2.ppf(0.025, df=2*n)`.

## 4. Due scoperte fatte implementandolo (importanti prima di usarlo)

### 4.1 — Il paper del prof sembra avere un errore aritmetico nella sua Tabella 2

Abbiamo verificato i quantili chi-quadrato riportati nella Tabella 2 del paper contro il calcolo
esatto (validato anche con l'approssimazione indipendente di Wilson-Hilferty, che concorda con
`scipy` al terzo decimale):

| n   | df=2n | quantile riportato nel paper | quantile esatto (scipy) |
|-----|-------|-------------------------------|--------------------------|
| 23  | 46    | 29,160                        | 29,160 ✓ (coincide)     |
| 206 | 412   | 360,480                       | 357,656 (differisce)    |
| 463 | 926   | 841,691                       | 843,563 (differisce)    |

Per il caso n=23 il valore riportato è corretto; per n=206 e n=463 no. Non è un dettaglio
cosmetico: nel loro esempio più citato (coorte vaccinata Vitiligo, n=463), l'errore **abbassa
artificialmente il limite inferiore di Garwood** quel tanto che basta a spingere il loro Z-score
riportato (1,961) appena sopra la soglia 1,96 — con il quantile corretto, il vero Z è 1,916, sotto
soglia. Non cambia la loro conclusione generale (in entrambi i casi il segnale è "al limite"), ma è
un'inconsistenza interna che vale la pena notare: è un *Author's Proof* con 15 query del
typesetter ancora irrisolte, quindi plausibilmente un bug non ancora corretto in fase di revisione.
**Per i nostri calcoli abbiamo sempre usato il quantile esatto**, non quello (apparentemente errato)
del paper.

### 4.2 — La soglia "Z ≥ 1,96" non è mai raggiungibile per costruzione matematica

Con il calcolo esatto, Z(n) è **strettamente crescente in n ma converge a 1,95996 dal basso, senza
mai raggiungerlo**, per qualunque n finito. È una conseguenza dell'asimmetria della distribuzione
di Poisson: il limite inferiore esatto di Garwood è sempre più conservativo (cioè più vicino a n) di
quanto lo sarebbe il limite Wald simmetrico, ma mai abbastanza da far collassare la formula
sull'asintoto normale. Verificato numericamente:

| n           | Z(n)   |
|-------------|--------|
| 23          | 1,7557 |
| 463         | 1,9156 |
| 1.000       | 1,9298 |
| 42.366      | 1,9554 |
| 1.000.000   | 1,9590 |
| 100.000.000 | 1,9599 |

Anche un conteggio-monstre come 100 milioni non arriva a 1,9600 esatto. **Conseguenza pratica**: un
criterio binario "supera 1,96 sì/no" applicato con il calcolo corretto **non sarà mai soddisfatto**
da nessun caso reale — non perché il segnale sia sempre fragile, ma perché la soglia stessa è un
asintoto irraggiungibile. È più corretto trattare Z(n) come un **indice continuo di distanza
strutturale dall'asintoto**, non come un test pass/fail. (Il paper del prof stesso, in prosa, la
descrive più cautamente come "hovers near/close to 1.96" — la formulazione binaria compare solo
nella soglia dichiarata nel testo, non riflette bene ciò che la matematica del metodo permette.)

## 5. Risultati — 17 casi picco/crollo (RQ2)

Per ciascuno dei 13 salti positivi e 4 crolli verificati nel paper (Tabelle "positive_spikes" /
"negative_spikes"), Z calcolato sul conteggio pre-evento (baseline) e sul conteggio post-evento,
usando i conteggi grezzi reali (incrociati con `us_names_long.csv` / `istat_contanomi_full.csv`,
non solo i numeri arrotondati riportati nel testo del paper):

| nome | paese | anno | n_pre | n_post | Z_pre | Z_post |
|------|-------|------|-------|--------|-------|--------|
| Shirley | USA | 1935 | 14.476 | 42.366 | 1,952 | 1,955 |
| Tammy | USA | 1957 | 193 | 4.365 | 1,891 | 1,946 |
| Nakia | USA | 1974 | 7 | 1.135 | 1,582 | 1,932 |
| Jaime | USA | 1976 | 259 | 7.838 | 1,900 | 1,949 |
| Devante | USA | 1991 | 10 | 131 | 1,646 | 1,876 |
| Mariah | USA | 1990 | 423 | 1.103 | 1,914 | 1,931 |
| Nevaeh | USA | 2001 | 8 | 1.199 | 1,607 | 1,932 |
| Jaslene | USA | 2007 | 6 | 501 | 1,551 | 1,917 |
| Karol | Italia | 2005 | 2 | 156 | 1,243 | 1,883 |
| Chanel | Italia | 2007 | 8 | 63 | 1,607 | 1,838 |
| Adele | Italia | 2012 | 449 | 1.075 | 1,915 | 1,931 |
| Elodie | Italia | 2017 | 13 | 135 | 1,686 | 1,877 |
| Soleil | Italia | 2022 | 98 | 474 | 1,863 | 1,916 |
| Hillary | USA | 1993 | 2.520 | 1.064 | 1,941 | 1,931 |
| Kobe | USA | 2004 | 1.392 | 625 | 1,934 | 1,922 |
| Alexa | USA | 2021 | 2.002 | 708 | 1,939 | 1,924 |
| Erica | Italia | 2002 | 863 | 416 | 1,928 | 1,913 |

**Lettura**: come atteso dal punto 4.2, nessuno raggiunge 1,96 esatto — ma il quadro relativo è
comunque informativo. I casi con il **baseline pre-evento più esiguo** (Karol n=2 → Z=1,24; Nakia
n=7 → Z=1,58; Nevaeh n=8 → Z=1,61; Chanel n=8 → Z=1,61; Jaslene n=6 → Z=1,55; Devante n=10 →
Z=1,65) sono quelli strutturalmente più lontani dall'asintoto sul lato "baseline" — cioè quelli in
cui il rapporto spettacolare (es. Nevaeh 150x, Jaslene 100x, Karol 78x) nasce da un conteggio di
partenza a singola/doppia cifra, per natura statisticamente meno stabile. I conteggi post-evento
sono quasi tutti molto più vicini all'asintoto (Z=1,83–1,96), inclusi quelli piccoli in termini
assoluti (Chanel n=63 → Z=1,84): il salto stesso, una volta avvenuto, è quasi sempre "misurato bene"
anche quando parte da un baseline fragile. Per i crolli, sia pre che post sono generalmente robusti
(Z=1,91–1,94), essendo partiti da conteggi già nell'ordine delle centinaia/migliaia.

## 6. Risultati — Event Study confermativo (N=152)

Per ciascuno dei 152 eventi mediatici, Z calcolato sulla somma dei conteggi grezzi nella finestra
post-evento (fino a 2 anni, la stessa finestra usata per calcolare `post_freq_per_100k` negli script
`07b/07d/07f_event_study_*.py`, ma qui sommando i conteggi invece di mediare le frequenze):

| categoria | N eventi | Z_post minimo | mediana | Z_post massimo | mediana n_post |
|---|---|---|---|---|---|
| Cinema & Serie TV | 71 | 1,455 | 1,935 | 1,956 | 1.483 |
| Musica & Pop Culture | 46 | 0,975 | 1,929 | 1,955 | 956 |
| Sport | 35 | 1,375 | 1,932 | 1,953 | 1.200 |
| **TOTALE** | **152** | **0,975** | **1,932** | **1,956** | **1.200** |

Le 8 storie più fragili in assoluto (Z_post più basso — cioè quelle il cui "impatto netto DiD"
riportato in Tabella 18 poggia sul conteggio grezzo post-evento più esiguo):

| nome | categoria | paese | anno | n_pre (somma 3a) | n_post (somma 2a) | Z_post |
|---|---|---|---|---|---|---|
| Celine | Musica & Pop Culture | IT | 2023 | 168 | **1** | 0,975 |
| Lautaro | Sport | IT | 2024 | 4 | 3 | 1,375 |
| Harry | Cinema & Serie TV | IT | 2001 | 3 | 4 | 1,455 |
| Nemo | Cinema & Serie TV | US | 2003 | 6 | 5 | 1,510 |
| Dwyane | Sport | US | 2006 | 10 | 8 | 1,607 |
| Andriy | Sport | IT | 2003 | 4 | 13 | 1,686 |
| Cher | Musica & Pop Culture | US | 1999 | 20 | 14 | 1,696 |
| Woody | Cinema & Serie TV | US | 2010 | 17 | 18 | 1,728 |

Il caso "Celine, IT, 2023" con n_post=1 salta all'occhio e merita una verifica manuale prima di
qualunque uso in presentazione — probabilmente è un evento diverso dal "Celine Dion" citato nella
Sezione Risultati (quello ha una base molto più larga, si veda il confronto USA/Italia nel testo),
forse un nome poco frequente o un anno con dati sparsi. Vale la pena controllarlo nel dataset grezzo
prima di citare questo numero.

**Lettura d'insieme**: la stragrande maggioranza dei 152 eventi (mediana Z=1,93 in tutte e tre le
categorie) poggia su conteggi post-evento ragionevolmente solidi, vicini all'asintoto. Solo una
manciata di code (< 10 eventi su 152) ha conteggi post-evento a una cifra o poco più, dove la
misura è strutturalmente più fragile — un'informazione complementare, non contraddittoria, al test
di Wilcoxon già riportato: quel test valuta se l'*effetto* (variazione % rispetto ai controlli) è
sistematico sull'insieme dei 152 eventi; questo valuta se il *conteggio grezzo* di ciascun singolo
evento è abbastanza consistente da fidarsi della sua stima individuale.

## 7. Come potremmo usarlo nel paper (da decidere insieme)

Alcune opzioni, non mutuamente esclusive:

- **Nuovo controllo di robustezza nella Sezione "Validazione scientifica"** (in coda alla lista
  esistente): un paragrafo che applica il test di Roccetti (2026) ai 17 casi RQ2 e ai 152 eventi
  dell'Event Study, riportando l'indice come misura *continua* di distanza strutturale (non come
  pass/fail), con la tabella riassuntiva del punto 6 e magari la Tabella 21 completa in appendice.
- **Nota metodologica sul rischio di baseline esigui**: usare i risultati del punto 5 per rafforzare
  onestamente un limite già dichiarato nel paper (il rischio di survivorship bias sui casi a bassa
  numerosità, già menzionato per il controllo geografico) — i baseline pre-evento a singola cifra
  (Karol, Nakia, Jaslene, Chanel, Nevaeh) sono precisamente i candidati più esposti a questo rischio.
- **Citare la scoperta sulla Tabella 2 del prof** solo se contestualmente rilevante (es. se vi chiede
  perché avete usato `scipy.stats.chi2.ppf` invece di riprodurre esattamente i loro numeri) — non è
  necessario metterla nel paper, ma è bene che la sappiate per l'orale.

Fatemi sapere quale/i pezzi volete integrare e li scrivo direttamente nel `.tex`.
