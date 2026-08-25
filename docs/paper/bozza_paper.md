> **Nota**: questa è una bozza molto iniziale, scritta per avere una struttura completa su cui
> lavorare e per non perdere nulla di quello che abbiamo fatto finora. Non è il testo finale — mancano
> ancora RQ3 (nomi neutri rispetto al genere, non ancora iniziata), una revisione linguistica seria, il
> conteggio parole definitivo e probabilmente un giro di tagli. La sezione Metodologie/Dati è già
> abbastanza matura (vedi `metodologie_dati_DRAFT.md`, di cui questa è una versione integrata); il
> resto è più abbozzato. I punti dove serve ancora lavoro sono segnati con **[DA FARE]**.

# L'Evoluzione dei Nomi: Diversità Culturale, Influenza dei Media e Individualismo nei Nomi dei Neonati (USA vs. Italia)

## Abstract

Questo lavoro studia come la diversità dei nomi dati ai neonati sia cambiata nel tempo negli Stati
Uniti (1880-2025) e in Italia (1999-2024), e cosa succede quando si confrontano i due paesi sulla
finestra che hanno in comune. La domanda di fondo è semplice da porre e meno semplice da rispondere:
scegliere il nome di un figlio è una delle decisioni più personali che esistano, eppure sembra
seguire pattern collettivi — mode che nascono, crescono, muoiono, e a volte crollano di colpo per una
ragione precisa. Usando la quota di concentrazione dei nomi più popolari come metrica principale
(validata empiricamente, non solo teoricamente), troviamo che entrambi i paesi si stanno
diversificando in modo statisticamente robusto (Mann-Kendall, p < 0,001 in ogni combinazione
testata), che l'Italia resta sistematicamente più concentrata degli USA in ogni singolo anno
osservato, ma che le due popolazioni di nomi si stanno anche avvicinando tra loro (similarità coseno
sull'intera distribuzione, p < 3 × 10⁻¹¹ per entrambi i sessi). Accanto a questo, raccogliamo e
verifichiamo 13 casi di "salto" onomastico legato a un evento culturale positivo (da *Frozen* a
Sanremo) e 4 casi di crollo legato a un evento negativo (da Hillary Clinton a un caso di cronaca
nera italiano), ognuno controllato singolarmente per plausibilità causale e coerenza temporale, e
per i casi più solidi anche per uniformità geografica.

**Parole chiave:** diversità onomastica, individualismo culturale, test di Mann-Kendall, event study, nomi dei neonati, confronto USA-Italia

## Introduzione

Scegliere il nome di un figlio è, probabilmente, una delle decisioni più intime che un genitore
possa prendere. Eppure basta guardare i dati per accorgersi che non è affatto una decisione isolata:
milioni di genitori, senza parlarsi, finiscono per convergere sugli stessi pochi nomi in certi anni,
e per abbandonarli in blocco pochi anni dopo. Questo paper nasce dalla curiosità di capire quanto di
"individuale" resti davvero in una scelta che sembra così personale, e quanto invece sia guidato da
forze esterne — la cultura di massa, un film, uno scandalo, un'epoca.

**[DA FARE — nota per la stesura finale]**: qui va la contestualizzazione con la letteratura esistente
(Lieberson & Bell 1992, Twenge et al. 2010, Ogihara 2025 — già confermati e citati in Bibliografia) e la
motivazione della scelta del tema rispetto ad alternative scartate (bias nei sistemi di
raccomandazione, teoria dell'onnivoro culturale con dati GSS) già discusse nel piano di ricerca
originale. Di seguito una versione provvisoria.

I dati sui nomi alla nascita sono un terreno relativamente poco battuto nella didattica di questo
tipo di corsi, il che ci ha dato margine per un'analisi originale piuttosto che una replica. Il primo
studio sistematico sull'argomento (Lieberson & Bell, 1992) inquadra la scelta del nome come un caso "puro" di
moda: a differenza dei vestiti o della musica, non c'è un'industria che spinge attivamente un nome
piuttosto che un altro, il che rende il fenomeno un osservatorio quasi di laboratorio su come le mode
nascono e muoiono per conto proprio. Twenge et al. (2010) hanno poi collegato il calo di uso dei nomi
comuni negli USA a un aumento più ampio dell'individualismo nella cultura americana, usando
esattamente gli stessi dati SSA che usiamo qui. Ogihara (2025) ha validato, sui dati del Regno Unito,
l'uso della quota di concentrazione dei nomi più popolari come proxy affidabile di diversità
onomastica anche quando la distribuzione completa non è disponibile — un punto che si è rivelato
centrale per questo lavoro, come si vedrà in Metodologie/Dati.

L'aspetto comparativo USA/Italia è il principale elemento di originalità di questo paper: la
letteratura esistente si concentra quasi sempre su un solo paese, e non abbiamo trovato alcuno studio
peer-reviewed sulla diversità dei nomi italiani nel tempo — un vuoto che questo lavoro prova a
colmare, pur con i limiti di un progetto universitario piuttosto che di una ricerca professionale.

Il lavoro è organizzato attorno a tre domande, di cui la seconda ha finito per diventare il filo
conduttore del paper:

1. **Diversità nel tempo**: la diversità dei nomi sta aumentando in entrambi i paesi? I due paesi si
   stanno anche avvicinando tra loro nelle scelte effettivamente fatte, o restano due mondi separati?
2. **Eventi culturali**: un film, una canzone, uno scandalo possono davvero far impennare o crollare
   l'uso di un nome specifico, in modo misurabile? Succede allo stesso modo nei due paesi?
3. **Nomi neutri rispetto al genere**: l'uso di nomi non marcati per genere sta aumentando? **[DA FARE
   — Person B, non ancora iniziata]**

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

Quello che cambia, ed è più interessante, è la *velocità* con cui il divario si muove, e qui il
risultato dipende dalla soglia scelta. Per i nomi femminili il quadro è coerente a entrambe le soglie:
l'Italia diversifica significativamente più in fretta degli USA (pendenza di Sen primi-10: −0,0033/anno
contro −0,0011/anno degli USA; primi-50: −0,0041/anno contro −0,0028/anno; intervalli **non**
sovrapposti in entrambi i casi, serie differenza con trend crescente significativo sia a primi-10
(p = 1,6 × 10⁻⁵) sia a primi-50 (p = 4,8 × 10⁻³)): il divario femminile si sta chiudendo, ed è un
risultato robusto rispetto alla soglia usata.

