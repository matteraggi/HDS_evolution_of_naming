# Metodologie e Dati (bozza — sezione a cura di Person A)

> Nota per la revisione: questa è una bozza di lavoro, non il testo finale del paper. **Riscritta il
> 2026-08-16** dopo un cambiamento sostanziale nella fonte dati italiana (si veda §1 e `PROJECT_LOG.md`
> per la cronologia completa): è stato individuato un servizio web reale dietro lo strumento ISTAT
> "contanomi", non documentato pubblicamente ma funzionante, che ha sostituito la raccolta manuale da
> PDF come fonte primaria. Questo ha risolto i due limiti principali della versione precedente di questa
> bozza (finestra ristretta a 2006-2024, dipendenza da una fonte secondaria per 15 anni su 19) ma ne ha
> introdotto uno nuovo, diverso e più tracciabile: una profondità di copertura variabile per anno, la cui
> non-distorsione sulla metrica primaria è stata dimostrata empiricamente (§4). **Aggiornata di nuovo il
> 2026-08-16**: §4 ora distingue esplicitamente i test di ipotesi formali (con H₀/H₁/α dichiarati, su
> richiesta del docente) dai controlli di robustezza; aggiunta §5 sul rilevamento di spike positivi *e
> negativi* (crolli dovuti a eventi negativi, non solo picchi); aggiunto il controllo di robustezza
> geografica per stato (§4.2). Lunghezza attuale: ~3300 parole — oltre il budget originario di ~1700 per
> questa sezione (si veda `PROJECT_LOG.md` per la nota sul bilancio parole complessivo del paper).

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
`dataset/istat/COLLECTION_NOTES.md` per il dettaglio completo, conservato come traccia di corroborazione
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
ottiene la distribuzione completa) — si veda `dataset/istat/contanomi_raw/manifest.csv` e Figura 3 per
il dettaglio anno per anno. **Prima di adottare questi dati come fonte primaria**, sono stati eseguiti due
controlli di validazione (si veda anche §4): (a) i valori estratti per il 2024 (Leonardo: 6.580 nascite,
Sofia: 4.636 nascite; quota primi-30 maschile: 42,94%) sono stati confrontati con quelli della raccolta
manuale precedente, risultando **identici**; (b) l'impatto della copertura variabile sulle metriche
utilizzate è stato quantificato empiricamente, non assunto (Tabella 14, Figura 4). Il risultato di questa
verifica ha motivato la scelta di adottare la nuova fonte come dataset primario per l'Italia, sostituendo
la raccolta manuale ma non eliminandola — resta disponibile come fonte di corroborazione in
`dataset/istat/istat_annual_top_names.csv`.

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

Per l'Italia, la tabella lunga (`dataset/istat/istat_contanomi_full.csv`, ~219.000 righe) è ottenuta
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
`dataset/processed/it_diversity_metrics.csv`).

## 4. Validazione scientifica

Questa sezione distingue esplicitamente due categorie di verifica, che rispondono a domande diverse e
vanno lette diversamente: (a) **test di ipotesi formali**, ciascuno con un'ipotesi nulla (H₀) dichiarata,
un'ipotesi alternativa (H₁) e una soglia di significatività fissata a α = 0,05 in tutto il paper; (b)
**controlli di robustezza/sensibilità**, che non testano un'ipotesi statistica ma quantificano quanto una
conclusione dipenderebbe da una scelta metodologica diversa (es. una profondità di copertura diversa) — utili
quanto un test formale, ma di natura logica diversa, e per questo tenuti distinti.

### 4.1 Test di ipotesi formali

