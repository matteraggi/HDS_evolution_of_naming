# Metodologie e Dati (bozza — sezione a cura di Person A)

> Nota per la revisione: questa è una bozza di lavoro, non il testo finale del paper. Dati ISTAT ora
> raccolti e confronto statistico eseguito (si vedano i risultati sotto). **Due punti richiedono una
> decisione dal team prima di considerare la sezione definitiva:** (1) la finestra comparabile
> USA/Italia si è ristretta a 2006-2024 invece di 1999-2025 (il 1999-2005 non è recuperabile
> pubblicamente, salvo il 2004); (2) la maggior parte degli anni italiani (tutti tranne 2011-2024)
> si appoggia su nomix.it come fonte secondaria per la quota di concentrazione, non su un PDF ISTAT
> letto direttamente — vedere §1 e §5 per il dettaglio ed eventualmente valutare una verifica manuale
> aggiuntiva dei PDF 2004/2006-2010 se il tempo lo consente. Lunghezza attuale: ~1900 parole.

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
riservatezza dei nuclei familiari più piccoli. Questo comporta un lieve sottostima della diversità reale,
più marcata nei decenni iniziali della serie e per gli stati a bassa natalità — un punto ripreso nei
Limiti (Discussione Finale). L'intero archivio nazionale è stato scaricato ed elaborato per intero: dopo
la pulizia, la tabella lunga risultante conta oltre 2,18 milioni di combinazioni nome/anno/sesso.

**Italia.** La fonte primaria è ISTAT, tramite il report statistico annuale "Natalità e fecondità della
popolazione residente", rilevazione esaustiva e a cadenza annuale attiva dal 1999 (anno da cui, per la
prima volta, i dati a livello di singolo nome sono raccolti sistematicamente tramite il modello
Istat P4, poi confluito nell'Anagrafe Nazionale della Popolazione Residente). A differenza della SSA,
ISTAT **non pubblica una tabella cumulativa scaricabile** nome × anno × sesso × conteggio. Le uniche
fonti pubbliche disponibili sono: (a) il report annuale in formato PDF, che riporta tipicamente i primi 5
nomi maschili e i primi 5 femminili con conteggio assoluto (in un grafico a barre) e, **solo in alcuni
anni**, una statistica aggregata sulla quota di nascite coperta dai primi 30 nomi in ordine di frequenza;
(b) lo strumento interattivo "contanomi" (`istat.it/it/data/interactive-contents/baby-names/`), che
permette di interrogare la serie storica 1999-2024 di un singolo nome alla volta, ma non consente
l'enumerazione sistematica dei circa 26.000 nomi maschili e 25.000 femminili distinti presenti nel
registro. Il confronto diretto di due report annuali consultati (anno di dati 2022 e anno di dati 2024)
ha confermato empiricamente questa incoerenza: il report relativo al 2022 dichiara esplicitamente che
"la distribuzione del numero di nati secondo il nome rivela un'elevata concentrazione intorno ai primi 30
in ordine di frequenza, che complessivamente coprono quasi il 44% di tutti i nomi attribuiti ai maschi e
quasi il 38% di quelli alle femmine"; il report relativo al 2024, di identica struttura editoriale
generale, omette del tutto questa frase, limitandosi al grafico dei primi 5 nomi. La raccolta dei dati
italiani non è quindi un processo di scraping automatizzabile, ma un lavoro di acquisizione manuale
report per report, riassunto in Tabella 1 e Tabella 13.

La raccolta ha coperto gli anni 2004 e 2006-2024 (21 anni; il 2005 risulta un'assenza reale — nessun
report, comunicato stampa o fonte secondaria è stato reperito per quell'anno specifico, nonostante
ricerche mirate). **Il 1999-2003 non è invece coperto**: nessun report o compilazione secondaria
risalente a quegli anni è stato reperito, per cui la finestra comparabile USA/Italia effettivamente
utilizzabile per il confronto statistico si restringe a **2006-2024** (19 anni), più stretta della
finestra 1999-2025 originariamente prevista nel piano di ricerca. Questo è un vincolo di disponibilità
dei dati, non una scelta metodologica, e va dichiarato esplicitamente nei Limiti.

