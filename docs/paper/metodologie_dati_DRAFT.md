# Metodologie e Dati (bozza — sezione a cura di Person A)

> Nota per la revisione: questa è una bozza di lavoro, non il testo finale del paper. **Riscritta il
> 2026-08-16** dopo un cambiamento sostanziale nella fonte dati italiana (si veda §1 e `PROJECT_LOG.md`
> per la cronologia completa): è stato individuato un servizio web reale dietro lo strumento ISTAT
> "contanomi", non documentato pubblicamente ma funzionante, che ha sostituito la raccolta manuale da
> PDF come fonte primaria. Questo ha risolto i due limiti principali della versione precedente di questa
> bozza (finestra ristretta a 2006-2024, dipendenza da una fonte secondaria per 15 anni su 19) ma ne ha
> introdotto uno nuovo, diverso e più tracciabile: una profondità di copertura variabile per anno, la cui
> non-distorsione sulla metrica primaria è stata dimostrata empiricamente (§4). Sono state inoltre
> aggiunte le sezioni su rilevamento degli spike (RQ2) e convergenza USA-Italia, assenti nella versione
> precedente. Lunghezza attuale: ~2600 parole.

## 1. Fonti dei dati

Per rispondere alle domande di ricerca è stato necessario ricostruire due serie storiche di nomi alla
nascita, una per gli Stati Uniti e una per l'Italia, che si sono rivelate profondamente asimmetriche per
struttura e accessibilità — un'asimmetria che, come discusso nella sezione sul Fattore Umano, non è un
semplice ostacolo tecnico ma un dato interessante di per sé.

**Stati Uniti.** La fonte primaria è la *Social Security Administration* (SSA), che dal 1997 pubblica
annualmente l'archivio "Baby Names from Social Security Card Applications"
(`https://www.ssa.gov/oact/babynames/names.zip`), rilasciato con licenza CC0/dominio pubblico. L'archivio
contiene un file per ogni anno dal 1880 al 2025 (146 file), con record `nome,sesso,conteggio` per ogni
combinazione osservata. L'unico limite dichiarato è una soglia di soppressione statistica: i nomi
attribuiti a meno di 5 nascite in un dato anno/stato/sesso non vengono riportati, per tutelare la
riservatezza dei nuclei familiari più piccoli. L'intero archivio nazionale è stato scaricato ed elaborato
per intero: dopo la pulizia, la tabella lunga risultante conta oltre 2,18 milioni di combinazioni
nome/anno/sesso.

**Italia.** Il piano di ricerca iniziale prevedeva l'acquisizione manuale dei dati italiani, poiché
ISTAT non pubblica una tabella cumulativa bulk nome × anno × sesso × conteggio attraverso i suoi canali
ufficiali (il portale Open Data / High Value Datasets è stato verificato direttamente e non contiene
alcun dataset a livello di nome — le voci "fertilità" e "mortalità" presenti sono in realtà lo stesso
indicatore demografico aggregato, senza alcuna informazione sui nomi). Questa raccolta manuale è stata
effettivamente svolta in una prima fase (2004 e 2006-2024, da 14 PDF ISTAT scaricati direttamente più
nomix.it come fonte secondaria per gli anni non altrimenti reperibili — si veda
`data/raw/istat/COLLECTION_NOTES.md` per il dettaglio completo, conservato come traccia di corroborazione
anche se non più fonte primaria).

Analizzando il codice JavaScript dello strumento interattivo "contanomi"
(`istat.it/dati/calcolatori/contanomi/`) è stato però individuato il servizio web reale che lo alimenta:
un endpoint JSONP non documentato pubblicamente
(`https://www.istat.it/wp-content/themes/EGPbs5-child/contanomi/nati/index2022.php`), privo di
restrizioni in `robots.txt`. L'interfaccia pubblica limita la visualizzazione ai primi 10-50 nomi per
anno, ma il parametro `limit` della richiesta non è vincolato a quell'intervallo: per gli anni più
recenti (2022-2024) restituisce l'intera distribuzione (rispettivamente 25.914, 25.197 e 25.265 nomi
maschili distinti, percentuali che sommano a ~100% delle nascite, nessuna soglia di soppressione
statistica osservabile). Per gli anni precedenti, il servizio presenta però un limite massimo per
richiesta non costante e non documentato, che varia in modo non monotono da un anno all'altro (es. il
1999 si interrompe oltre circa 377 nomi, il 2018 già a 375, il 2021 — il caso peggiore — a soli 137).
Test ripetuti con richieste identiche a distanza di tempo hanno escluso che si tratti di un limite di
frequenza delle richieste (rate limiting) o di una cache instabile: il comportamento è deterministico
per ogni combinazione anno/profondità, il che suggerisce un vincolo strutturale del lato server (es. dati
pre-generati a profondità diverse per anni diversi) piuttosto che una condizione transitoria. È stato
quindi sviluppato uno script di acquisizione (`src/scripts/00_scrape_istat_contanomi.py`) che individua
tramite ricerca binaria, per ciascun anno, la profondità massima effettivamente ottenibile.

