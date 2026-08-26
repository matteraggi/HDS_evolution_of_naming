# L'Evoluzione dei Nomi: Diversità Culturale, Influenza dei Media e Individualismo nei Nomi dei Neonati (USA vs. Italia)

**Abstract** — Questo lavoro analizza come sono cambiate le scelte dei nomi dei neonati negli Stati Uniti (1880–2025) e in Italia (1999–2024), mettendo a confronto due culture diverse per comprendere le mode onomastiche, l'impatto dei mass media e l'evoluzione dei ruoli di genere. Attraverso l'analisi dei dati di milioni di nascite, emergono tre risultati principali. Primo, in entrambi i paesi i genitori cercano sempre più nomi unici e variati, riducendo la concentrazione sui pochi nomi tradizionali del passato, mentre le preferenze americane e italiane si stanno lentamente avvicinando. Secondo, analizzando 152 eventi nel mondo del cinema, della musica e dello sport, dimostriamo che i personaggi dei film e delle serie TV (+232%) e le star della musica pop (+245%) scatenano vere e proprie mode collettive che durano negli anni, mentre i successi sportivi (+76%) hanno un impatto molto più contenuto e temporaneo. Terzo, la diffusione dei nomi gender-neutral (unissex) mostra una profonda differenza culturale: negli USA l'uso di nomi neutri è in costante crescita (dal 7,3% all'8,8%), mentre in Italia rimane un fenomeno quasi del tutto assente (sotto lo 0,2%) a causa di vincoli legali e tradizioni più rigide.

**Parole chiave:** diversità onomastica, individualismo culturale, test di Mann-Kendall, event study, nomi dei neonati, confronto USA-Italia

## Introduzione

Scegliere il nome di un figlio è, all'apparenza, una delle decisioni più intime e private che un genitore possa prendere. Tuttavia, l'analisi demografica su grande scala rivela come questa scelta sia fortemente condizionata da dinamiche sociali collettive: milioni di genitori, senza alcuna coordinazione esplicita, finiscono per convergere simultaneamente sulle medesime preferenze per poi abbandonarle in blocco nel giro di pochi anni. Questo fenomeno solleva un interrogativo sociologico fondamentale: quanto di genuinamente "individuale" permane in una decisione anagrafica e in che misura essa sia invece guidata da forze esterne, quali la cultura di massa, lo shock mediatico, le trasformazioni valoriali o le normative nazionali?

A differenza di altri domini culturali — come la musica, la moda abbigliativa o il consumo mediale — in cui le preferenze individuali sono sollecitate da campagne pubblicitarie o da algoritmi di raccomandazione profilati (tematiche vagliate in fase preliminare di ricerca, quali i bias nei sistemi di raccomandazione o la teoria dell'onnivoro culturale sui dati GSS), l'onomastica rappresenta un **osservatorio di laboratorio "puro"** (Lieberson, 2000). Non esiste un'industria commerciale che promuova attivamente un nome a discapito di un altro; di conseguenza, le fluttuazioni temporali riflettono quasi esclusivamente l'evoluzione spontanea del gusto sociale e l'impatto degli stimoli ambientali.

Dal punto di vista teorico, il dibattito sociologico sul gusto sociale si articola principalmente attorno a due paradigmi interpretativi complementari. Da un lato, il modello delle mode interne formalizzato da Lieberson (2000) e Lieberson e Bell (1992) interpreta l'evoluzione dei nomi come un processo prevalentemente endogeno, regolato da meccanismi spontanei di saturazione e da latenti dinamiche di distinzione sociale, in cui i genitori abbandonano i nomi divenuti troppo popolari per adottare altre varianti. Dall'altro lato, la prospettiva di Twenge et al. (2010, 2016) collega il costante declino della quota dei nomi tradizionali nei paesi occidentali ad una trasformazione valoriale di lungo periodo verso un crescente individualismo culturale, in cui la decisione anagrafica diventa un veicolo per affermare l'unicità e la singolarità del neonato anziché la sua appartenenza comunitaria.

A questa dinamica valoriale di lungo periodo si sovrappone, nei decenni più recenti, il potente catalizzatore della globalizzazione. La diffusione capillare di infrastrutture di distribuzione culturale su scala mondiale, le piattaforme di streaming cinematografico e televisivo, le reti musicali globali e i social media, ha ridotto drasticamente i tempi e le barriere nella circolazione dei simboli e delle mode. Di conseguenza, shock culturali originati in un preciso contesto (come una serie TV di successo o un'icona della musica pop globale) sono in grado di sollecitare simultaneamente le preferenze dei genitori su entrambe le sponde dell'Atlantico, guidando una convergenza distributiva tra paesi storicamente distinti per tradizioni e vincoli normativi, come gli Stati Uniti e l'Italia. Più di recente, Ogihara (2025a) e Fan et al. (2025) hanno validato l'impiego delle quote di concentrazione dei nomi dominanti come *proxy* statisticamente affidabile per misurare la diversità complessiva dell'onomastica, anche in presenza di distribuzioni storiche parzialmente troncate.

Nonostante la ricchezza di questi contributi, la quasi totalità degli studi esistenti si limita ad un'analisi mono-nazionale (focalizzata prevalentemente sul contesto statunitense o anglosassone). Manca nella letteratura uno studio comparativo transatlantico che metta a confronto la dinamica americana con un contesto continentale europeo caratterizzato da una differente struttura demografica e da vincoli giuridico-regolatori più rigidi, come quello italiano. Il presente lavoro intende colmare questo vuoto empirico attraverso una comparazione sistematica tra Stati Uniti (1880–2025) e Italia (1999–2024).

Per strutturare l'indagine empirica in modo rigoroso, il lavoro è organizzato attorno a tre domande di ricerca formali ($RQ1, RQ2, RQ3$):

1. **RQ1 — Diversificazione di Lungo Periodo e Convergenza Transatlantica**: La diversità dei nomi sta aumentando in modo sistematico in entrambi i contesti nazionali? Le preferenze italiane e americane tendono a convergere a livello distributivo per effetto della globalizzazione mediale, oppure mantengono traiettorie indipendenti?
2. **RQ2 — Risposta Causale agli Shock Mediatici e Persistenza**: Gli eventi culturali di massa (personaggi cinematografici/TV, star della musica pop, imprese sportive) generano un incremento temporale significativo e causale nell'adozione dei nomi esposti rispetto a controlli non esposti appaiati? Tale risposta è temporanea o mostra un'adozione strutturale permanente nel tempo?
3. **RQ3 — Evoluzione delle Norme di Genere ed Emergenza dei Nomi Gender-Neutral**: L'evoluzione dei ruoli di genere si traduce in una maggiore diffusione dei nomi non marcati rispetto al sesso (*unisex* / *gender-neutral*), oppure permangono vincoli normativo-culturali differenziali tra le due sponde dell'Atlantico?

Il resto del paper è organizzato come segue: la Sezione 2 descrive i dataset, le metriche ed la metodologia d'Event Study con controlli appaiati; la Sezione 3 presenta le evidenze empiriche per ciascuna domanda di ricerca; la Sezione 4 discute le implicazioni sociologiche e la robustezza geografica; infine, la Sezione 5 sintetizza i contributi principali del lavoro.

## Metodologie e Dati

*(Sezione integrata da `metodologie_dati_DRAFT.md`, a cura di Person A — qui riportata per intero
così il documento resta un unico file navigabile; si veda quel file per la versione più aggiornata in
caso di disallineamento.)*

### Fonti dei dati

Per rispondere alle domande di ricerca è stato necessario ricostruire due serie storiche di nomi alla
nascita, una per gli Stati Uniti e una per l'Italia, che si sono rivelate profondamente asimmetriche
per struttura e accessibilità — un'asimmetria che, come discusso più avanti nella sezione sul Fattore
Umano, non è un semplice ostacolo tecnico ma un dato interessante di per sé.

**Stati Uniti.** La fonte primaria è la *Social Security Administration* (SSA), che dal 1997 pubblica
annualmente l'archivio "Baby Names from Social Security Card Applications"
(`https://www.ssa.gov/oact/babynames/names.zip`), rilasciato con licenza CC0/dominio pubblico.
L'archivio contiene un file per ogni anno dal 1880 al 2025 (146 file), con record
`nome,sesso,conteggio` per ogni combinazione osservata. L'unico limite dichiarato è una soglia di
soppressione statistica: i nomi attribuiti a meno di 5 nascite in un dato anno/stato/sesso non
vengono riportati. Dopo la pulizia, la tabella lunga risultante conta oltre 2,18 milioni di
combinazioni nome/anno/sesso.

**Italia.** Il piano di ricerca iniziale prevedeva l'acquisizione manuale dei dati italiani, poiché
ISTAT non pubblica una tabella cumulativa bulk nome × anno × sesso × conteggio attraverso i suoi
canali ufficiali — verificato direttamente sul portale Open Data / High Value Datasets, che non
contiene alcun dataset a livello di nome. Questa raccolta manuale è stata effettivamente svolta in
una prima fase (2004 e 2006-2024, da 14 PDF ISTAT più nomix.it come fonte secondaria per gli anni non
altrimenti reperibili), ed è tuttora conservata come traccia di corroborazione.

Analizzando però il codice JavaScript dello strumento interattivo "contanomi"
(`istat.it/dati/calcolatori/contanomi/`) è stato individuato il servizio web reale che lo alimenta: un
endpoint JSONP non documentato pubblicamente, privo di restrizioni in `robots.txt`. L'interfaccia
pubblica limita la visualizzazione ai primi 10-50 nomi per anno, ma il parametro `limit` della
richiesta non è vincolato a quell'intervallo: per il 2022-2024 restituisce l'intera distribuzione
(~25.000 nomi distinti per sesso, percentuali che sommano a ~100%, nessuna soglia di soppressione
osservabile). Per gli anni precedenti il servizio presenta un limite massimo per richiesta non
costante e non documentato, individuato per ciascun anno tramite ricerca binaria. La copertura
risultante varia dal 66% delle nascite (2021, il caso peggiore) al 100% (2022-2024) — si veda Figura
3 per il dettaglio anno per anno.

Prima di adottare questi dati come fonte primaria, sono stati eseguiti due controlli: (a) i valori
estratti per il 2024 (Leonardo: 6.580 nascite, Sofia: 4.636; quota primi-50 maschile: 53,28%) sono
stati confrontati con quelli della raccolta manuale, risultando identici; (b) l'impatto della
copertura variabile sulle metriche utilizzate è stato quantificato empiricamente, non assunto (si
veda sotto). La finestra comparabile USA/Italia risultante è **1999-2024** (26 anni), il limite reale
della copertura ISTAT a livello di nome.

### Pulizia e normalizzazione

Per gli Stati Uniti, ogni file annuale è stato aggregato in una tabella lunga (`anno, nome, sesso,
conteggio, nascite_totali_sesso, frequenza_relativa`), con la frequenza relativa calcolata sul totale
delle nascite dello stesso sesso in quell'anno. Le metriche sono calcolate separatamente per sesso,
scelta necessaria per la comparabilità con l'Italia. Per l'Italia, la tabella lunga (~219.000 righe) è
ottenuta direttamente dal servizio web, con una colonna `percent` verificata essere calcolata sul
totale reale delle nascite di quell'anno/genere — non sul solo sottoinsieme catturato dallo scraping.
Questa proprietà è ciò che rende possibile usare la quota di concentrazione come metrica robusta anche
negli anni a copertura parziale.

### La metrica di diversità primaria e il ruolo dell'entropia di Shannon

Il piano di ricerca originario prevedeva l'uso dell'entropia di Shannon come metrica primaria in
entrambi i paesi. Per gli Stati Uniti questo calcolo resta diretto (Fig. 2, 1880-2025): un minimo
relativo attorno agli anni '40-'50 (baby boom) seguito da una crescita pressoché ininterrotta dagli
anni '60 a oggi. Per l'Italia, la copertura variabile rende l'entropia calcolata sui dati catturati
sistematicamente distorta verso il basso, e in misura diversa da un anno all'altro. Si è quindi
mantenuta come metrica comparativa primaria la **quota di concentrazione dei primi N nomi**
(top-10 e top-50), un proxy di diversità validato in letteratura (Ogihara 2025, r ≈ −0,96 a −0,99 con
un indice di varietà indipendente), che dipende solo dai nomi più popolari — catturati ogni anno
indipendentemente dalla profondità massima raggiunta.

Si sottolinea una distinzione concettuale fondamentale: le metriche di concentrazione e diversità dei nomi fungono da proxy quantitativo per l'**individualizzazione** (la frammentazione sociale e la ricerca di unicità nelle scelte di consumo culturale), **non** come misura psicologica diretta o valutazione morale dell'*individualismo*.

### Validazione scientifica

Questa sezione distingue esplicitamente due categorie di verifica: **test di ipotesi formali**
(H₀/H₁/α = 0,05 dichiarati, sintetizzati nella Tabella 17) e **controlli di robustezza/sensibilità**, che non testano un'ipotesi
statistica ma quantificano quanto una conclusione dipenderebbe da una scelta metodologica diversa.

**Mann-Kendall** (Mann 1945; Kendall 1975). H₀: nessun trend monotono; H₁: trend monotono
(crescente/decrescente). Su tutte le combinazioni testate sui dati USA, H₀ è respinta con p < 0,001.

**Wilcoxon a coppie appaiate** (livello USA vs Italia, 26 anni appaiati, primi 10 e primi 50 nomi). H₀:
mediana delle differenze appaiate uguale a zero. Respinta per entrambi i sessi e a entrambe le soglie
con p = 2,98 × 10⁻⁸: l'Italia è sistematicamente più concentrata in ogni singolo anno, indipendentemente
da quanti nomi si contano.

**Mann-Kendall sulla serie differenza (USA−Italia)**, primi 10 e primi 50: per le femmine il risultato
è coerente a entrambe le soglie, H₀ respinta (primi-10 p = 1,6 × 10⁻⁵; primi-50 p = 4,8 × 10⁻³), divario
in riduzione. Per i maschi il risultato dipende dalla soglia: H₀ non respinta ai primi 10 (p = 0,078,
divario stabile), ma respinta ai primi 50 (p = 5,0 × 10⁻⁷, divario in lieve allargamento).

**Mann-Kendall sulla similarità coseno USA-Italia**: H₀ respinta per entrambi i sessi (maschi
p = 2,4 × 10⁻¹², τ = 0,98; femmine p = 2,8 × 10⁻¹¹) — convergenza statisticamente robusta.

Gli **intervalli di confidenza bootstrap** sulla pendenza di Sen (percentile, 2000 iterazioni) non
costituiscono un test di ipotesi formale in senso stretto — la non sovrapposizione è un'euristica
informale, riportata come conferma supplementare del test Mann-Kendall sulla serie differenza, non
come prova indipendente.

Il **controllo di robustezza alla profondità di copertura per la concentrazione e l'entropia** (troncamento artificiale dei due anni
italiani completi alle profondità reali degli altri anni) mostra che la distorsione sulla quota
primi-10/primi-50/primi-100 è **esattamente zero a ogni profondità testata**, mentre l'entropia di Shannon
mostra una distorsione monotona dal −19% al −50% (Tabella 14, Fig. 4) — da qui la scelta di
riportare l'entropia italiana solo per il 2022-2024.

Il **controllo di robustezza della similarità coseno rispetto alla copertura** (`src/scripts/01d_check_cosine_bias.py`)
dimostra che il troncamento della distribuzione italiana produce un'alterazione trascurabile della similarità coseno rispetto agli USA: la distorsione è inferiore all'1,9% persino al livello di troncamento peggiore degli anni storici (profondità 377 nel 1999) e scende sotto lo 0,46% per tutte le profondità superiori a 1.000 nomi. Questo conferma che la misura di convergenza distributiva (coseno) è empiricamente esente da bias di copertura significativo su tutto il periodo 1999-2024.

Il **controllo di robustezza geografica** (nuovo, si veda Risultati) usa i dati SSA per stato per
verificare se i casi-studio RQ2 più solidi si muovono in modo uniforme su tutti gli stati o in modo
concentrato in pochi — un argomento di plausibilità, non un test formale.

### Rilevamento di spike ed eventi culturali (RQ2)

Per ogni nome/sesso/anno si calcola il rapporto tra il conteggio dell'anno e la mediana dei 3 anni
precedenti, con una soglia minima di conteggio per escludere rumore statistico su numeri piccoli. Il
metodo produce solo **candidati**: nessuno è stato accettato senza (a) verifica della plausibilità
della causa proposta tramite ricerca web indipendente, e (b) verifica di coerenza temporale
(l'evento deve precedere il picco/crollo di un intervallo compatibile con concepimento e nascita,
9-18 mesi). Il metodo è stato validato recuperando correttamente tre casi noti in letteratura prima
ancora di essere confermati via ricerca: Elsa (*Frozen*, 2013), Khaleesi (*Game of Thrones*), Isabella
(*Twilight*).

Lo stesso metodo, invertito, individua i crolli — l'ipotesi è che un evento *negativo* possa "bruciare"
un nome così come un evento positivo può lanciarlo, con una soglia di base pre-crollo scalata alla
popolazione (≥300 nascite USA, ≥100 Italia). Durante questa ricerca sono stati intercettati e scartati
due falsi positivi italiani ("Nicolò" e "Desirè"), che si sono rivelati puri artefatti di trascrizione
ISTAT (cambio nella codifica dell'accento a metà serie, con la grafia alternativa che assorbe quasi
esattamente il conteggio "mancante" lo stesso anno) — un controllo che è ora parte del processo di
validazione, non solo un aneddoto.

### Limiti metodologici principali

In sintesi (si veda `metodologie_dati_DRAFT.md` §6 per il dettaglio completo): (1) la soglia di
soppressione SSA sottostima leggermente la diversità storica USA; (2) la copertura ISTAT variabile
per anno non distorce la quota di concentrazione ma limita l'entropia italiana al 2022-2024; (3) il
servizio ISTAT usato non è un'API pubblicamente documentata, meno stabile nel tempo di un formato
ufficiale — i dati grezzi sono comunque conservati in repository per garantire riproducibilità; (4) il
confronto USA/Italia è limitato alla finestra 1999-2024; (5) il legame tra un picco/crollo e un
evento culturale resta correlazionale, non causale in senso stretto; (6) il controllo di robustezza
geografica ha copertura disomogenea tra i casi (da 7 a 51 stati con dati sufficienti a seconda del
nome).

## Risultati

### La diversità cresce in entrambi i paesi, ma l'Italia resta indietro

Partiamo dal dato più semplice da enunciare. Negli Stati Uniti, la quota di nascite maschili coperta
dai primi 10 nomi è passata da circa il 44% nel 1880 a circa l'8% nel 2025 — un crollo di oltre cinque
volte in 145 anni, monotono e statisticamente solidissimo (Mann-Kendall, p < 0,001 su tutte le 18
combinazioni testate tra metriche, sessi e finestre temporali). La Fig. 2 mostra la stessa storia
raccontata dall'entropia: un minimo relativo negli anni del baby boom, poi una salita quasi
ininterrotta.

Sulla finestra comparabile 1999-2024 (Fig. 5), l'Italia parte più concentrata degli Stati Uniti e
resta più concentrata per tutti i 26 anni osservati, sia guardando ai primi 10 sia ai primi 50 nomi: il
test di Wilcoxon a coppie appaiate è fortemente significativo a entrambe le soglie (p = 2,98 × 10⁻⁸,
statistica pari a 0 su 26 confronti in tutti e quattro i casi sesso/soglia). Detto in altri termini:
non c'è stato un solo anno, in un quarto di secolo, in cui l'Italia sia stata meno concentrata degli
USA, indipendentemente da quanti nomi si contano.

L'analisi quantitativa evidenzia inoltre una marcata asimmetria strutturale tra i sessi in entrambi i contesti nazionali: i nomi femminili mostrano storicamente tassi di diversificazione e turnover significativamente superiori rispetto a quelli maschili. Negli Stati Uniti, la quota primi-50 per le femmine scende dal 53,2% nel 1880 a meno dell'11,4% nel 2025 (pendenza di Sen pari a $-0,0048$/anno, $p < 0,001$), mentre per i maschi la quota scende dal 61,5% al 15,2% (pendenza di Sen pari a $-0,0041$/anno). Questa maggiore variabilità femminile riflette una minore pressione tradizionale all'ereditarietà del nome di famiglia (come la trasmissione del nome del padre o del nonno) ed una maggiore permeabilità alle mode culturali emergenti.

Quello che cambia, ed è più interessante, è la *velocità* con cui il divario tra i due paesi si muove, dove l'analisi di robustezza sulle soglie di concentrazione (Top-10 vs Top-50 vs Top-100) rivela una sfumatura cruciale.
Per i nomi femminili il quadro è coerente a entrambe le soglie: l'Italia diversifica significativamente più in fretta degli USA (pendenza di Sen primi-10: −0,0033/anno contro −0,0011/anno degli USA; primi-50: −0,0041/anno contro −0,0028/anno; intervalli **non** sovrapposti in entrambi i casi, serie differenza con trend crescente significativo sia a primi-10 ($p = 1,6 \times 10^{-5}$) sia a primi-50 ($p = 4,8 \times 10^{-3}$)): il divario femminile si sta chiudendo, ed è un risultato robusto rispetto a quale soglia di concentrazione si usa.

Per i nomi maschili, invece, il risultato dipende dalla soglia scelta. Ai primi 10 nomi le pendenze di Sen tra i due paesi sono statisticamente indistinguibili (USA −0,0020/anno, Italia −0,0023/anno, intervalli sovrapposti, serie differenza senza trend significativo, $p = 0,078$): il divario appare stabile nei primissimi posti della classifica. Ai primi 50 nomi, però, gli Stati Uniti diversificano significativamente più in fretta dell'Italia (USA −0,0064/anno contro Italia −0,0055/anno, intervalli **non** sovrapposti, serie differenza con trend decrescente significativo, $p = 5,0 \times 10^{-7}$): a questa soglia il divario maschile starebbe leggermente allargandosi. Questa differenza suggerisce che, sebbene le famiglie tradizionali in entrambi i paesi mantengano modelli di concentrazione simili nei primissimi posti della classifica maschile, la popolazione americana diversifica le proprie scelte nella "pancia" della distribuzione (Top-50) molto più velocemente di quella italiana. Il risultato femminile è quindi robusto alla soglia, mentre quello maschile evidenzia una differente dinamica di posizione in classifica.

### I due paesi si stanno anche avvicinando tra loro

Questa è, probabilmente, la scoperta più interessante di tutta la parte "backbone" del lavoro, e in un certo senso risponde a una domanda diversa dalla precedente: non "quanto è concentrato ciascun paese" ma "quanto USA e Italia scelgono *gli stessi* nomi." Misurando la similarità coseno tra le distribuzioni complete di nomi dei due paesi, anno per anno e per sesso (Fig. 6), il trend è netto e statisticamente fortissimo per entrambi i sessi: per i maschi la similarità triplica quasi (da 0,066 a 0,176 tra il 1999 e il 2024, $p = 2,4 \times 10^{-12}$, $\tau$ di Kendall pari a 0,98 — quasi perfettamente monotono), per le femmine più che raddoppia (da 0,119 a 0,302, $p = 2,8 \times 10^{-11}$). Un esempio concreto vale più di una statistica: Liam e Noah, entrambi assenti dalla top-30 italiana nel 1999, ci sono entrati stabilmente entro il 2024 — nomi di chiara origine anglo-americana che attraversano il confine culturale.

### Event Study Confermativo sugli Impatti Mediatici (RQ2)

Per superare l'approccio puramente esplorativo e prevenire obiezioni di *HARKing* (ipotesi fatte a posteriori), l'analisi di RQ2 è stata condotta tramite un **Event Study quantitativo confermativo su un campione complessivo di $N = 152$ eventi mediatici oggettivamente documentati** tra il 1999 e il 2024 (estratti da archivi ufficiali Box Office Mojo, Cinetel, Billboard Hot 100, FIMI Top of the Music, Auditel, FIFA e Lega Serie A).

Per ciascun nome esposto, l'algoritmo ha calcolato la variazione relativa della frequenza pre-post evento e la ha confrontata con la variazione *mediana* di tutti i nomi di controllo non esposti dello stesso sesso e paese con frequenza pre-evento entro il ±35% di quella del nome esposto (metodo *Difference-in-Differences*, DiD).

Come sintetizzato nella **Tabella 18** e visibile nella **Fig. 7**, l'esito complessivo dell'Event Study conferma un impatto causale delle esposizioni mediatiche di massa su scala globale (test di Wilcoxon per ranghi con segno complessivo: $W = 2954,5, p = 1,44 \times 10^{-7}$).

L'analisi comparativa tra categorie mediatiche rivela tuttavia una netta differenza sociologica:

1. **Cinema & Serie TV ($N=71$)**: I personaggi della finzione cinematografica e televisiva (es. *Elsa*, *Khaleesi*, *Katniss*, *Rey*, *Sole*, *Chanel*) producono uno shock culturale massivo, con un impatto netto medio DiD del **$+232,2\%$** rispetto ai controlli ($p = 5,56 \times 10^{-5}$, altamente significativo).
2. **Musica & Pop Culture ($N=46$)**: Le icone della musica pop e i protagonisti dello spettacolo (es. *Aaliyah*, *Kesha*, *Elodie*, *Soleil*, *Blanco*) generano un impatto netto medio DiD del **$+244,9\%$** rispetto ai controlli ($p = 5,44 \times 10^{-4}$, altamente significativo).
3. **Sport ($N=35$)**: I campioni sportivi (es. vincitori dei Mondiali di calcio o campioni NBA) registrano un impatto netto medio DiD del $+76,2\%$, ma il test statistico aggregato mostra che l'effetto **non è statisticamente significativo sull'intera popolazione** ($p = 0,190$).

Per verificare l'ipotesi di adozione strutturale permanente ($H_{2b}$), l'analisi dell'Event Study è stata condotta lungo un orizzonte temporale post-evento di 5 anni ($t+1, t+3, t+5$). Per la finzione cinematografica e televisiva, l'effetto netto DiD si mantiene elevato e statisticamente significativo anche a 5 anni dalla prima esposizione ($+184,5\%$ a $t+5$, $p = 2,1 \times 10^{-4}$), evidenziando un'assimilazione culturale duratura che va oltre l'effetto novità. Al contrario, per la categoria dello sport, l'effetto mostra un rapido decadimento già a 3 anni dall'evento ($+21,3\%$ a $t+3$, $p = 0,412$), riassorbendosi verso la linea di base dei controlli appaiati.

Questa tripartizione suggerisce una differenza sociologica interessante tra categorie: i personaggi della **finzione narrativa** e i **miti della musica** sono associati a un impatto molto più marcato e diffuso rispetto alle imprese degli atleti, che generano ammirazione momentanea ma raramente si traducono in un cambiamento generalizzato delle scelte anagrafiche. Un'ipotesi di lettura plausibile è che i personaggi fittizi offrano ai genitori un veicolo più diretto per esprimere desideri di unicità; restiamo tuttavia nel campo dell'interpretazione, non di una conclusione causale sui meccanismi psicologici individuali.

### Tredici storie di picchi ed il roster esplorativo supplementare

Accanto all'Event Study confermativo, l'analisi esplorativa meccanica (Tabella 16 in Appendice, 87 righe) e la ricerca sul campo hanno confermato storie emblematiche sia in USA che in Italia.

Tra i casi statunitensi più eclatanti: da Shirley Temple (1935) a Tammy (*Tammy and the Bachelor*, 1957, passato da 255 a quasi 10.000 nascite), fino a Nevaeh ("heaven" al contrario, esploso dopo un'apparizione su MTV nel 2000).

Sul lato italiano spiccano: **Karol**, aumentato di 78 volte nel 2005 (in coincidenza con la morte di Papa Giovanni Paolo II, Karol Wojtyła, e la trasmissione della fiction TV a lui dedicata); **Adele**, che mostra il ritardo temporale di recepimento culturale tra USA (2011) e Italia (2012); **Elodie** (Sanremo 2017); **Soleil** (*Grande Fratello Vip* 2021); e **Chanel** (2007, nascita della figlia di Totti e Blasi abbinata al fascino del brand).

### E quando un nome "brucia": i crolli

Meno raccontata in letteratura, ma altrettanto interessante, è la domanda opposta: un evento *negativo* può far crollare l'uso di un nome? La risposta, sui quattro casi che abbiamo verificato, è sì, e in modo piuttosto drammatico. Il caso più eclatante è **Hillary/Hilary**: negli Stati Uniti, 1992 è l'ultimo anno "normale" per il nome; nel 1993, l'anno in cui Hillary Clinton diventa First Lady e si trova immediatamente al centro di una battaglia politica polarizzante sulla riforma sanitaria, l'uso del nome crolla del 58% in dodici mesi, per poi perdere il 90% complessivo entro il 1999 — uno dei cali più ripidi mai registrati nei dati SSA, e uno dei pochi casi in cui un nome *scende* più velocemente di quanto sia salito, invertendo il pattern tipico delle mode onomastiche. **Kobe** crolla nel 2003-2004, in coincidenza con l'accusa di aggressione sessuale contro Kobe Bryant. **Alexa** inizia un declino marcato dal 2015, il cosiddetto "effetto Alexa": da quando Amazon ha lanciato l'assistente vocale Echo, sempre più genitori evitano il nome per non associare la propria figlia a un dispositivo che "obbedisce a comando" — un fenomeno ampiamente documentato dalla stampa internazionale, con casi di bambine prese in giro a scuola.

Sul lato italiano, il caso verificato è **Erica**, che dimezza il proprio uso tra il 1999 e il 2002 (863 nascite nel 1999, 416 nel 2002). La tempistica coincide in modo preciso con il delitto di Novi Ligure: nel febbraio 2001 Erika De Nardo, sedici anni, uccide la madre e il fratellino insieme al fidanzato — uno dei casi di cronaca nera più seguiti degli anni 2000 in Italia, con il processo che tiene banco sui media fino alla sentenza d'appello di maggio 2002, esattamente il periodo in cui il calo del nome si aggrava ulteriormente.

Un secondo candidato italiano, **Enrica** (nome foneticamente vicino a Erica), è stato considerato ma scartato dal roster finale: il suo declino, per quanto reale, prosegue in modo lineare ben oltre il 2002, il che lo rende più coerente con un lento tramonto di moda già in corso che con un effetto puntuale legato al caso di cronaca.

### Un controllo di realtà: gli stati sono tutti d'accordo?

Per i casi-studio più solidi (sei positivi, tre negativi — tutti americani, poiché non esistono dati regionali italiani comparabili), abbiamo verificato se il salto o il crollo osservato a livello nazionale fosse effettivamente diffuso su tutto il paese, o concentrato in poche zone (Fig. 8, Tabella 15). La logica è semplice: un vero evento mediatico nazionale — un film, un programma TV visto ovunque — dovrebbe muovere la maggior parte degli stati nella stessa direzione; un effetto concentrato in uno o due stati soli sarebbe un campanello d'allarme per una causa regionale o, peggio, per una coincidenza statistica. Sette casi su nove superano il 90% di stati concordanti (Jaime al 100%, Kobe e Alexa al 97%), il che ci dà una certa fiducia che questi non siano artefatti isolati. Le due eccezioni sono interessanti di per sé: Jaslene (79%) è compatibile con un'adozione inizialmente più forte nelle aree a maggiore presenza ispanica, coerente con il fatto che fu la prima vincitrice ispanica del programma; Hillary (74%) è compatibile con una polarizzazione politica che, ragionevolmente, non ha colpito ogni stato allo stesso modo.

### Le storie in comune tra i due paesi

Infine, quattro casi che permettono un confronto diretto tra USA e Italia sullo stesso evento. **Celine Dion** è forse il più istruttivo: la sua diagnosi di sindrome della persona rigida (annunciata a dicembre 2022) e il documentario che ne è seguito (giugno 2024) hanno prodotto una crescita graduale del nome negli USA (da 614 a 1.466 nascite tra il 2018 e il 2025) ma un'impennata molto più marcata in Italia (fino a 6 volte il livello di base) — stessa causa, magnitudine molto diversa, probabilmente perché il nome partiva da una base molto più piccola in Italia. **Elsa**, dopo *Frozen*, è reale in entrambi i paesi ma arriva in Italia con circa un anno di ritardo (il film uscì lì a dicembre 2013) e con un'ampiezza molto più contenuta. **Khaleesi** resta invece un fenomeno puramente americano: non compare mai nei dati italiani catturati, nemmeno negli anni a copertura completa. **Isabella**, dopo *Twilight*, è il caso più ambiguo: cresce in entrambi i paesi, ma in Italia la crescita comincia *prima* dell'uscita della saga e prosegue senza scosse anche dopo — probabilmente perché Isabella è già un nome classico italiano, e quindi le due curve, per quanto visivamente simili, raccontano storie causali diverse.

### Una tabella esaustiva, non solo i casi scelti a mano

Per non dare l'impressione di aver scelto solo gli esempi più belli da raccontare, abbiamo anche generato una tabella puramente meccanica di ogni nome/anno che supera una soglia di crescita fissata a priori (USA: rapporto ≥6x e conteggio finale ≥2.000; Italia: rapporto ≥2,5x e conteggio ≥150) — 87 righe in tutto (48 USA, 39 Italia), senza alcuna selezione manuale. Le tredici storie curate qui sopra sono un sottoinsieme di questa base più ampia, non un'eccezione ad essa.

### Divergenza nei Ruoli di Genere Anagrafici: Nomi Gender-Neutral (RQ3)

La terza domanda di ricerca (RQ3) analizza se il processo di individualizzazione e l'evoluzione delle norme di genere abbiano portato ad un aumento dei **nomi gender-neutral (unissex)**, ovvero attribuiti sia a nati maschi che femmine ($0,10 \le p_F \le 0,90$).

Come sintetizzato nella **Tabella 19** e nella **Fig. 9**, si osserva una drastica divergenza strutturale tra i due paesi:

1. **Stati Uniti (USA)**: La quota di nascite con nomi neutri rispetto al sesso è cresciuta dal **$7,31\%$** nel 1999 all'**$8,81\%$** nel 2024 (test di Mann-Kendall: $\tau = 0,526, p = 1,79 \times 10^{-4}$, altamente significativo). Nomi come *Avery*, *Riley*, *Jordan*, *Charlie*, *Taylor*, *Peyton*, *Morgan* e *Quinn* sono entrati stabilmente nell'uso comune.
2. **Italia (IT)**: La quota di nascite con nomi unissex rimane estremamente limitata, passando da uno **$0,06\%$** nel 1999 allo **$0,22\%$** nel 2024 (test di Mann-Kendall: $\tau = 0,031, p = 0,842$, non significativo).

Questa drastica divergenza tra l'incremento dei nomi gender-neutral negli Stati Uniti ($7,31\% \to 8,81\%$) e la loro sostanziale assenza in Italia ($<0,22\%$) affonda le sue radici probabilmente in due fattori strutturali: la morfologia linguistica e l'architettura giuridico-normativa.

Dal punto di vista linguistico, la lingua italiana possiede una struttura flessiva con forte marcatura di genere fonetico, in cui la desinenza in *-o* identifica quasi univocamente la maschilità e quella in *-a* la femminilità (con pochissime eccezioni tradizionali come Andrea o Mattia). Al contrario, la lingua inglese presenta una struttura fonetica non flessiva che facilita l'attribuzione di nomi neutri o l'adozione di cognomi storici come primi nomi (*Avery*, *Riley*, *Jordan*, *Peyton*, *Quinn*).

Dal punto di vista normativo, l'ordinamento giuridico italiano ha storicamente esercitato un controllo rigido attraverso l'Art. 35 del DPR 396/2000, il quale stabiliva tassativamente che il nome imposto al bambino dovesse corrispondere al sesso biologico indicato nell'atto di nascita. Sebbene sentenze recenti abbiano progressivamente attenuato questo vincolo (consentendo ad esempio l'attribuzione del nome Andrea alle femmine), la persistenza delle prassi anagrafiche e la sensibilità culturale tradizionale hanno mantenuto l'onomastica italiana ancorata ad una rigorosa binarietà di genere.

## Discussione Finale

Il quadro che emerge da questo lavoro racconta una storia coerente attraverso le tre domande di ricerca (diversità di lungo periodo RQ1, impatti mediatici RQ2, ed evoluzione delle norme di genere RQ3).
In tutti e tre i casi, il filo conduttore è lo stesso: la scelta del nome di un figlio, per quanto intima, resta sistematicamente esposta a forze culturali che vanno ben oltre il singolo nucleo familiare, tra cui grandi cambiamenti generazionali di valori (la diversificazione di lungo periodo, coerente con la tesi di Twenge et al. sull'aumento dell'individualismo), la globalizzazione dei media (la convergenza USA-Italia, con nomi anglo-americani come Liam e Noah che attraversano l'Atlantico), l'impatto causale della finzione narrativa e della musica pop, ed il superamento progressivo dei ruoli tradizionali di genere negli USA rispetto all'Italia (RQ3).

Un punto che vale la pena riprendere esplicitamente qui è quello, già accennato in Metodologie, sull'asimmetria tra le due infrastrutture statistiche nazionali. Gli Stati Uniti pubblicano l'intera distribuzione dei nomi in un archivio aperto, aggiornato annualmente, ricco dal 1880. L'Italia non pubblica nulla del genere: i dati usati in questo lavoro esistono solo perché raggiungibili tramite un servizio web non documentato, pensato per un tool di consultazione singola, non per la ricerca. Non è un dettaglio tecnico neutro — è, a suo modo, un dato culturale: riflette due approcci molto diversi alla trasparenza dei dati pubblici, che meriterebbe una riflessione a sé.

## Conclusioni

In questo studio è stata analizzata l'evoluzione dell'onomastica in prospettiva transatlantica, mettendo a confronto l'esperienza degli Stati Uniti (1880–2025) e dell'Italia (1999–2024). L'indagine empirica evidenzia come la diversità dei nomi mostri una crescita sistematica di lungo periodo in entrambi i paesi, accompagnata da una progressiva riduzione del divario di concentrazione nella popolazione femminile e da una convergenza distributiva globale alimentata dai flussi culturali transnazionali (RQ1). Al contempo, gli shock mediatici legati alla finzione cinematografica e alla musica pop esercitano un impatto causale significativo e duraturo sulle scelte anagrafiche, a differenza delle imprese sportive la cui influenza appare più contenuta e circoscritta (RQ2). Infine, l'analisi dei nomi *gender-neutral* fa emergere una drastica divergenza socio-normativa, evidenziando una crescita costante del fenomeno negli Stati Uniti a fronte di una sostanziale stabilità su valori marginali in Italia (RQ3). Nel complesso, i risultati suggeriscono come le decisioni anagrafiche costituiscano un rilevante indicatore quantitativo per misurare l'evoluzione dei valori culturali e l'impatto dei media nelle società contemporanee.

## Bibliografia

> **Correzione**: la voce Mann (1945) nella versione precedente di questa bozza riportava le pagine
> 163-171 a memoria — sbagliato. Il numero corretto, confermato da più fonti indipendenti (Cambridge
> Core, Econometric Society, Semantic Scholar), è **245-259**. Corretto qui sotto.

- Mann, H.B. (1945). "Nonparametric Tests Against Trend." *Econometrica*, 13(3), 245–259.
  DOI: [10.2307/1907187](https://doi.org/10.2307/1907187).
- Kendall, M.G. (1975). *Rank Correlation Methods*, 4ª ed. Londra: Charles Griffin. (Nessun ISBN
  univoco reperito per la 4ª edizione del 1975 nello specifico — le fonti trovate citano ISBN legati a
  edizioni precedenti; da verificare in biblioteca se serve un riferimento preciso.)
- Wilcoxon, F. (1945). "Individual Comparisons by Ranking Methods." *Biometrics Bulletin*, 1(6), 80-83.
  DOI: [10.2307/3001968](https://doi.org/10.2307/3001968).
- Lieberson, S. & Bell, E.O. (1992). "Children's First Names: An Empirical Study of Social Taste."
  *American Journal of Sociology*, 98(3), 511-554. DOI:
  [10.1086/230048](https://doi.org/10.1086/230048).
- Twenge, J.M., Abebe, E.M., & Campbell, W.K. (2010). "Fitting In or Standing Out: Trends in American
  Parents' Choices for Children's Names, 1880-2007." *Social Psychological and Personality Science*,
  1(1), 19-25. DOI: [10.1177/1948550609349515](https://doi.org/10.1177/1948550609349515).
- Twenge, J.M., Dawson, L., & Campbell, W.K. (2016). "Still Standing Out: Children's Names in the
  United States During the Great Recession and Correlations with Economic Indicators." *Journal of
  Applied Social Psychology*, 46, 663-670. DOI:
  [10.1111/jasp.12409](https://doi.org/10.1111/jasp.12409). (Nomi degli autori completati — la
  versione precedente diceva genericamente "et al.".)
- Ogihara, Y. (2025). "Popularity and Diversity: The Negative Relationship in Baby Names in the United
  Kingdom." *F1000Research*, 14, 424. DOI:
  [10.12688/f1000research.162476.1](https://doi.org/10.12688/f1000research.162476.1).
- Fan, Z., Thouzeau, V., de Dampierre, C., Chevallier, C., & Baumard, N. (2025). "Name Uniqueness and
  the Rise of Individualism in the Western Hemisphere (1500-2000)." *Current Research in Ecological
  and Social Psychology*, vol. 9, art. 100235. DOI:
  [10.1016/j.cresp.2025.100235](https://doi.org/10.1016/j.cresp.2025.100235).
- UK Office for National Statistics (2015). "10 Pop Culture Influences on Baby Names: Game of Thrones,
  Marvel, Frozen and more." A cura di Tom Davy e Rachel Lewis, pubblicato il 17 agosto 2015.
  [ons.gov.uk](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths/articles/10popcultureinfluencesonbabynamesgameofthronesmarvelfrozenandmore/2015-08-17).

## Repository e riproducibilità

Codice, dati grezzi ed elaborati, figure e tabelle sono disponibili nel repository del progetto:
`https://github.com/matteraggi/HDS_evolution_of_naming`. Si veda `README.md` per gli step di
riproduzione completi e `PROJECT_LOG.md` per il log cronologico di tutte le decisioni prese durante il
lavoro.
