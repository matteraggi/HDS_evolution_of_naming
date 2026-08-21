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
mediana di queste differenze è zero. H0 respinta, p < 0,0001, per entrambi i sessi. Il risultato è
quasi impressionante da dire a voce: l'Italia è stata più concentrata degli USA in *tutti e 26* gli
anni osservati, zero eccezioni. Non è "l'Italia è mediamente più concentrata", è "non c'è mai stato un
solo anno in cui non lo fosse".

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
questa differenza ha un trend. Per i maschi: H0 *non* respinta (p = 0,172). Il gap tra i due paesi non
sta né restringendosi né allargandosi in modo significativo: è stabile.

**6. Mann-Kendall sulla serie differenza USA−Italia, femmine.**
Stessa domanda, per le femmine: H0 respinta (p = 3,4e-5). Qui il gap *si sta chiudendo* in modo
statisticamente significativo: le bambine italiane diversificano più in fretta delle americane, e la
distanza tra i due paesi si sta riducendo nel tempo. Il fatto che il risultato sia diverso per i due
sessi (stabile per i maschi, in chiusura per le femmine) è di per sé un dato interessante da
sottolineare a voce.

## Il caveat sul bootstrap (piccolo, onesto, facilmente derubricabile)

**7. Intervalli di confidenza bootstrap sulla pendenza di Sen.**
Questo non è un vero test di ipotesi: è un intervallo di confidenza (2000 iterazioni bootstrap,
metodo percentile) attorno alla pendenza con cui la concentrazione scende in ciascun paese. Si guarda
se gli intervalli di USA e Italia si sovrappongono o no: se non si sovrappongono, è un segnale
informale che le due pendenze sono diverse, ma "non sovrapposizione" non è un test statistico formale
in senso stretto, è un'euristica. Nel paper viene usato solo come conferma supplementare del test 6
(la serie differenza femminile), non come prova indipendente. **Candidato naturale al taglio o
all'accorpamento**: è l'elemento più debole della lista, ed è esplicitamente presentato come tale nel
paper stesso ("non come prova indipendente"). Se dovete tagliare qualcosa per il tempo, questo è il
primo candidato: potete menzionarlo in una riga sola ("un controllo bootstrap conferma lo stesso
quadro") senza spiegarne il meccanismo.

## I due controlli di robustezza alla copertura (giustificano le scelte metodologiche di Metodologie e Dati)

Questi due sono cruciali per la credibilità del paper, ma sono controlli di robustezza, non test di
ipotesi: non c'è un H0 da respingere, c'è una domanda tipo "quanto cambierebbe la mia conclusione se i
miei dati fossero più incompleti?".

**8. Controllo di robustezza alla profondità di copertura, per concentrazione ed entropia.**
Metodo: per il 2022-2024 (gli unici anni in cui l'Italia ha la distribuzione completa) si tronca
artificialmente la lista di nomi alle stesse profondità che si sono ottenute realmente negli altri
anni (es. solo i primi 137 nomi, come nel 2021), e si guarda quanto cambia la metrica calcolata sul
troncamento rispetto al valore vero. Risultato, ed è quello che giustifica tutta l'impalcatura
metodologica del paper: la quota primi-10/primi-30 non si sposta *per niente* (bias esattamente zero
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

## Riepilogo per la gestione del tempo in presentazione

Se dovete tagliare, in ordine di priorità dal più sacrificabile al meno sacrificabile:

1. **Il caveat bootstrap (punto 7)**: taglia o riduci a una riga, è esplicitamente secondario anche
   nel paper.
2. **Il controllo di robustezza coseno-copertura (punto 9)**: riassumibile in una frase, i numeri
   esatti servono solo se qualcuno fa la domanda specifica.
3. **Le due serie-differenza per sesso (punti 5-6)**: si possono raccontare come un solo risultato
   invece di due test separati, se il tempo stringe.
4. **Da non tagliare mai**: i quattro test di ipotesi formali (punti 1-4, il cuore di RQ1), il
   controllo di robustezza alla copertura per concentrazione/entropia (punto 8, giustifica la scelta
   metodologica centrale del paper), e il controllo geografico (punto 10, è il più intuitivo e
   probabilmente quello che il docente apprezzerà di più data la sua enfasi sul rigore statistico).