La copertura risultante varia dal 66% delle nascite (2021, il caso peggiore) al 100% (2022-2024, dove si
ottiene la distribuzione completa) — si veda `data/raw/istat/contanomi_raw/manifest.csv` e Figura 3 per
il dettaglio anno per anno. **Prima di adottare questi dati come fonte primaria**, sono stati eseguiti due
controlli di validazione (si veda anche §4): (a) i valori estratti per il 2024 (Leonardo: 6.580 nascite,
Sofia: 4.636 nascite; quota primi-30 maschile: 42,94%) sono stati confrontati con quelli della raccolta
manuale precedente, risultando **identici**; (b) l'impatto della copertura variabile sulle metriche
utilizzate è stato quantificato empiricamente, non assunto (Tabella 14, Figura 4). Il risultato di questa
verifica ha motivato la scelta di adottare la nuova fonte come dataset primario per l'Italia, sostituendo
la raccolta manuale ma non eliminandola — resta disponibile come fonte di corroborazione in
`data/raw/istat/istat_annual_top_names.csv`.

La finestra comparabile USA/Italia risultante è **1999-2024** (26 anni), coincidente con il limite reale
della copertura ISTAT a livello di nome (nessun dato esiste prima del 1999), e più ampia della finestra
2006-2024 raggiunta con la sola raccolta manuale.

## 2. Pulizia e normalizzazione

Per gli Stati Uniti, ogni file annuale è stato letto e aggregato in una tabella lunga
(`anno, nome, sesso, conteggio, nascite_totali_sesso, frequenza_relativa`), con la frequenza relativa
calcolata sul totale delle nascite dello stesso sesso in quell'anno, per evitare che la crescita o il
calo della popolazione nel tempo confondesse le variazioni di diversità onomastica con semplici
variazioni di scala. Le metriche sono state calcolate **separatamente per sesso** (maschi, femmine),
scelta necessaria per la comparabilità con l'Italia, il cui dato è sistematicamente riportato per genere.

Per l'Italia, la tabella lunga (`data/raw/istat/istat_contanomi_full.csv`, ~219.000 righe) è ottenuta
direttamente dal servizio web descritto in §1, con lo stesso schema concettuale (nome, anno, genere,
conteggio) più una colonna `percent` fornita direttamente da ISTAT — verificata essere calcolata sul
totale reale delle nascite di quell'anno/genere, non sul solo sottoinsieme catturato dallo scraping
(la somma delle percentuali dei nomi catturati coincide con la copertura osservata, non con 100%, tranne
negli anni a copertura completa). Questa proprietà è ciò che rende possibile usare la quota di
concentrazione come metrica robusta anche negli anni a copertura parziale (§3-4).

## 3. La metrica di diversità primaria (RQ1) e il ruolo dell'entropia di Shannon

Il piano di ricerca originario prevedeva l'uso dell'entropia di Shannon come metrica primaria di
diversità onomastica in entrambi i paesi:

H(anno, sesso) = − Σᵢ pᵢ · log₂(pᵢ)

dove pᵢ è la frequenza relativa dell'i-esimo nome in quell'anno/sesso. Per gli Stati Uniti, dove la
distribuzione è sempre completa, questo calcolo è diretto e viene presentato come figura di
approfondimento (Figura 2, 1880-2025): un minimo relativo attorno agli anni '40-'50 (fase del baby boom)
seguito da una crescita pressoché ininterrotta dagli anni '60 a oggi, coerente con Twenge et al. (2010).

Per l'Italia, la copertura variabile per anno descritta in §1 rende l'entropia calcolata direttamente sui
dati catturati **sistematicamente distorta verso il basso** negli anni a copertura parziale, e in misura
diversa da un anno all'altro — un'entropia calcolata così non sarebbe comparabile nemmeno all'interno
della stessa serie italiana, prima ancora che con gli USA. Si è quindi mantenuta, come **metrica
comparativa primaria tra i due paesi, la quota di concentrazione dei primi N nomi** (top-10 e top-30):
la percentuale di nascite coperta dai nomi più frequenti dell'anno, un proxy di diversità validato in
letteratura (Ogihara 2025, UK 1996-2016, r ≈ −0,96 a −0,99 con un indice di varietà onomastica
indipendente). A differenza dell'entropia, questa metrica dipende solo dai nomi più popolari — che ogni
singolo anno della serie italiana cattura, indipendentemente dalla profondità massima raggiunta (il caso
peggiore, il 2021, raggiunge comunque la posizione 137, ben oltre la trentesima). La sezione 4 dimostra
empiricamente, non solo teoricamente, che questa proprietà tiene.

