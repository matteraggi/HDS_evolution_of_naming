# Validazione scientifica, spiegata per la presentazione

Questo file esiste solo per prepararvi all'orale: spiega in italiano semplice cosa dice ogni pezzo
della sezione "Validazione scientifica" del paper, perché è lì, e quanto è importante da difendere a
voce (vs. quanto si può tagliare o accorpare se il tempo stringe). Non è materiale da mettere nel
paper così com'è.

La sezione fa una distinzione centrale che vale la pena tenere a mente sopra tutto il resto: **test di
ipotesi formali** (hanno un H0/H1 dichiarato, un p-value, una soglia alpha=0,05, e quindi una vera
decisione statistica) contro **controlli di robustezza/sensibilità** (non stanno testando un'ipotesi,
stanno chiedendo "se avessi fatto una scelta metodologica diversa, la conclusione sarebbe cambiata?").
Se durante l'orale vi chiedono "questo è un test statistico vero?", la prima cosa da fare è capire in
quale dei due gruppi cade la domanda.

## I quattro test di ipotesi formali (il cuore statistico di RQ1)

Questi quattro sono il nucleo duro: sono nella Tabella "formal_hypotheses" e sono quelli che, se
tagliate, indebolite l'intero paper. **Non tagliare questi.**

**1. Mann-Kendall sul trend USA (backbone).**
Domanda: la concentrazione dei nomi USA (quota primi-10) sta davvero cambiando nel tempo, o è solo
rumore che sale e scende a caso? H0 = nessun trend monotono; H1 = c'è un trend (in questo caso,
decrescente: la concentrazione scende, cioè i nomi si diversificano). Risultato: H0 respinta con
p < 0,001 su tutte le combinazioni testate. In parole povere: è statisticamente fuori discussione che
i nomi USA si stiano diversificando nel tempo, non è un'impressione visiva del grafico.

**2. Mann-Kendall sul trend Italia.**
Stessa identica logica del punto 1, applicata alla serie italiana 1999-2024. H0 respinta, p < 1e-9.
Stesso risultato: anche l'Italia si sta diversificando, in modo statisticamente solido, anche se su
una finestra molto più corta (26 anni contro 145).

**3. Wilcoxon a coppie appaiate, USA vs Italia.**
Domanda diversa dalle prime due: non "il trend nel tempo" ma "chi è più concentrato dei due paesi, in
ciascuno dei 26 anni in cui li possiamo confrontare?". Si prendono i 26 anni comparabili, per ciascuno
si guarda se l'Italia è più o meno concentrata degli USA quell'anno specifico, e si testa se la
mediana di queste differenze è zero. Rifatto sia sui primi 10 sia sui primi 50 nomi: H0 respinta,
p = 2,98e-08, per entrambi i sessi e a entrambe le soglie (lo stesso identico p-value in tutti e
quattro i casi, perché in tutti e quattro l'esito è ugualmente estremo). Il risultato è quasi
impressionante da dire a voce: l'Italia è stata più concentrata degli USA in *tutti e 26* gli anni
osservati, zero eccezioni, indipendentemente da quanti nomi si contano. Non è "l'Italia è mediamente
più concentrata", è "non c'è mai stato un solo anno in cui non lo fosse".

*Domanda che vi siete fatti: può essere un artefatto dell'incompletezza dei dati ISTAT?* No, e questo
è esattamente il motivo per cui il controllo 8 esiste. Il controllo 8 dimostra che le quote primi-10 e
primi-50 (le metriche usate qui) hanno bias *esattamente zero* a ogni profondità di copertura testata,
comprese le profondità più basse in assoluto (137 nomi nel 2021). Il motivo è meccanico, non
statistico: per calcolare "quanto valgono i primi N nomi" basta aver catturato almeno i primi N nomi, e
anche l'anno peggiore (137 catturati) supera abbondantemente sia 10 sia 50. La copertura incompleta è
un problema serio per l'entropia (che ha bisogno dell'intera coda di nomi rari per essere corretta), ma
è strutturalmente irrilevante per una metrica che guarda solo alla testa della distribuzione. Quindi il
risultato del test 3 è reale, non un artefatto di misurazione.