Per la maggior parte degli anni (2004, 2006-2010), la statistica di concentrazione primi-30 e i conteggi
esatti dei primi 5 nomi non erano recuperabili da un PDF ISTAT rintracciabile; sono stati invece ottenuti
da nomix.it, un sito di terze parti specializzato in nomi che cita esplicitamente ISTAT come fonte per
ogni anno e i cui valori sono stati incrociati, dove possibile, con i PDF ISTAT primari (2020, 2022,
2024), risultando coerenti. Si tratta comunque di una **fonte secondaria non accademica**, e ogni singolo
valore proveniente da nomix.it è tracciato come tale nella tabella
`data/raw/istat/istat_annual_top_names.csv` (colonna `notes`) — un punto da discutere esplicitamente nei
Limiti e, se necessario, da rafforzare con verifica manuale aggiuntiva dei PDF primari (14 dei 21 anni,
2011-2024, sono già stati verificati contro un PDF ISTAT scaricato direttamente).

Un'ulteriore discontinuità metodologica rilevata nei report stessi: dal 2020 ISTAT ha cambiato il
criterio di attribuzione dell'anno di riferimento delle nascite, passando dall'anno di **registrazione**
in anagrafe all'anno **evento** (data di nascita effettiva) — un cambiamento che può introdurre una lieve
discontinuità nel confronto anno su anno a cavallo del 2020, da segnalare in nota.

## 2. Pulizia e normalizzazione

Per gli Stati Uniti, ogni file annuale è stato letto e aggregato in una tabella lunga
(`anno, nome, sesso, conteggio, nascite_totali_sesso, frequenza_relativa`), con la frequenza relativa
calcolata sul totale delle nascite dello stesso sesso in quell'anno, per evitare che la crescita o il
calo della popolazione nel tempo confondesse le variazioni di diversità onomastica con semplici
variazioni di scala. È importante notare che le metriche sono state calcolate **separatamente per sesso**
(maschi, femmine) e non sulla distribuzione aggregata: questa scelta, apparentemente in contrasto con la
prassi di alcuni studi precedenti sui soli dati USA, è stata necessaria per garantire la comparabilità
con l'Italia, il cui unico dato aggregato pubblicato (la quota primi-30) è sistematicamente riportato
separatamente per nascite maschili e femminili. Una riga "aggregata" (M+F) per anno è comunque calcolata
e conservata come riferimento secondario, non come metrica comparativa primaria.