L'entropia di Shannon completa per l'Italia è comunque calcolabile e riportata come dato aggiuntivo per
gli anni 2022-2024, gli unici con distribuzione integralmente catturata (colonna `entropy_reliable` in
`data/processed/it_diversity_metrics.csv`).

## 4. Validazione scientifica

**Validazione della robustezza alla profondità di copertura.** Prima di usare la quota di concentrazione
come metrica comparativa su anni a copertura disomogenea, la sua robustezza è stata verificata
empiricamente, non assunta: i due anni a copertura completa (2023, 2024) sono stati troncati
artificialmente a ciascuna delle profondità effettivamente raggiunte dagli altri anni (137, 246, ...,
5.577 nomi), e le metriche ricalcolate sul sottoinsieme troncato sono state confrontate con il valore
vero (`src/scripts/01c_check_coverage_bias.py`, Tabella 14, Figura 4). Risultato: la distorsione sulla
quota primi-10/primi-30 è **esattamente zero a ogni profondità testata** — una prova diretta, non
un'assunzione, che la metrica primaria dell'analisi è utilizzabile su tutta la finestra 1999-2024 senza
riserve. L'entropia di Shannon mostra invece una distorsione severa e monotona (dal −19% alla profondità
migliore, 5.577 nomi, fino al −50% alla profondità peggiore, 137 nomi) — motivo per cui resta limitata
al 2022-2024 nel confronto (§3).

**Test di trend Mann-Kendall.** Per verificare che le serie di entropia e di concentrazione mostrino un
andamento monotono statisticamente significativo nel tempo, è stato applicato il test non parametrico di
Mann-Kendall (Mann, 1945; Kendall, 1975) separatamente per sesso, metrica e finestra temporale, con lo
stimatore di pendenza di Sen come misura complementare di intensità del trend. Sui dati USA, tutti i test
eseguiti risultano significativi con p < 0,001: l'entropia cresce e le quote di concentrazione calano in
modo monotono e robusto in ogni combinazione testata.

**Confronto statistico tra paesi.** Sulla finestra sovrapposta **1999-2024** (26 anni) sono stati
eseguiti, per ciascun sesso, quattro test: (a) Mann-Kendall sulla serie propria di ciascun paese; (b)
Mann-Kendall sulla serie differenza USA−Italia; (c) test di Wilcoxon a coppie appaiate sui valori annuali;
(d) intervalli di confidenza bootstrap (percentile, 2000 iterazioni) sulla pendenza di Sen di ciascun
paese.

I risultati (Tabella 12, `data/processed/us_italy_comparison.csv`) mostrano un quadro differenziato per
sesso. Per i nomi **maschili**, la velocità di diversificazione USA e Italia risulta statisticamente
indistinguibile: pendenza di Sen USA −0,004801/anno (IC 95% [−0,005143, −0,004458]) contro Italia
−0,005169/anno (IC 95% [−0,005405, −0,004931]), intervalli sovrapposti, e la serie differenza non mostra
un trend significativo (p = 0,172). Per i nomi **femminili**, l'Italia si sta diversificando
significativamente più in fretta: pendenza di Sen Italia −0,003780/anno contro USA −0,002636/anno,
intervalli **non sovrapposti**, e la serie differenza mostra un trend crescente significativo
(p = 3,4 × 10⁻⁵) — il divario si sta riducendo nel tempo. In entrambi i sessi, il test di Wilcoxon a
coppie appaiate è fortemente significativo (p < 0,0001, statistica 0 su 26 confronti): in ogni singolo
anno della finestra 1999-2024, la quota di concentrazione italiana è risultata superiore a quella
statunitense.

