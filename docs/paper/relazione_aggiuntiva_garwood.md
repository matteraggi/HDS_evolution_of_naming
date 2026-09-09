# Relazione aggiuntiva: applicazione dell'inference stress test di Roccetti (2026) a RQ2 e all'Event Study

## 1. Metodologia adottata

Roccetti (2026)¹ propone un test diagnostico per conteggi rari di eventi Poisson osservati su
denominatori enormi: nei nostri dati, le nascite di un nome in un dato anno (conteggio raro, n)
rispetto al totale delle nascite di quell'anno/sesso/paese (denominatore N, dell'ordine di 1-2
milioni per gli USA). In presenza di N così grandi, l'errore standard di Wald si restringe quasi a
zero indipendentemente dalla reale solidità del segnale, producendo p-value "ultra-significativi"
che riflettono la scala del database più che l'evidenza biologica/comportamentale sottostante.

Il rimedio proposto sostituisce l'errore standard di Wald con l'errore standard esatto di Poisson,
che dipende solo dal conteggio osservato n, e confronta la stima osservata con il limite inferiore
esatto dell'intervallo di confidenza di Garwood (1936) costruito sullo stesso n. L'indice risultante è:

Z_R(n) = ( n − ½·χ²(2n, α/2) ) / √n

dove χ²(2n, α/2) è il quantile α/2 della distribuzione chi-quadrato con 2n gradi di libertà
(α=0,05). Una proprietà algebrica notevole della formula è che il denominatore N si cancella
completamente: Z_R dipende solo dal conteggio grezzo n, non dalla popolazione totale. È proprio
questa cancellazione a rendere l'indice immune all'inflazione di significatività causata da un
denominatore enorme.