**4. Mann-Kendall sulla similarità coseno USA-Italia (convergenza).**
Domanda ancora diversa: non "quanto è concentrato ciascun paese" ma "quanto USA e Italia scelgono gli
*stessi* nomi, anno dopo anno?". Si misura la similarità coseno tra le due distribuzioni complete di
nomi, anno per anno, e si testa se questa similarità ha un trend nel tempo. H0 respinta per entrambi i
sessi (maschi p = 2,4e-12, tau di Kendall = 0,98 quasi perfettamente monotono; femmine p = 2,8e-11).
Questo è probabilmente il risultato più "sorprendente" da raccontare in presentazione: i due paesi non
solo si diversificano ciascuno per conto proprio, ma stanno anche convergendo tra loro, scegliendo
sempre più spesso gli stessi nomi (esempio concreto pronto all'uso: Liam e Noah, assenti dalla top-30
italiana nel 1999, stabilmente dentro nel 2024).

## Le due serie-differenza (spiegano la *velocità* del gap, non solo che esiste)

Questi due non sono nella tabella formale ma sono comunque veri test Mann-Kendall, con H0/H1 chiari;
sono un livello di dettaglio in più rispetto ai quattro sopra. **Utili da tenere, ma se il tempo
stringe si possono raccontare insieme come un solo risultato ("il divario si comporta diversamente per
maschi e femmine") invece di due test separati.**

**5. Mann-Kendall sulla serie differenza USA−Italia, maschi.**
Si prende, anno per anno, quanto l'Italia è più concentrata degli USA (la differenza), e si chiede se
questa differenza ha un trend. Qui il risultato *dipende dalla soglia*, e questo è uno dei punti più
interessanti da avere pronti per l'orale: ai primi 10 nomi H0 *non* è respinta (p = 0,078), il gap
sembra stabile; ai primi 50 nomi H0 *è* respinta (p = 5,0e-7), e il gap risulta in leggero
*allargamento* (gli USA diversificano più in fretta dell'Italia in questa finestra specifica). Non
abbiamo nascosto questa discrepanza: è riportata esplicitamente nel paper come esempio di risultato
sensibile alla scelta della soglia.

**6. Mann-Kendall sulla serie differenza USA−Italia, femmine.**
Stessa domanda, per le femmine: H0 respinta a entrambe le soglie (primi-10 p = 1,6e-5; primi-50
p = 4,8e-3). Qui il gap *si sta chiudendo* in modo statisticamente significativo e *coerente
indipendentemente da quanti nomi si contano*: le bambine italiane diversificano più in fretta delle
americane, e la distanza tra i due paesi si sta riducendo nel tempo. Questa è la scoperta più solida
delle due, proprio perché regge a entrambe le soglie usate nel paper.

*Come si spiega 6 rispetto a 5, se qualcuno chiede "perché proprio le femmine, e perché i maschi non
sono altrettanto chiari"?* La risposta onesta, al livello puramente statistico, è nelle pendenze di Sen
già riportate in Risultati. Per i maschi: ai primi 10 le pendenze USA e Italia sono quasi identiche
(-0,0020/anno contro -0,0023/anno, intervalli sovrapposti, gap stabile), ma ai primi 50 gli USA
accelerano più dell'Italia (-0,0064/anno contro -0,0055/anno, intervalli **non** sovrapposti, gap in
leggero allargamento): il segno del risultato dipende da quanti nomi si contano, un segnale che per i
maschi l'effetto è debole e non del tutto stabile. Per le femmine, invece, la pendenza italiana è
chiaramente più ripida di quella USA a *entrambe* le soglie (primi-10: -0,0033/anno contro
-0,0011/anno; primi-50: -0,0041/anno contro -0,0028/anno, intervalli **non** sovrapposti in entrambi i
casi): l'Italia sta perdendo concentrazione più in fretta degli USA in modo netto e coerente, e quando
chi parte più indietro corre più veloce a ogni soglia di misura, la distanza si accorcia in modo
affidabile. Questo è il "perché" statisticamente onesto: il risultato femminile è più solido di quello
maschile perché regge al cambio di soglia, quello maschile no.

Se volete offrire anche un'ipotesi sostanziale (dichiarandola esplicitamente come speculazione
correlazionale, coerente con il Limite metodologico (5) del paper), un candidato plausibile è che il
canale di importazione culturale via cui nomi stranieri entrano nel pool italiano sembra colpire in
modo sproporzionato i nomi femminili: quasi tutti i casi di convergenza e di "salto" raccontati nel
paper con una fonte mediatica americana riguardano nomi femminili (Elsa/\emph{Frozen}, Isabella/
\emph{Twilight}, Khaleesi/\emph{Game of Thrones}, Celine Dion), mentre i nomi maschili italiani
restano più ancorati a convenzioni familiari/religiose tradizionali (nomi di nonni, santi) meno
permeabili alle mode importate. Non è provato nel paper, è un'ipotesi di lettura, e va presentata come
tale se la usate.