**Test di trend Mann-Kendall** (Mann, 1945; Kendall, 1975). Applicato separatamente per sesso, metrica
(entropia, quota primi-10, quota primi-30) e finestra temporale.
- **H₀**: la serie non presenta alcun trend monotono nel tempo (i valori sono indipendenti e
  identicamente distribuiti nell'ordine osservato).
- **H₁**: la serie presenta un trend monotono (crescente o decrescente).
- Statistica S di Mann-Kendall, distribuzione normale approssimata per n > 10; lo stimatore di pendenza
  di Sen accompagna il test come misura di intensità del trend (non è un test a sé, ma una stima puntuale
  robusta agli outlier che ha senso riportare solo quando H₀ è respinta).
- **Risultato USA**: su tutte le combinazioni testate (3 metriche × 3 gruppi di sesso × 2 finestre
  temporali sui dati storici, più le repliche sulla finestra 1999-2024), **H₀ è respinta con p < 0,001** in
  ogni caso: l'entropia cresce e le quote di concentrazione calano in modo monotono e statisticamente
  robusto.

**Test di Wilcoxon a coppie appaiate** (confronto di livello USA vs Italia, non di trend). Applicato ai
26 valori annuali appaiati (1999-2024) della quota primi-30, separatamente per sesso.
- **H₀**: la mediana delle differenze appaiate (quota_USA − quota_Italia) è zero, cioè non c'è una
  differenza sistematica di livello tra i due paesi.
- **H₁**: la mediana delle differenze appaiate è diversa da zero.
- **Risultato**: per entrambi i sessi, **H₀ è respinta con p < 0,0001** (statistica del test pari a 0 su
  26 confronti in entrambi i casi, il minimo possibile) — la quota di concentrazione italiana è
  sistematicamente superiore a quella statunitense in ogni singolo anno della finestra, non solo in media.

**Test di Mann-Kendall sulla serie differenza (USA − Italia)**, per verificare se il divario tra i due
paesi si sta sistematicamente ampliando o riducendo nel tempo (H₀/H₁ come sopra, applicate alla serie
delle differenze anno per anno anziché al livello assoluto).
- **Risultato maschi**: H₀ non respinta (p = 0,172) — il divario resta stabile.
- **Risultato femmine**: **H₀ respinta** (p = 3,4 × 10⁻⁵, trend crescente) — il divario si sta riducendo:
  l'Italia diversifica i nomi femminili più velocemente degli USA.

**Test di Mann-Kendall sulla similarità coseno USA-Italia** (convergenza/divergenza, si veda §4.3 per il
motivo della scelta metrica).
- **H₀**: nessun trend monotono nella similarità tra le due distribuzioni nome-per-nome nel tempo.
- **H₁**: la similarità aumenta (convergenza) o diminuisce (divergenza) in modo monotono.
- **Risultato**: **H₀ respinta per entrambi i sessi** — maschi p = 2,4 × 10⁻¹² (τ di Kendall = 0,98, quasi
  perfettamente monotono), femmine p = 2,8 × 10⁻¹¹ — evidenza di convergenza statisticamente robusta, non
  di un andamento casuale.

Un'osservazione di rigore metodologico: gli **intervalli di confidenza bootstrap** sulla pendenza di Sen
(percentile, 2000 iterazioni per ricampionamento dei residui attorno al fit Theil-Sen) **non costituiscono
un test di ipotesi formale in senso stretto** — la non sovrapposizione di due IC al 95% è un'euristica
comunemente usata come segnale informale che due pendenze differiscono, ma non equivale a un test a due
campioni sulla differenza delle pendenze con una propria H₀/H₁ esplicita e un proprio livello di
significatività calibrato. Per questo motivo il test formale primario sulla domanda "il divario tra i due
paesi cambia nel tempo?" resta il Mann-Kendall sulla serie differenza sopra descritto; il confronto degli
IC bootstrap (pendenza USA −0,004801/anno IC 95% [−0,005143, −0,004458] vs Italia −0,005169/anno IC 95%
[−0,005405, −0,004931] per i maschi, intervalli sovrapposti, coerente con H₀ non respinta sulla serie
differenza; pendenza Italia −0,003780/anno vs USA −0,002636/anno per le femmine, intervalli **non**
sovrapposti, coerente con H₀ respinta) è riportato come conferma supplementare coerente, non come prova
indipendente.

### 4.2 Controlli di robustezza (non test di ipotesi)

**Robustezza alla profondità di copertura.** I due anni italiani a copertura completa (2023, 2024) sono
stati troncati artificialmente a ciascuna delle profondità effettivamente raggiunte dagli altri anni (137,
246, ..., 5.577 nomi), e le metriche ricalcolate sul sottoinsieme troncato sono state confrontate con il
valore vero (`src/scripts/01c_check_coverage_bias.py`, Tabella 14, Figura 4). Non è un test di ipotesi (non
c'è una H₀ da respingere: è una misura diretta e deterministica di quanto una metrica cambierebbe con
meno dati). Risultato: la distorsione sulla quota primi-10/primi-30 è **esattamente zero a ogni
profondità testata**; l'entropia di Shannon mostra invece una distorsione monotona dal −19% (profondità
migliore) al −50% (profondità peggiore) — motivo per cui resta limitata al 2022-2024 nel confronto (§3).