**Convergenza/divergenza USA-Italia (metrica secondaria, non di trend ma di somiglianza).** Oltre al
confronto sul livello di concentrazione di ciascun paese, è stata misurata separatamente quanto le
*stesse* scelte di nomi si stiano avvicinando tra i due paesi — una domanda diversa da "quanto è
concentrato ciascun paese," più vicina a "quanto i due paesi scelgono gli stessi nomi." Una prima
versione (`08_us_italy_name_overlap.py`) contava semplicemente quanti nomi coincidono tra le due liste
dei primi 30 per anno — una misura grezza su appena 60 nomi totali, cieca a tutto ciò che sta fuori dal
livello più popolare. È stata quindi sostituita da una misura sull'intera distribuzione catturata
(`08b_us_italy_distribution_similarity.py`): la similarità coseno tra i due vettori di frequenza
nome-per-nome di ciascun paese/anno/sesso, pesati per la reale quota di nascite di ciascun nome — non
solo i primi 30. Questa misura è per costruzione poco sensibile alla profondità di copertura variabile
dell'Italia, per lo stesso motivo per cui lo è la quota di concentrazione: è dominata dai nomi ad alta
frequenza, che ogni anno cattura indipendentemente dalla profondità massima raggiunta. Risultato:
convergenza significativa per **entrambi** i sessi (maschi: similarità coseno 0,066→0,176, 1999→2024,
p = 2,4 × 10⁻¹²; femmine: 0,119→0,302, p = 2,8 × 10⁻¹¹) — più forte di quanto la sola sovrapposizione
primi-30 avesse rilevato (che non trovava un trend significativo per i maschi). Esempio concreto: Liam e
Noah sono entrambi entrati nella top-30 italiana entro il 2024, assenti nel 1999 — evidenza diretta di
nomi di origine anglo-americana che attraversano il confine culturale.

**Sanity-check del metodo di rilevamento spike (RQ2).** Il metodo di rilevamento (rapporto tra il
conteggio di un nome in un anno e la mediana dei 3 anni precedenti, con soglia minima di conteggio per
escludere il rumore su numeri piccoli) è stato validato verificando che recuperi correttamente casi noti
e documentati: Elsa (Frozen, 2013), Khaleesi (Game of Thrones) e Isabella (Twilight) per gli USA sono
tutti individuati dal metodo prima ancora di essere confermati via ricerca. Ogni candidato del roster
finale (13 casi curati, si veda Risultati) è stato inoltre verificato singolarmente tramite ricerca web
per confermare la plausibilità della causa proposta e la coerenza temporale (l'evento deve precedere il
picco di un intervallo compatibile con concepimento e nascita, tipicamente 9-18 mesi) — non è stato
accettato nessun candidato sulla sola base del rapporto statistico.

## 5. Limiti metodologici principali

Primo, la soglia di soppressione SSA (nomi con <5 nascite/anno/stato/sesso non riportati) introduce una
lieve sottostima della diversità reale statunitense, più accentuata nei decenni iniziali.

Secondo, la profondità di copertura del servizio ISTAT utilizzato varia per anno (66-100% delle nascite,
minimo storico 137 nomi nel 2021) per un motivo tecnico non documentato dal lato server, non per una
politica di soppressione dichiarata. Questo limite è stato **quantificato empiricamente** (§4, Tabella
14): non introduce distorsione misurabile sulla quota di concentrazione primi-10/30 (la metrica primaria
di questo studio), ma introduce una distorsione severa e monotona sull'entropia di Shannon (dal −19% al
−50% a seconda della profondità) — per questo l'entropia italiana è riportata solo per il 2022-2024,
esplicitamente etichettata come tale, e non usata come base di confronto di trend con gli USA.

Terzo, il servizio web utilizzato per l'Italia non è un'API pubblicamente documentata: è stato
individuato analizzando il codice JavaScript dello strumento "contanomi" ed è, per sua natura, meno
stabile nel tempo di un formato di dati pubblicato ufficialmente come quello SSA — un cambiamento
lato-server non annunciato potrebbe rendere lo script di acquisizione non più funzionante in futuro. I
dati grezzi scaricati sono comunque conservati in repository (`data/raw/istat/contanomi_raw/`) per
garantire la riproducibilità dell'analisi indipendentemente da modifiche successive del servizio.

Quarto, il confronto USA/Italia è per necessità limitato alla finestra 1999-2024, poiché l'Italia non
dispone di dati a livello di nome per gli anni precedenti; l'entropia USA 1880-2025 viene quindi
presentata come figura di approfondimento non comparativa (Figura 2).

Quinto, il legame tra un picco di frequenza di un nome e un evento culturale specifico resta per natura
correlazionale, non causale in senso stretto: la verifica di coerenza temporale e di plausibilità
(§4) riduce ma non elimina il rischio di attribuire un picco alla causa sbagliata tra più eventi
concomitanti — un caso discusso esplicitamente in Risultati/Discussione è quello di "Chanel" in Italia,
per cui sia la nascita di una figlia di un personaggio pubblico sia il fascino del marchio di moda
stesso sono presentati come cause concorrenti, non alternative reciprocamente esclusive.