## Il caveat sul bootstrap (piccolo, onesto, facilmente derubricabile)

**7. Intervalli di confidenza bootstrap sulla pendenza di Sen.**
Questo non è un vero test di ipotesi: è un intervallo di confidenza (2000 iterazioni bootstrap,
metodo percentile) attorno alla pendenza con cui la concentrazione scende in ciascun paese. Si guarda
se gli intervalli di USA e Italia si sovrappongono o no: se non si sovrappongono, è un segnale
informale che le due pendenze sono diverse, ma "non sovrapposizione" non è un test statistico formale
in senso stretto, è un'euristica. Nel paper viene usato solo come conferma supplementare del test 6
(la serie differenza femminile), non come prova indipendente. **Deciso: si taglia dalla
presentazione.** Se qualcuno lo chiede esplicitamente, una riga basta: "un controllo bootstrap
supplementare conferma lo stesso quadro, ma non è un test di ipotesi formale."

## I due controlli di robustezza alla copertura (giustificano le scelte metodologiche di Metodologie e Dati)

Questi due sono cruciali per la credibilità del paper, ma sono controlli di robustezza, non test di
ipotesi: non c'è un H0 da respingere, c'è una domanda tipo "quanto cambierebbe la mia conclusione se i
miei dati fossero più incompleti?".

**8. Controllo di robustezza alla profondità di copertura, per concentrazione ed entropia.**
Metodo: per il 2022-2024 (gli unici anni in cui l'Italia ha la distribuzione completa) si tronca
artificialmente la lista di nomi alle stesse profondità che si sono ottenute realmente negli altri
anni (es. solo i primi 137 nomi, come nel 2021), e si guarda quanto cambia la metrica calcolata sul
troncamento rispetto al valore vero. Risultato, ed è quello che giustifica tutta l'impalcatura
metodologica del paper: le quote primi-10/primi-50/primi-100 non si spostano *per niente* (bias esattamente zero
a ogni profondità testata), mentre l'entropia di Shannon si distorce pesantemente (dal -19% al -50% a
seconda della profondità). Questo è il motivo tecnico per cui il paper usa la quota di concentrazione
come metrica primaria su tutta la finestra 1999-2024, ma riporta l'entropia italiana solo per il
2022-2024: non è una scelta arbitraria, è una scelta dimostrata empiricamente. **Da tenere, è il
fondamento di una scelta metodologica che altrimenti sembrerebbe non giustificata.**