**Come interpretiamo l'indice in questa relazione.** Per costruzione, Z_R(n) cresce in modo
monotono e converge asintoticamente al valore normale standard 1,96 (quantile normale al 97,5%).
Lo utilizziamo coerentemente con la descrizione datane dallo stesso autore ("a standardized
descriptive index of structural distance"), come **indice continuo della distanza strutturale di
ciascuna stima dal proprio riferimento asintotico 1,96**. Valori di Z_R più vicini a 1,96 indicano
conteggi la cui stima è strutturalmente più solida (meno esposta all'illusione di precisione della
scala del database); valori più lontani segnalano conteggi la cui apparente robustezza statistica
poggia su una base numerica più esigua.

## 2. Applicazione a RQ2: le 17 storie di picco/crollo

Per ciascuno dei 13 salti positivi e delle 4 flessioni verificate, abbiamo calcolato Z_R sul
conteggio grezzo pre-evento e post-evento (baseline e picco), usando i conteggi reali incrociati
con `us_names_long.csv` / `istat_contanomi_full.csv`:

| nome | paese | anno | n_pre | n_post | Z_R (pre) | Z_R (post) |
|------|-------|------|-------|--------|-----------|------------|
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

**Lettura.** I casi con baseline pre-evento più esiguo (Karol n=2, Nakia n=7, Jaslene n=6, Chanel
n=8, Nevaeh n=8, Devante n=10) mostrano i valori di Z_R più distanti dal riferimento asintotico
sul lato "baseline" (1,24–1,65): sono cioè i conteggi la cui stima di partenza è strutturalmente
meno solida, coerentemente col fatto che i loro rapporti di crescita più spettacolari (es. Nevaeh
150×, Jaslene 100×, Karol 78×) nascono da un conteggio iniziale a singola/doppia cifra, in linea
con l'avvertenza già presente in tesi sul rischio di survivorship bias per i casi a bassa
numerosità. I conteggi post-evento sono quasi tutti molto più vicini al riferimento (1,84–1,96),
incluso quando il valore assoluto resta piccolo (Chanel n=63 → 1,838): l'evento, una volta
avvenuto, tende a essere misurato con una base numerica più solida anche quando è partito da un
baseline fragile. I quattro casi di flessione (Hillary, Kobe, Alexa, Erica) mostrano valori pre e
post entrambi ravvicinati al riferimento (1,91–1,94), partendo da conteggi già nell'ordine delle
centinaia/migliaia.

## 3. Applicazione all'Event Study confermativo (N=152)

Per ciascuno dei 152 eventi mediatici, Z_R è stato calcolato sulla somma dei conteggi grezzi nella
finestra post-evento (fino a 2 anni), la stessa finestra usata per il calcolo della frequenza
post-evento già riportato nella tesi:

| categoria | N eventi | Z_R minimo | mediana | Z_R massimo | mediana n_post |
|---|---|---|---|---|---|
| Cinema & Serie TV | 71 | 1,455 | 1,935 | 1,956 | 1.483 |
| Musica & Pop Culture | 46 | 0,975 | 1,929 | 1,955 | 956 |
| Sport | 35 | 1,375 | 1,932 | 1,953 | 1.200 |
| **Totale** | **152** | **0,975** | **1,932** | **1,956** | **1.200** |

Le otto storie strutturalmente più distanti dal riferimento asintotico (Z_R più basso, quelle il
cui impatto netto DiD in Tabella 18 poggia sul conteggio grezzo post-evento più esiguo):

| nome | categoria | paese | anno | n_pre | n_post | Z_R (post) |
|---|---|---|---|---|---|---|
| Celine | Musica & Pop Culture | IT | 2023 | 168 | 1 | 0,975 |
| Lautaro | Sport | IT | 2024 | 4 | 3 | 1,375 |
| Harry | Cinema & Serie TV | IT | 2001 | 3 | 4 | 1,455 |
| Nemo | Cinema & Serie TV | US | 2003 | 6 | 5 | 1,510 |
| Dwyane | Sport | US | 2006 | 10 | 8 | 1,607 |
| Andriy | Sport | IT | 2003 | 4 | 13 | 1,686 |
| Cher | Musica & Pop Culture | US | 1999 | 20 | 14 | 1,696 |
| Woody | Cinema & Serie TV | US | 2010 | 17 | 18 | 1,728 |

**Lettura.** La stragrande maggioranza dei 152 eventi (mediana Z_R=1,93 in tutte e tre le
categorie) poggia su conteggi post-evento vicini al riferimento asintotico, cioè strutturalmente
solidi. Una minoranza di code (meno di 10 eventi su 152) mostra conteggi post-evento a una cifra o
poco più, dove la distanza dal riferimento è maggiore: un'informazione complementare, non
contraddittoria, rispetto al test di Wilcoxon già riportato nella tesi: quest'ultimo valuta se
l'effetto (variazione percentuale rispetto ai controlli) è sistematico sull'insieme dei 152 eventi,
mentre Z_R valuta quanto il conteggio grezzo di ciascun singolo evento sia strutturalmente solido
come base per quella stima. Il caso "Celine, IT, 2023" (n_post=1) è quello più esposto in assoluto.

## 4. Sintesi

Su entrambi i sottoinsiemi (RQ2 e Event Study), l'indice di distanza strutturale conferma un
quadro coerente con quanto già discusso nella tesi in termini di limiti dei casi a bassa numerosità:
i conteggi con base numerica più esigua (singola/doppia cifra) sono sistematicamente quelli
strutturalmente più distanti dal riferimento asintotico, mentre la stragrande maggioranza dei casi
(inclusi quelli con rapporti di crescita percentualmente più eclatanti) poggia su una base
numerica sufficientemente solida da collocarsi vicino al riferimento. Questo rafforza, con una
misura indipendente dal denominatore del database, un limite già dichiarato nella tesi (il rischio
di survivorship bias sui casi a bassa numerosità), individuando puntualmente i candidati più
esposti a quel rischio.

## 5. Contributi

- **Matteo Raggi:** la direzione "da evento a nome" dell'individuazione dei picchi/crolli per
  RQ2 (partendo dagli eventi mediatici noti per verificarne l'impatto sui nomi) e la relativa
  organizzazione per settore (Cinema & Serie TV, Musica & Pop Culture, Sport) dell'Event Study,
  l'intera RQ3, e la maggior parte della stesura del testo della tesi.
- **Elia Friberg:** RQ1, la direzione "da nome a evento" dell'individuazione dei picchi/crolli
  per RQ2 (partendo dalle anomalie nei dati dei nomi per risalire alla causa mediatica),
  l'applicazione dell'inference stress test di Roccetti (2026) descritta in questa relazione
  (Sezioni 1-4) con relativa validazione numerica indipendente, e la parte restante della
  stesura del testo della tesi.

---

¹ Roccetti, M. (2026). *An AI for diseases or a sick AI? The epistemological pathology of big data
overload and the loss of statistical significance.* Frontiers in Artificial Intelligence, 9:1961525.
doi: 10.3389/frai.2026.1961525 (Author's Proof).