Per i nomi maschili, invece, il risultato dipende dalla soglia. Ai primi 10 nomi le pendenze di Sen
sono statisticamente indistinguibili (USA −0,0020/anno, Italia −0,0023/anno, intervalli sovrapposti,
serie differenza senza trend significativo, p = 0,078): il divario appare stabile. Ai primi 50 nomi,
però, gli Stati Uniti diversificano significativamente più in fretta dell'Italia (USA −0,0064/anno
contro Italia −0,0055/anno, intervalli **non** sovrapposti, serie differenza con trend decrescente
significativo, p = 5,0 × 10⁻⁷): a questa soglia il divario maschile starebbe leggermente allargandosi.
Il risultato femminile è quindi robusto rispetto alla scelta della soglia, quello maschile no.

### I due paesi si stanno anche avvicinando tra loro

Questa è, probabilmente, la scoperta più interessante di tutta la parte "backbone" del lavoro, e in un
certo senso risponde a una domanda diversa dalla precedente: non "quanto è concentrato ciascun paese"
ma "quanto USA e Italia scelgono *gli stessi* nomi." Misurando la similarità coseno tra le distribuzioni
complete di nomi dei due paesi, anno per anno e per sesso (Fig. 6), il trend è netto e
statisticamente fortissimo per entrambi i sessi: per i maschi la similarità triplica quasi (da 0,066 a
0,176 tra il 1999 e il 2024, p = 2,4 × 10⁻¹², τ di Kendall pari a 0,98 — quasi perfettamente
monotono), per le femmine più che raddoppia (da 0,119 a 0,302, p = 2,8 × 10⁻¹¹). Un esempio concreto
vale più di una statistica: Liam e Noah, entrambi assenti dalla top-30 italiana nel 1999, ci sono
entrati stabilmente entro il 2024 — nomi di chiara origine anglo-americana che attraversano il
confine culturale.

### Event Study Confermativo sugli Impatti Mediatici (RQ2)