Per l'Italia, dato che non esiste una tabella grezza da pulire nel senso tradizionale, il processo di
"normalizzazione" consiste nell'estrazione manuale, da ciascun report PDF disponibile, delle statistiche
effettivamente pubblicate (quota primi-30 quando presente, nomi e conteggi dei primi 5 quando presente,
totale nascite dell'anno) in una tabella strutturata comparabile nel formato ai dati USA, con celle vuote
esplicite per gli anni in cui una data statistica non è disponibile — piuttosto che stime o
interpolazioni, per non introdurre artificialmente continuità dove i dati non la garantiscono.

## 3. Il pivot della metrica di diversità (RQ1)

Il piano di ricerca originario prevedeva l'uso dell'entropia di Shannon come metrica primaria di
diversità onomastica in entrambi i paesi. Questo approccio è rimasto invariato per gli Stati Uniti, dove
la distribuzione completa dei nomi consente il calcolo diretto:

H(anno, sesso) = − Σᵢ pᵢ · log₂(pᵢ)

dove pᵢ è la frequenza relativa dell'i-esimo nome in quell'anno/sesso. Il calcolo sull'intera serie
1880-2025 (Figura 2) mostra un andamento coerente con la letteratura: un minimo relativo attorno agli
anni '40-'50 (coincidente con la fase del baby boom, tradizionalmente associata a una maggiore
conformità sociale nelle scelte dei nomi) seguito da una crescita pressoché ininterrotta dagli anni '60 a
oggi, in linea con la tesi di Twenge et al. (2010) sull'aumento dell'individualismo nelle scelte dei
genitori americani.

Per l'Italia, tuttavia, l'assenza di una distribuzione completa pubblicamente accessibile rende
impossibile calcolare l'entropia di Shannon reale — al più se ne potrebbe stimare un limite inferiore
usando solo i nomi noti, ma il risultato sarebbe sistematicamente e in modo non quantificabile distorto
verso il basso, e quindi non comparabile in modo rigoroso con il dato USA. Si è quindi adottata come
**metrica comparativa primaria tra i due paesi la quota di concentrazione dei primi N nomi** (top-10 e
top-30), ovvero la percentuale di nascite coperta dai nomi più frequenti dell'anno. Questo è un proxy
di diversità ampiamente validato in letteratura: Ogihara (2025), nel suo studio sui nomi nel Regno Unito
1996-2016, riporta una correlazione negativa quasi perfetta (r ≈ −0,96 a −0,99) tra la quota di
concentrazione dei nomi più popolari e un indice di varietà onomastica calcolato indipendentemente,
confermando che la quota di concentrazione è un proxy affidabile della diversità complessiva anche
quando la distribuzione completa non è disponibile.

Per gli Stati Uniti la quota di concentrazione è calcolata direttamente sulla distribuzione completa; per
l'Italia, dove i nomi classificati oltre la quinta (o decima) posizione non sono singolarmente noti, la
quota primi-30 pubblicata da ISTAT — quando disponibile — è utilizzata così com'è, senza tentativi di
ricostruzione o stima dei singoli nomi mancanti.

## 4. Validazione scientifica

**Test di trend Mann-Kendall.** Per verificare che le serie di entropia e di concentrazione mostrino un
andamento monotono statisticamente significativo nel tempo (e non variazioni casuali), è stato applicato
il test non parametrico di Mann-Kendall (Mann, 1945; Kendall, 1975) separatamente per sesso, metrica e
finestra temporale (serie completa 1880-2025 e finestra comparabile 1999-2025), con lo stimatore di
pendenza di Sen come misura complementare di intensità del trend. Sui dati USA, tutti i 18
test eseguiti (3 metriche × 3 gruppi di sesso × 2 finestre temporali) risultano significativi con
p < 0,001: l'entropia cresce e le quote di concentrazione (sia primi-10 sia primi-30) calano in modo
monotono e robusto in ogni combinazione testata, confermando che il pivot verso la metrica di
concentrazione cattura un fenomeno reale e non un artefatto della scelta metodologica.

**Confronto statistico tra paesi.** Sulla finestra sovrapposta 2006-2024 (19 anni; si veda sopra per il
motivo del restringimento rispetto al 1999-2025 originariamente previsto) sono stati eseguiti, per ciascun
sesso, quattro test: (a) Mann-Kendall sulla serie propria di ciascun paese, come controllo di coerenza col
risultato ottenuto sul campione USA completo; (b) Mann-Kendall sulla serie differenza USA−Italia, per
verificare se il divario tra i due paesi si sta sistematicamente ampliando o riducendo; (c) test di
Wilcoxon a coppie appaiate sui valori annuali, per verificare se il livello di concentrazione USA è
sistematicamente diverso da quello italiano; (d) intervalli di confidenza bootstrap (percentile, 2000
iterazioni) sulla pendenza di Sen di ciascun paese, con la non sovrapposizione degli intervalli come
segnale di pendenze significativamente diverse.

I risultati (Tabella 12) mostrano un quadro differenziato per sesso. Per i nomi **maschili**, la velocità
di diversificazione USA e Italia risulta statisticamente indistinguibile: pendenza di Sen USA
−0,00427/anno (IC 95% [−0,00438, −0,00416]) contro Italia −0,00440/anno (IC 95% [−0,00486, −0,00392]),
intervalli sovrapposti, e la serie differenza non mostra un trend significativo (p = 0,36) — il divario
tra i due paesi resta stabile nel tempo. Per i nomi **femminili**, invece, l'Italia si sta diversificando
significativamente più in fretta degli USA: pendenza di Sen Italia −0,00355/anno contro USA
−0,00172/anno, intervalli **non sovrapposti**, e la serie differenza mostra un trend crescente
significativo (p < 0,001) — il divario si sta riducendo nel tempo. In entrambi i sessi, il test di
Wilcoxon a coppie appaiate è fortemente significativo (p < 0,0001): in ogni singolo anno della finestra
2006-2024, la quota di concentrazione italiana è risultata superiore a quella statunitense, ovvero
l'Italia rimane sistematicamente più concentrata (meno diversificata) degli Stati Uniti per l'intero
periodo osservato, pur convergendo nel caso femminile. Questo è il risultato centrale della RQ1 e la base
della Figura 5 (confronto USA/Italia sulla finestra sovrapposta).

## 5. Limiti metodologici principali

Tre limiti meritano di essere dichiarati esplicitamente, in linea con la richiesta di validazione
scientifica del corso. Primo, la soglia di soppressione SSA (nomi con <5 nascite/anno/stato/sesso non
riportati) introduce una lieve sottostima della diversità reale statunitense, più accentuata nei decenni
iniziali. Secondo, e più rilevante, l'asimmetria strutturale tra le due fonti: la distribuzione USA è
completa, quella italiana è per costruzione parziale (solo i nomi più frequenti, e con copertura
temporale della statistica di concentrazione non garantita anno per anno) — questo non è un difetto del
disegno di ricerca ma un limite oggettivo dell'infrastruttura statistica pubblica italiana rispetto a
quella americana, discusso più diffusamente nella sezione sul Fattore Umano. Terzo, il confronto USA/Italia
è per necessità limitato alla finestra 1999-2025, poiché l'Italia non dispone di dati a livello di nome
per gli anni precedenti; l'entropia USA 1880-2025 viene quindi presentata come figura di approfondimento
non comparativa, chiaramente etichettata come tale (Figura 2), e non come base per affermazioni
comparative dirette con l'Italia al di fuori della finestra 1999-2025.

Due limiti aggiuntivi sono emersi durante la raccolta effettiva dei dati italiani e vanno dichiarati con
altrettanta chiarezza. Quarto, la finestra comparabile realmente utilizzabile per il confronto statistico
si è ristretta ulteriormente a **2006-2024** (19 anni): nessun report o compilazione secondaria per il
1999-2003 e il 2005 è stato reperito pubblicamente, nonostante ricerche mirate — un limite di
reperibilità dei dati, non di esistenza (ISTAT dichiara di raccogliere dati a livello di nome dal 1999),
che riduce la finestra comparativa di sette anni rispetto a quanto originariamente previsto. Quinto, per
15 dei 19 anni della finestra comparabile (tutti tranne 2011-2024, verificati contro un PDF ISTAT
scaricato e letto direttamente), la quota di concentrazione primi-30 e i conteggi dei primi 5 nomi
provengono da nomix.it, un sito di terze parti non accademico che dichiara ISTAT come fonte per ogni
anno; i valori sono stati incrociati con successo nei tre punti in cui un confronto diretto con il PDF
ISTAT primario era possibile (2020, 2022, 2024), ma restano una **fonte secondaria non verificata in modo
sistematico** per gli anni più vecchi. Questo va dichiarato esplicitamente in Metodologie/Dati e ripreso
in Discussione Finale; se il tempo a disposizione del team lo consente, un rafforzamento consigliato è la
verifica manuale diretta dei report ISTAT primari (o dell'interrogazione dello strumento "contanomi") per
almeno un sottoinsieme degli anni 2004-2010 prima della consegna finale.