**Robustezza geografica dei casi-studio RQ2 (nuovo).** Per i casi-studio più solidi del roster (positivi e
negativi, solo USA — non esistono dati regionali italiani comparabili), è stato verificato se il
salto/crollo osservato a livello nazionale fosse geograficamente uniforme o concentrato in pochi stati,
usando i dati SSA per stato (`dataset/namesbystate/`, 51 file, 1910-2025). Per ciascun caso, si calcola il
rapporto conteggio-anno-evento / mediana-3-anni-precedenti separatamente per ogni stato con dati
sufficienti, e si conta la quota di stati che si muove nella stessa direzione dell'effetto nazionale
(`src/scripts/15_state_concentration_analysis.py`, Tabella 15, Figura 8). Anche questo non è un test
di ipotesi in senso stretto, ma un argomento di plausibilità: un evento mediatico realmente nazionale
dovrebbe muovere la maggioranza degli stati nella stessa direzione, mentre un effetto concentrato in uno o
due stati suggerirebbe una causa regionale o un artefatto statistico. Risultato (9 casi, 6 positivi + 3
negativi): **7 casi su 9 mostrano oltre il 90% degli stati concordanti** con la direzione nazionale (es.
Jaime 100%, Kobe 97%, Alexa 97%); le due eccezioni sono Jaslene (79%, ANTM 2007) e Hillary (74%, 1993) —
compatibili rispettivamente con un'adozione inizialmente più concentrata nelle aree a maggiore presenza
ispanica e con una polarizzazione politica che, ragionevolmente, non ha colpito tutti gli stati in modo
identico — dettagli interessanti più che una debolezza del metodo.

### 4.3 Scelta della metrica di convergenza (non un test, una scelta di misura)

Oltre al confronto sul livello di concentrazione di ciascun paese (§4.1), è stata misurata separatamente
quanto le *stesse* scelte di nomi si stiano avvicinando tra i due paesi. Una prima versione
(`08_us_italy_name_overlap.py`) contava quanti nomi coincidono tra le liste dei primi 30 per anno — una
misura grezza su appena 60 nomi totali, cieca a tutto ciò che sta fuori dal livello più popolare, che
infatti non rilevava un trend significativo per i maschi. È stata sostituita da una misura sull'intera
distribuzione catturata (`08b_us_italy_distribution_similarity.py`): la similarità coseno tra i due vettori
di frequenza nome-per-nome di ciascun paese/anno/sesso, pesati per la reale quota di nascite di ciascun
nome. Questa misura è poco sensibile alla profondità di copertura variabile dell'Italia per lo stesso
motivo della quota di concentrazione (§4.2): è dominata dai nomi ad alta frequenza, catturati ogni anno
indipendentemente dalla profondità massima raggiunta. Il test di ipotesi formale su questa serie è
riportato in §4.1; qui si riporta solo un esempio concreto a corredo del risultato statistico: Liam e Noah
sono entrambi entrati nella top-30 italiana entro il 2024, assenti nel 1999.

## 5. Rilevamento di spike ed eventi culturali (RQ2)

**Metodo di rilevamento.** Per ogni nome/sesso/anno, si calcola il rapporto tra il conteggio dell'anno e
la mediana dei 3 anni precedenti, con una soglia minima di conteggio (post-salto per gli spike positivi,
pre-crollo per i casi negativi) per escludere rumore statistico su numeri piccoli — una variazione da 2 a
6 nascite è un rapporto di 3× ma non significa nulla; una da 2.000 a 6.000 sì. Il metodo è puramente
statistico e produce solo **candidati**: nessun candidato è stato accettato nel roster finale senza (a)
verifica della plausibilità della causa proposta tramite ricerca web indipendente, e (b) verifica di
coerenza temporale (l'evento deve precedere il picco/crollo di un intervallo compatibile con
concepimento e nascita, tipicamente 9-18 mesi).

**Sanity-check del metodo.** Applicato ai dati USA, il metodo recupera correttamente tre casi noti e
documentati in letteratura prima ancora di essere confermati via ricerca: Elsa (Frozen, 2013), Khaleesi
(Game of Thrones), Isabella (Twilight) — si veda anche l'ONS britannico (2015) per un precedente
istituzionale dello stesso tipo di analisi.