Per superare l'approccio puramente esplorativo e prevenire obiezioni di *HARKing* (ipotesi fatte a posteriori), l'analisi di RQ2 è stata condotta tramite un **Event Study quantitativo confermativo su un campione complessivo di $N = 152$ eventi mediatici oggettivamente documentati** tra il 1999 e il 2024 (estratti da archivi ufficiali Box Office Mojo, Cinetel, Billboard Hot 100, FIMI Top of the Music, Auditel, FIFA e Lega Serie A).

Per ciascun nome esposto, l'algoritmo ha calcolato la variazione relativa della frequenza pre-post evento e la ha confrontata con la variazione *mediana* di tutti i nomi di controllo non esposti dello stesso sesso e paese con frequenza pre-evento entro il ±35% di quella del nome esposto (metodo *Difference-in-Differences*, DiD).

Come sintetizzato nella **Tabella 18** e visibile nella **Fig. 7**, l'esito complessivo dell'Event Study conferma un impatto causale delle esposizioni mediatiche di massa su scala globale (test di Wilcoxon per ranghi con segno complessivo: $W = 2954,5, p = 1,44 \times 10^{-7}$).

L'analisi comparativa tra categorie mediatiche rivela tuttavia una netta differenza sociologica:

1. **Cinema & Serie TV ($N=71$)**: I personaggi della finzione cinematografica e televisiva (es. *Elsa*, *Khaleesi*, *Katniss*, *Rey*, *Sole*, *Chanel*) producono uno shock culturale massivo, con un impatto netto medio DiD del **$+232,2\%$** rispetto ai controlli ($p = 5,56 \times 10^{-5}$, altamente significativo).
2. **Musica & Pop Culture ($N=46$)**: Le icone della musica pop e i protagonisti dello spettacolo (es. *Aaliyah*, *Kesha*, *Elodie*, *Soleil*, *Blanco*) generano un impatto netto medio DiD del **$+244,9\%$** rispetto ai controlli ($p = 5,44 \times 10^{-4}$, altamente significativo).
3. **Sport ($N=35$)**: I campioni sportivi (es. vincitori dei Mondiali di calcio o campioni NBA) registrano un impatto netto medio DiD del $+76,2\%$, ma il test statistico aggregato mostra che l'effetto **non è statisticamente significativo sull'intera popolazione** ($p = 0,190$).

Questa tripartizione suggerisce una differenza sociologica interessante tra categorie: i personaggi della **finzione narrativa** e i **miti della musica** sono associati a un impatto molto più marcato e diffuso rispetto alle imprese degli atleti, che generano ammirazione momentanea ma raramente si traducono in un cambiamento generalizzato delle scelte anagrafiche. Un'ipotesi di lettura plausibile è che i personaggi fittizi offrano ai genitori un veicolo più diretto per esprimere desideri di unicità; restiamo tuttavia nel campo dell'interpretazione, non di una conclusione causale sui meccanismi psicologici individuali.

### Tredici storie di picchi ed il roster esplorativo supplementare

Accanto all'Event Study confermativo, l'analisi esplorativa meccanica (Tabella 16 in Appendice, 87 righe) e la ricerca sul campo hanno confermato storie emblematiche sia in USA che in Italia.