**9. Controllo di robustezza della similarità coseno rispetto alla copertura.**
Stessa logica del punto 8, ma applicata alla metrica di convergenza (coseno) invece che a
concentrazione/entropia: si tronca la distribuzione italiana e si guarda quanto si sposta la
similarità coseno rispetto al valore vero. Risultato: la distorsione resta sotto l'1,9% anche nel
troncamento peggiore in assoluto (377 nomi, il 2021... 1999 secondo il testo), e scende sotto lo 0,46%
per qualunque profondità sopra i 1.000 nomi. Conclusione: anche la misura di convergenza è
sostanzialmente immune al problema di copertura variabile. **Utile da avere pronto se qualcuno chiede
"ma la convergenza non potrebbe essere un artefatto della copertura incompleta?", ma può essere
riassunto in una frase sola in presentazione** ("abbiamo verificato che anche la convergenza non è un
artefatto della copertura, con distorsioni sotto il 2% nel caso peggiore") senza bisogno di citare i
numeri esatti a memoria.

## Il controllo di plausibilità geografico (diverso in natura da tutti gli altri)

**10. Controllo di robustezza geografica.**
Questo non è nemmeno un controllo statistico in senso stretto: è un argomento di plausibilità. Per i
casi-studio RQ2 più solidi (sei salti positivi, tre crolli, tutti USA perché solo l'SSA ha dati per
stato), si guarda se l'effetto nazionale osservato si riflette in modo uniforme in (quasi) tutti gli
stati, o se è concentrato in pochi. Se è uniforme, è un forte indizio che la causa sia davvero un
evento mediatico nazionale (un film, uno scandalo) e non un artefatto regionale o statistico. Sette
casi su nove superano il 90% di stati concordanti. Le due eccezioni (Jaslene al 79%, Hillary al 74%)
sono raccontabili come storie a sé: compatibili con un'adozione inizialmente concentrata in aree
ispaniche per Jaslene, e con una polarizzazione politica non uniforme sul territorio per Hillary. **Da
tenere, è un argomento intuitivo e facile da spiegare a voce, probabilmente il più "raccontabile" di
tutta la sezione.**

## Come funzionano i test, nel dettaglio (se vi chiedono "ma come si calcola?")

Questa sezione spiega il meccanismo dei tre strumenti usati più spesso nel paper. Sono descritti
esattamente come sono stati calcolati nel codice (`02_mann_kendall_us.py`, `03_us_italy_comparison.py`,
`01c_check_coverage_bias.py`), non in astratto.

### Mann-Kendall (test di trend)

Serve a rispondere a una domanda semplice senza assumere che il trend sia lineare o che i dati siano
normali (è un test non parametrico, il che lo rende adatto a serie "rumorose" come queste): **la serie
sta salendo, scendendo, o è solo rumore senza direzione?**

Il calcolo, in breve: si prendono tutte le coppie possibili di anni $(i, j)$ con $i < j$ nella serie, e
per ciascuna coppia si guarda solo il segno della differenza (il valore nell'anno più recente è più
alto, più basso, o uguale a quello nell'anno più vecchio). Si sommano tutti questi segni in una
statistica $S$ (coppie concordanti con un trend crescente contano $+1$, quelle discordanti $-1$). Se
non c'è nessun trend reale, ci si aspetta che $S$ sia vicino a zero, con una variabilità nota che
dipende solo dal numero di anni $n$. Si standardizza $S$ in uno z-score, e da lì si ricava il p-value
(quanto sarebbe raro osservare uno $S$ così estremo se non ci fosse alcun trend). Il coefficiente
$\tau$ di Kendall che compare spesso nel paper è semplicemente $S$ normalizzato tra $-1$ e $+1$ (una
misura di quanto le coppie sono "quasi tutte concordi", indipendente dal p-value: un $\tau$ vicino a
$\pm 1$ significa che il trend è quasi perfettamente monotono, come nel caso della convergenza coseno,
$\tau = 0{,}98$). Nel codice il calcolo non è fatto a mano: si usa la libreria `pymannkendall`
(`mk.original_test(serie)`), che implementa esattamente questo procedimento (Mann 1945, formalizzato
da Kendall 1975) e restituisce anche la pendenza di Sen (la mediana di tutte le pendenze calcolabili
tra ogni coppia di punti: una stima robusta di "quanto velocemente" cambia la serie, usata al posto di
una normale regressione lineare perché non risente di outlier).

### Wilcoxon a coppie appaiate (test di livello)

Domanda diversa da Mann-Kendall: non "c'è un trend nel tempo" ma "in un confronto diretto anno per
anno, una delle due serie è sistematicamente più alta dell'altra?". Si applica solo a dati *appaiati*
(qui: stesso anno, stesso sesso, USA vs Italia).

Calcolo: per ciascuno dei 26 anni appaiati si calcola la differenza (nel codice: valore USA meno
valore Italia). Si prendono i valori assoluti di queste 26 differenze e li si ordina dal più piccolo
al più grande, assegnando un rango (1 = differenza più piccola in valore assoluto, 26 = la più
grande). Si sommano separatamente i ranghi delle differenze positive e quelli delle differenze
negative: se non ci fosse alcuna differenza sistematica tra i due paesi, queste due somme dovrebbero
essere circa uguali. Nel nostro caso sono agli antipodi: nella pratica, l'Italia è risultata più
concentrata degli USA in tutti e 26 gli anni (nessuna eccezione, si veda Sezione Risultati, "statistica
pari a 0 su 26 confronti"), quindi tutte le 26 differenze hanno lo stesso segno: è un esito così
estremo da avere una probabilità bassissima sotto l'ipotesi "nessuna differenza sistematica", da cui
$p < 0{,}0001$. Nel codice si usa `scipy.stats.wilcoxon(us_vals, it_vals)` direttamente sulle due serie
appaiate.

### Entropia di Shannon

Non è un test di ipotesi, è la metrica di diversità stessa (quella di approfondimento per gli USA,
Figura 2; quella scartata come primaria per l'Italia a causa della copertura variabile). Misura quanto
è "sorprendente", in media, il nome di un neonato scelto a caso in un dato anno: se un solo nome copre
quasi tutte le nascite, la sorpresa media è quasi zero (entropia bassa, poca diversità); se le nascite
sono spalmate su migliaia di nomi diversi in proporzioni simili, la sorpresa media è alta (entropia
alta, molta diversità).

Formula: $H = -\sum_i p_i \log_2(p_i)$, dove $p_i$ è la quota di nascite del nome $i$-esimo (un numero
tra 0 e 1) e la somma è su *tutti* i nomi osservati quell'anno/sesso, non solo sui più popolari. Si
misura in
bit: ogni bit in più raddoppia, in un certo senso, il numero "effettivo" di nomi ugualmente probabili
tra cui i genitori stanno scegliendo. È esattamente questa dipendenza dalla coda intera della
distribuzione (migliaia di nomi rari, ciascuno con un contributo minuscolo ma non nullo) a renderla
fragile alla copertura incompleta: se lo scraping cattura solo i primi 137 nomi di un anno, tutta la
massa di probabilità dei nomi non catturati viene silenziosamente persa dal calcolo, e l'entropia
risulta artificialmente più bassa di quella vera (da qui il bias del $-19\%$ al $-50\%$ misurato nel
controllo 8). Nel codice il calcolo è diretto, riga per riga: `h -= p * math.log2(p)` per ogni nome con
$p>0$.

### Perché primi-10 e primi-50 (e perché non top-100 come primaria)

Il paper è passato da top-10/top-30 a top-10/top-50 come metriche primarie (decisione del 2026-08-24,
si veda PROJECT_LOG.md), proprio per avere una rappresentazione più ampia della distribuzione reale dei
nomi senza rinunciare alla sicurezza rispetto alla copertura ISTAT. Numeri reali del 2024: la quota
primi-10 copre circa l'8\% (USA M) / 23\% (IT M) delle nascite; la quota primi-50 arriva a circa il
25\% (USA M) / 53\% (IT M); il top-100, calcolato solo come controllo supplementare in Tabella 14, non
come metrica di trend, arriva al 38\% (USA M) / 66\% (IT M). Il rapporto Italia/USA resta largo a ogni
soglia (circa 2,5x a top-10, circa 2,1x a top-50, circa 1,9x a top-100): la storia di fondo non cambia,
solo si smorza leggermente man mano che si allarga la finestra.

Sulla sicurezza rispetto alla copertura: il controllo 8, rifatto a profondità 10/50/100, mostra bias
esattamente zero a tutte e tre le soglie, perché l'anno ISTAT peggiore mai osservato (137 nomi, 2021)
le supera tutte. La differenza è il margine di sicurezza: 87 nomi di margine con top-50 (137-50) contro
appena 37 con top-100 (137-100). Questo è il motivo per cui top-100 resta confinato alla tabella di
robustezza (un riferimento extra, utile a mostrare che la storia non cambia nemmeno guardando ancora
più in profondità) invece di diventare una terza metrica di trend a pieno titolo: il margine più
stretto la rende meno prudente da usare per ripetere tutti i test statistici, mentre top-10 e top-50
restano entrambi ampiamente al sicuro e insieme danno già due granularità indipendenti su cui
verificare la tenuta di ogni risultato (esattamente quello che ha permesso di scoprire, nel test 5, che
il risultato maschile dipende dalla soglia mentre quello femminile no).

## Riepilogo per la gestione del tempo in presentazione

Se dovete tagliare, in ordine di priorità dal più sacrificabile al meno sacrificabile:

1. **Il caveat bootstrap (punto 7)**: deciso, si taglia (o al massimo una riga se qualcuno lo chiede).
2. **Il controllo di robustezza coseno-copertura (punto 9)**: riassumibile in una frase, i numeri
   esatti servono solo se qualcuno fa la domanda specifica.
3. **Le due serie-differenza per sesso (punti 5-6)**: se il tempo stringe, la versione minima è "il
   divario si chiude per le femmine in modo robusto a ogni soglia, per i maschi il risultato dipende
   dalla soglia scelta ed è quindi più debole" (una frase, non due test separati da spiegare a fondo).
   Non tagliatele del tutto: la contrapposizione femmine-robuste/maschi-dipendenti-dalla-soglia è
   probabilmente l'osservazione più sofisticata della sezione, vale la pena tenerla anche solo come
   una riga.
4. **Da non tagliare mai**: i quattro test di ipotesi formali (punti 1-4, il cuore di RQ1), il
   controllo di robustezza alla copertura per concentrazione/entropia (punto 8, giustifica la scelta
   metodologica centrale del paper), e il controllo geografico (punto 10, è il più intuitivo e
   probabilmente quello che il docente apprezzerà di più data la sua enfasi sul rigore statistico).
