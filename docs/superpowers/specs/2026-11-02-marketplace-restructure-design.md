# Ristrutturazione del marketplace `giofornari`: design

Data: 2026-11-02. Stato: in attesa di approvazione del proprietario (rottura degli id approvata).
Le scelte segnate **[mia scelta]** non sono state discusse: vanno controllate.

## 1. Intento

Oggi il marketplace è un indice ordinato di repo altrui: 61 voci, 8 pack, nessun valore proprio. Chi lo apre non ha un motivo per preferirlo a una awesome-list.

L'obiettivo è renderlo un marketplace che chiunque possa usare, con una logica chiara: pacchetti combinabili che non si sovrappongono, costo in token contenuto, e un contenuto nostro (gli *essential*) che esiste solo qui. Successo vuol dire che una persona nuova installa un solo pacchetto per categoria e ottiene un setup compatto, senza doppioni e senza dover capire quale delle tre skill "grill" scegliere.

### Problemi verificati nello stato attuale

- **Doppioni dentro i pack.** `grill-me`, `grill-with-docs` e `grilling` sono la stessa idea tre volte e si sovrappongono a `brainstorming` di superpowers. Ricerca web ha tre backend (firecrawl, exa, tavily). Design ha cinque skill che promettono "UI migliore". `seo`, `marketing-skills` e `marketing-cro` si sovrappongono su CRO e copywriting.
- **Categorie incoerenti.** "Design" e "Design Advanced" sono una divisione arbitraria. "Learning" contiene pptx, diagrammi e anatomy, che con l'imparare c'entrano poco. Ogni categoria coincide con un pack, quindi tassonomia e installazione sono la stessa cosa.
- **Costo in token.** Il pack Marketing aggiunge ~25.7k token a ogni sessione, Content ~8.6k.

## 2. Modello: tre livelli per categoria

```
categoria
├── essential     plugin nostro in plugins/<categoria>: skill fuse dai migliori plugin
├── pack          solo dependencies: essential + plugin indivisibili installati così come sono
└── plugin        puntatori upstream (github, git-subdir, ...), installabili uno a uno
```

**Essential.** Plugin locale con il nome della categoria. Contiene skill nostre, ottenute fondendo le skill che nei plugin della categoria fanno lo stesso lavoro. Dove tre plugin offrono tre varianti dello stesso lavoro, l'essential ne ha una sola.

**Pack.** Plugin vuoto con sole `dependencies`, come oggi. Contiene i plugin che non si possono fondere né ottimizzare (claude-mem, ponytail, superpowers per Fundamentals) e che quindi si installano interi.
- **[mia scelta]** Il pack include anche l'essential della categoria, così un comando installa tutto.
- **[mia scelta]** Regola di composizione: un plugin donatore le cui skill sono state fuse **esce dal pack** (resta installabile da solo). Nel pack restano l'essential e i soli plugin indivisibili. Gli indivisibili che duplicano un'idea dell'essential (superpowers e `brainstorming`) restano comunque: è la duplicazione accettata sopra.
- **[mia scelta]** I pack tengono la convenzione numerata (`1-pack-fundamentals`, ...) perché la lista di `/plugin` ordina alfabeticamente e le cifre vengono prima. Gli essential hanno il nome pulito della categoria (`fundamentals`, `design`).

**Plugin singoli.** Restano nel catalogo come oggi. Anche i plugin donatori di skill all'essential restano installabili da soli.

### Regole di ammissione

- **Fondibile:** una skill in Markdown che nella sua categoria si sovrappone per funzione ad altre.
- **Da pack così com'è:** plugin con hook, demoni, server MCP o una metodologia che funziona solo intera.
- **Decisione del proprietario:** la stessa idea può comparire sia nell'essential (come skill fusa) sia nel pack (come originale). La skill fusa è un'altra skill; non è un doppione.
- **Conseguenza da gestire:** quando entrambe sono installate, le loro `description` non devono contendersi gli stessi trigger. Ogni skill fusa ha una descrizione scritta per attivarsi in modo distinto dall'originale.

## 3. Categorie (7)

| Categoria | Contenuto di partenza | Cambia rispetto a oggi |
|---|---|---|
| Fundamentals | metodo di lavoro: planning, debug, interview/grill, review, regole di comportamento | resta |
| Context & Memory | honcho, claude-mem, caveman, graphify | resta |
| Design | impeccable, taste-skill, emil, ui-ux-pro-max, hallmark, ux-heuristics, steve-jobs-design-review, threejs | unisce Design e Design Advanced |
| Research & Web | firecrawl, exa, tavily, camoufox, agent-reach, last30days | agent-reach arriva da Content |
| Content & Media | openmontage, hyperframes, remotion, ppt-master, diagram-design, anatomy, academic-pptx | ppt, diagrammi, anatomy arrivano da Learning |
| Marketing & Sales | seo, seo-extensions, marketing-cro, marketing-skills, sales-* | resta |
| Learning | teach, understand-anything, education-agent-skills, i-have-adhd | si svuota di ciò che non riguarda l'imparare |

`career-ops` non ha una categoria: **[mia scelta]** resta un bonus fuori categoria.