Tra i casi statunitensi più eclatanti: da Shirley Temple (1935) a Tammy (*Tammy and the Bachelor*, 1957, passato da 255 a quasi 10.000 nascite), fino a Nevaeh ("heaven" al contrario, esploso dopo un'apparizione su MTV nel 2000).

Sul lato italiano spiccano: **Karol**, aumentato di 78 volte nel 2005 (anno della morte di Papa Giovanni Paolo II); **Adele**, che mostra il ritardo temporale di recepimento culturale tra USA (2011) e Italia (2012); **Elodie** (Sanremo 2017); **Soleil** (*Grande Fratello Vip* 2021); e **Chanel** (2007, nascita della figlia di Totti e Blasi abbinata al fascino del brand).

### E quando un nome "brucia": i crolli

Meno raccontata in letteratura, ma altrettanto interessante, è la domanda opposta: un evento
*negativo* può far crollare l'uso di un nome? La risposta, sui quattro casi che abbiamo verificato, è
sì, e in modo piuttosto drammatico. Il caso più eclatante è **Hillary/Hilary**: negli Stati Uniti,
1992 è l'ultimo anno "normale" per il nome; nel 1993, l'anno in cui Hillary Clinton diventa First
Lady e si trova immediatamente al centro di una battaglia politica polarizzante sulla riforma
sanitaria, l'uso del nome crolla del 58% in dodici mesi, per poi perdere il 90% complessivo entro il
1999 — uno dei cali più ripidi mai registrati nei dati SSA, e uno dei pochi casi in cui un nome
*scende* più velocemente di quanto sia salito, invertendo il pattern tipico delle mode onomastiche.
**Kobe** crolla nel 2003-2004, in coincidenza con l'accusa di aggressione sessuale contro Kobe Bryant.
**Alexa** inizia un declino marcato dal 2015, il cosiddetto "effetto Alexa": da quando Amazon ha
lanciato l'assistente vocale Echo, sempre più genitori evitano il nome per non associare la propria
figlia a un dispositivo che "obbedisce a comando" — un fenomeno ampiamente documentato dalla stampa
internazionale, con casi di bambine prese in giro a scuola.

Sul lato italiano, il caso verificato è **Erica**, che dimezza il proprio uso tra il 1999 e il 2002
(863 nascite nel 1999, 416 nel 2002). La tempistica coincide in modo preciso con il delitto di Novi
Ligure: nel febbraio 2001 Erika De Nardo, sedici anni, uccide la madre e il fratellino insieme al
fidanzato — uno dei casi di cronaca nera più seguiti degli anni 2000 in Italia, con il processo che
tiene banco sui media fino alla sentenza d'appello di maggio 2002, esattamente il periodo in cui il
calo del nome si aggrava ulteriormente.

Un secondo candidato italiano, **Enrica** (nome foneticamente vicino a Erica), è stato considerato ma
scartato dal roster finale: il suo declino, per quanto reale, prosegue in modo lineare ben oltre il
2002, il che lo rende più coerente con un lento tramonto di moda già in corso che con un effetto
puntuale legato al caso di cronaca.

### Un controllo di realtà: gli stati sono tutti d'accordo?

Per i casi-studio più solidi (sei positivi, tre negativi — tutti americani, poiché non esistono dati
regionali italiani comparabili), abbiamo verificato se il salto o il crollo osservato a livello
nazionale fosse effettivamente diffuso su tutto il paese, o concentrato in poche zone (Fig. 8,
Tabella 15). La logica è semplice: un vero evento mediatico nazionale — un film, un programma TV
visto ovunque — dovrebbe muovere la maggior parte degli stati nella stessa direzione; un effetto
concentrato in uno o due stati soli sarebbe un campanello d'allarme per una causa regionale o, peggio,
per una coincidenza statistica. Sette casi su nove superano il 90% di stati concordanti (Jaime al
100%, Kobe e Alexa al 97%), il che ci dà una certa fiducia che questi non siano artefatti isolati. Le
due eccezioni sono interessanti di per sé: Jaslene (79%) è compatibile con un'adozione inizialmente
più forte nelle aree a maggiore presenza ispanica, coerente con il fatto che fu la prima vincitrice
ispanica del programma; Hillary (74%) è compatibile con una polarizzazione politica che, ragionevolmente,
non ha colpito ogni stato allo stesso modo.

### Le storie in comune tra i due paesi

Infine, quattro casi che permettono un confronto diretto tra USA e Italia sullo stesso evento. **Celine
Dion** è forse il più istruttivo: la sua diagnosi di sindrome della persona rigida (annunciata a
dicembre 2022) e il documentario che ne è seguito (giugno 2024) hanno prodotto una crescita graduale
del nome negli USA (da 614 a 1.466 nascite tra il 2018 e il 2025) ma un'impennata molto più marcata in
Italia (fino a 6 volte il livello di base) — stessa causa, magnitudine molto diversa, probabilmente
perché il nome partiva da una base molto più piccola in Italia. **Elsa**, dopo *Frozen*, è reale in
entrambi i paesi ma arriva in Italia con circa un anno di ritardo (il film uscì lì a dicembre 2013) e
con un'ampiezza molto più contenuta. **Khaleesi** resta invece un fenomeno puramente americano: non
compare mai nei dati italiani catturati, nemmeno negli anni a copertura completa. **Isabella**, dopo
*Twilight*, è il caso più ambiguo: cresce in entrambi i paesi, ma in Italia la crescita comincia
*prima* dell'uscita della saga e prosegue senza scosse anche dopo — probabilmente perché Isabella è già
un nome classico italiano, e quindi le due curve, per quanto visivamente simili, raccontano storie
causali diverse.

### Una tabella esaustiva, non solo i casi scelti a mano

Per non dare l'impressione di aver scelto solo gli esempi più belli da raccontare, abbiamo anche
generato una tabella puramente meccanica di ogni nome/anno che supera una soglia di crescita fissata
a priori (USA: rapporto ≥6x e conteggio finale ≥2.000; Italia: rapporto ≥2,5x e conteggio ≥150) — 87
righe in tutto (48 USA, 39 Italia), senza alcuna selezione manuale. Le tredici storie curate qui sopra
sono un sottoinsieme di questa base più ampia, non un'eccezione ad essa.

## Discussione Finale

**[DA FARE — Person A e Person B insieme]**

Il quadro che emerge da questo lavoro racconta, crediamo, una storia coerente nonostante la sua
struttura a tre livelli (diversità di lungo periodo, convergenza tra paesi, singoli eventi culturali).
In tutti e tre i casi, il filo conduttore è lo stesso: la scelta del nome di un figlio, per quanto
intima, resta sistematicamente esposta a forze che vanno ben oltre il singolo nucleo familiare —
grandi cambiamenti generazionali di valori (la diversificazione di lungo periodo, coerente con la
tesi di Twenge et al. sull'aumento dell'individualismo), la globalizzazione dei media (la
convergenza USA-Italia, con nomi anglo-americani come Liam e Noah che attraversano l'Atlantico), e
momenti culturali specifici e datati (le tredici storie di salto, i quattro crolli).

Un punto che vale la pena riprendere esplicitamente qui è quello, già accennato in Metodologie,
sull'asimmetria tra le due infrastrutture statistiche nazionali. Gli Stati Uniti pubblicano
l'intera distribuzione dei nomi in un archivio aperto, aggiornato annualmente, riccio dal 1880.
L'Italia non pubblica nulla del genere: i dati usati in questo lavoro esistono solo perché
raggiungibili tramite un servizio web non documentato, pensato per un tool di consultazione singola,
non per la ricerca. Non è un dettaglio tecnico neutro — è, a suo modo, un dato culturale: riflette due
approcci molto diversi alla trasparenza dei dati pubblici, che meriterebbe una riflessione a sé.

**[DA FARE]**: qui va anche discusso più esplicitamente il tema dei nomi neutri rispetto al genere
(RQ3) una volta completata quella parte, e va inquadrato meglio il caso "Chanel" come esempio di
cause concorrenti non mutuamente esclusive, già menzionato nei Limiti.

## Conclusioni

**[DA FARE — abbozzo]**

Questo lavoro ha provato a rispondere a una domanda semplice — i nomi dei bambini si stanno
diversificando, e come? — usando due dataset molto diversi per qualità e accessibilità, e ne è uscita
una risposta più ricca di quanto ci aspettassimo all'inizio. La diversità cresce in entrambi i paesi.
L'Italia resta più concentrata, ma il divario femminile si sta chiudendo. Le scelte dei due paesi si
stanno avvicinando, non solo nei numeri aggregati ma in modo tracciabile, nome per nome. E dietro
molte di queste curve statistiche ci sono storie vere e verificabili — un film, una canzone, uno
scandalo — che rendono concreto quello che altrimenti resterebbe solo un trend su un grafico.

Restano aperti dei limiti reali, discussi per esteso in Metodologie: la finestra comparabile è
vincolata al 1999-2024, l'entropia italiana è affidabile solo per tre anni, e il legame tra un evento e
un nome resta per natura correlazionale. Restano anche margini di lavoro concreti: completare RQ3, e
probabilmente affinare ulteriormente il roster di eventi con l'aiuto diretto del professore, dato il
suo interesse specifico per il rigore statistico di questo tipo di verifiche.

## Bibliografia

**[DA FARE — formattazione secondo lo stile richiesto dal corso; verificate via ricerca web il
2026-08-17, non solo a memoria — vedi nota di correzione sotto]**

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