**Estensione ai crolli ("anti-spike").** Lo stesso metodo, invertito, individua nomi che hanno subito un
crollo improvviso — l'ipotesi di lavoro è che un evento *negativo* (uno scandalo, una controversia, un
personaggio pubblico che diventa impopolare) possa "bruciare" un nome così come un evento positivo può
lanciarlo (`src/scripts/14_find_us_declines.py` per gli USA, `16_find_it_declines.py` per l'Italia,
soglia di base scalata alla popolazione: ≥300 nascite USA, ≥100 Italia). La soglia di significatività
richiede un conteggio di base pre-crollo sostanziale, non solo un rapporto grande, per lo stesso motivo
del filtro sugli spike positivi. Roster finale (Tabella 16, 4 casi — un caso italiano candidato,
"Enrica", è stato scartato perché il calo prosegue linearmente ben oltre l'anno dell'evento proposto,
più coerente con un declino di lungo periodo già in corso che con un effetto puntuale): **Hillary/Hilary**
(crollo del 58% tra il 1992 e il 1993, l'anno in cui Hillary Clinton diventa First Lady — uno dei cali più
documentati nella letteratura sui nomi USA, si veda ad es. Ghirlanda, CUNY); **Kobe** (crollo 2003-2004,
in coincidenza con l'accusa di aggressione sessuale a Kobe Bryant); **Alexa** (crollo dal 2015, "effetto
Alexa" ampiamente documentato nella stampa dopo il lancio di Amazon Echo); **Erica** (Italia, crollo
2001-2002, 863→416 nascite, in coincidenza con il delitto di Novi Ligure — Erika De Nardo, 16 anni,
uccide madre e fratello nel febbraio 2001, uno dei casi di cronaca nera più discussi in Italia in
quel periodo; la tempistica combacia esattamente, con il calo che si aggrava durante il processo di
dicembre 2001 e l'appello di maggio 2002).

**Un falso positivo intercettato, utile come nota di rigore metodologico.** La ricerca dei crolli
italiani ha inizialmente segnalato "Nicolò" e "Desirè" come collassi enormi (rapporto fino a 0,02). Prima
di accettarli, è stata controllata la traiettoria delle grafie alternative: il conteggio di "NICOLO"
crolla nel 2011 esattamente nello stesso anno in cui compare "NICOLO'" con un conteggio quasi
compensativo (3.196 nel 2010 → 99 nel 2011 per "NICOLO", ma 2.956 per "NICOLO'" nel 2011) — non un calo
reale, ma un cambiamento nella convenzione di trascrizione dell'accento da parte di ISTAT. Entrambi i
casi sono stati esclusi dal roster. Questo controllo — verificare le grafie alternative prima di
accettare un candidato — è ora parte integrante del processo di validazione dei candidati-crollo, non
solo un aneddoto.

## 6. Limiti metodologici principali

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
dati grezzi scaricati sono comunque conservati in repository (`dataset/istat/contanomi_raw/`) per
garantire la riproducibilità dell'analisi indipendentemente da modifiche successive del servizio.

Quarto, il confronto USA/Italia è per necessità limitato alla finestra 1999-2024, poiché l'Italia non
dispone di dati a livello di nome per gli anni precedenti; l'entropia USA 1880-2025 viene quindi
presentata come figura di approfondimento non comparativa (Figura 2).

Quinto, il legame tra un picco di frequenza di un nome e un evento culturale specifico resta per natura
correlazionale, non causale in senso stretto: la verifica di coerenza temporale e di plausibilità
(§5) riduce ma non elimina il rischio di attribuire un picco alla causa sbagliata tra più eventi
concomitanti — un caso discusso esplicitamente in Risultati/Discussione è quello di "Chanel" in Italia,
per cui sia la nascita di una figlia di un personaggio pubblico sia il fascino del marchio di moda
stesso sono presentati come cause concorrenti, non alternative reciprocamente esclusive.

Sesto, il controllo di robustezza geografica (§4.2) ha copertura disomogenea tra i casi: per nomi già
rari a livello nazionale nell'anno di riferimento (es. Nevaeh, solo 7 stati con dati sufficienti; Devante,
11 stati), la soglia di soppressione SSA per stato lascia pochi stati osservabili, e la percentuale di
"stati concordanti" riportata va letta con questo in mente — è un'evidenza di plausibilità supplementare,
non un test con potenza statistica garantita, ed è più informativa per i casi con ampia copertura
geografica (es. Jaime, 45 stati; Hillary, 43 stati) che per quelli con pochi stati osservabili.