**Non ogni categoria ha un essential.** Context & Memory e Research & Web sono fatte di backend (hook, demoni, MCP) che non si fondono: lì esiste solo il pack. Essential certi: Fundamentals, Design, Marketing & Sales. Content & Media e Learning si decidono dopo l'analisi.

## 4. Come si fonde

Per ogni categoria con essential:

1. **Inventario.** Per ogni plugin donatore: elenco delle skill, descrizione, costo in token (`claude plugin details`), licenza.
2. **Raggruppamento** delle skill per lavoro svolto.
3. **Decisione per gruppo:** fondere in una skill nuova, tenere la migliore estraendola, oppure scartare.
4. **Scrittura** della skill fusa in `plugins/<categoria>/skills/<nome>/SKILL.md`.
5. **Misura.** Due controlli, con `claude plugin details`: (a) il costo dell'essential è inferiore alla somma dei soli plugin donatori usciti dal pack; (b) il costo del nuovo pack è inferiore a quello del pack attuale della stessa categoria.
6. **Revisione con il proprietario** categoria per categoria prima di passare alla successiva.

Fundamentals è il pilota: ha i doppioni più evidenti e il metodo si valida lì.

### Licenze e fonti

- Fondere vuol dire copiare e riscrivere. La regola attuale del `CLAUDE.md` ("copia nulla, segui upstream") vale solo per i plugin puntatore; **va riscritta** nello stesso commit perché gli essential sono l'eccezione.
- **[mia scelta]** Soglia di licenza: entrano nella fusione solo fonti con licenza permissiva (MIT, Apache-2.0, BSD, CC0) e con attribuzione. Tutto il resto resta puntatore: GPL/AGPL, CC-BY-SA, CC-BY-NC, e i repo senza file di licenza (senza licenza i diritti sono riservati). Il repo è MIT. L'analisi riporta per ogni donatore la licenza trovata, così l'impatto sull'essential si vede prima di scrivere.
- **[mia scelta]** Attribuzione in due posti: una riga di fonte (repo, licenza, data della versione letta) nell'intestazione di ogni skill fusa, e un `NOTICE` nel plugin che le elenca tutte.
- **[mia scelta]** Poiché una skill fusa non segue più upstream, la data della versione letta serve a rivedere periodicamente le fonti. Un processo automatico di aggiornamento è fuori scope.

## 5. Obiettivi, non-obiettivi, anti-obiettivi

**Obiettivi**
- Sette categorie coerenti, ognuna usabile con un solo pack.
- Essential che costano meno dei plugin che sostituiscono.
- Documentazione (README, README.it, immagini) che spieghi la logica a chi arriva da fuori.

**Non-obiettivi**
- Non riscrivere né forkare i plugin del pack: restano puntatori.
- Non pinnare versioni (resta la convenzione attuale: nessun `version`).
- Non costruire strumenti nuovi oltre a quanto serve a misurare e validare.

**Anti-obiettivi (fallimento anche se tecnicamente funziona)**
- Una "skill fusa" che è la concatenazione delle originali: stesso costo, nessun guadagno.
- Un essential che costa più dei plugin che sostituisce.
- Pack ancora pieni di plugin che fanno la stessa cosa.
- Skill fuse senza fonte o con licenza non rispettata.

## 6. Fasi

**[mia scelta] Branch.** Tutto il lavoro avviene su un branch `restructure` e arriva su `main` con un unico merge a fine lavoro. Così `main` non resta mai a metà, e la regola "README e PNG nello stesso commit di `marketplace.json`" vale per il merge, non per ogni commit intermedio.

1. **Pilota Fundamentals, dall'inizio alla fine:** analisi in sola lettura, revisione con il proprietario, costruzione di essential e pack. Serve a validare il metodo prima di moltiplicarlo. In più, un inventario veloce e in sola lettura di Content & Media e Learning, per decidere se meritano un essential.
2. **Le altre categorie,** nell'ordine Design, Marketing & Sales, poi le altre. L'analisi si può lanciare in parallelo, una per categoria; la revisione del proprietario e la costruzione restano una categoria alla volta. Per ognuna: essential, pack riscritto, voci in `marketplace.json`, `claude plugin validate .`.
3. **Prima commit del branch:** riscrittura del `CLAUDE.md` con la regola nuova (copia ammessa per gli essential, con fonte e licenza).
4. **A fine lavoro, prima del merge:** README, README.it, tutti i PNG in `docs/` (anche `docs/it/` e `map.it.png`) con le nuove categorie e i nuovi costi in token, descrizioni italiane per ogni voce nuova.

## 7. Lasciato a chi costruisce

- I nomi esatti delle skill fuse.
- La soglia di token per ciascun essential (criterio minimo: inferiore alla somma dei sostituiti).
- Se Content & Media e Learning ottengono un essential, in base ai risultati dell'analisi.
- Il modo di generare i nuovi PNG.

## 8. Installazioni esistenti (deciso dal proprietario)

Unificare Design e Design Advanced, ridurre le categorie a 7 e rinominarne alcune rompe gli id dei pack attuali (`4-pack-design-advanced`, `7-pack-content-creation`, ...). **Decisione: rottura netta**, senza pack-stub. I due README riportano una tabella "vecchio id, nuovo id".
