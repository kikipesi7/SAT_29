# Generátor rozpisu sportovních turnajů (SAT)

Tento projekt řeší problém plánování sportovního turnaje (Sports Tournament Scheduling) pomocí převodu na problém splnitelnosti booleovských formulí v konjunktivní normální formě. Skript vygeneruje logický model pro zadaný počet týmů a kol, uloží jej ve formátu DIMACS CNF a pomocí SAT solveru Glucose 4 nalezne platný rozpis zápasů.

## 1. Popis problému a matematický model

Cílem je naplánovat rozpis sportovního turnaje pro $T$ týmů do $R$ hracích kol tak, aby v každém kole hrál každý tým právě jeden zápas a žádné dva týmy spolu během celého turnaje nehrály více než jednou.

**Vstupní parametry:**
- $T \in \mathbb{N}$ = celkový počet týmů v turnaji
- $R \in \mathbb{N}$ = celkový počet hracích kol

**Výrokové proměnné:**
Pro reprezentaci problému ve výrokové logice zavádíme množinu prvovýroků $x_{i,j,r} \in \{0, 1\}$ pro všechna $i, j \in \{1, \dots, T\}$ (kde $i \neq j$) a $r \in \{1, \dots, R\}$:
- $x_{i,j,r} = 1$ (pravda), pokud tým $i$ hraje proti týmu $j$ v kole $r$.
- $x_{i,j,r} = 0$ (nepravda) v opačném případě.
- Případ $i = j$ je z modelu přímo vyloučen. Celkový počet proměnných je $R \cdot T \cdot (T - 1)$.

**Omezující podmínky (axiomy teorie):**
1. **Každý tým hraje v každém kole alespoň jeden zápas:**
   $$\forall r \in \{1, \dots, R\} \ \forall i \in \{1, \dots, T\}: \bigvee_{j \in \{1, \dots, T\} \setminus \{i\}} x_{i,j,r}$$

2. **Každý tým hraje v každém kole nejvýše jeden zápas:**
   $$\forall r \in \{1, \dots, R\} \ \forall i \in \{1, \dots, T\} \ \forall j, k \in \{1, \dots, T\} \setminus \{i\}, j < k: \neg(x_{i,j,r} \land x_{i,k,r})$$

3. **Zápasy jsou oboustranné:**
   $$\forall r \in \{1, \dots, R\} \ \forall i, j \in \{1, \dots, T\}, i < j: x_{i,j,r} \leftrightarrow x_{j,i,r}$$

4. **Týmy spolu hrají nejvýše jednou za celý turnaj:**
   $$\forall i, j \in \{1, \dots, T\}, i \neq j \ \forall r_1, r_2 \in \{1, \dots, R\}, r_1 < r_2: \neg(x_{i,j,r_1} \land x_{i,j,r_2})$$

## 2. Popis zakódování do CNF

Pro použití v SAT solveru je celá teorie převedena do konjunktivní normální formy (CNF), tedy na konjunkci klauzulí, kde každá klauzule je disjunkcí literálů. Trojice $(i, j, r)$ jsou pomocí slovníku `match_id` bijektivně namapovány na přirozená čísla od $1$ do $R \cdot T \cdot (T - 1)$, která v DIMACS formátu reprezentují jednotlivé prvovýroky.

- **Pravidlo 1 (alespoň jeden soupeř v kole):** Tvoří přímo jednu klauzuli o $T-1$ pozitivních literálech pro každý tým $i$ a kolo $r$. Celkem generuje $R \cdot T$ klauzulí.
- **Pravidlo 2 (nejvýše jeden soupeř v kole):** Podmínka $\neg(x_{i,j,r} \land x_{i,k,r})$ je dle De Morganových zákonů ekvivalentní binární klauzuli $(\neg x_{i,j,r} \lor \neg x_{i,k,r})$. Pro každý tým a kolo kódujeme toto omezení pomocí zakázaných dvojic přes všechny unikátní dvojice potenciálních soupeřů $j < k$.
- **Pravidlo 3 (symetrie zápasů):** Ekvivalence $x_{i,j,r} \leftrightarrow x_{j,i,r}$ je rozložena na dvě implikace $(x_{i,j,r} \rightarrow x_{j,i,r}) \land (x_{j,i,r} \rightarrow x_{i,j,r})$ a následně zapsána jako dvě binární klauzule: $(\neg x_{i,j,r} \lor x_{j,i,r})$ a $(x_{i,j,r} \lor \neg x_{j,i,r})$.
- **Pravidlo 4 (vzájemný zápas nejvýše jednou za turnaj):** Obdobně jako u druhého pravidla využíváme zakázané dvojice. Pro každou uspořádanou dvojici týmů $i \neq j$ a každou dvojici kol $r_1 < r_2$ přidáváme binární klauzuli se zápornými literály $(\neg x_{i,j,r_1} \lor \neg x_{i,j,r_2})$.

## 3. Uživatelská dokumentace

Skript je napsán v jazyce Python 3 a ke svému běhu vyžaduje knihovnu `python-sat`, která zpřístupňuje SAT solver Glucose 4.

**Instalace závislostí:**
    pip install python-sat

**Spuštění skriptu:**
Program se spouští z příkazové řádky a následně se interaktivně zeptá na dva vstupní parametry — počet týmů $T$ (`number of teams:`) a počet kol $R$ (`number od rounds:`):

    python3 tournament.py


**Popis výstupu:**
1. Skript nejprve sestaví CNF formuli a uloží ji do souboru `dimacs.cnf` v pracovním adresáři ve standardním formátu DIMACS CNF (hlavička `p cnf <pocet_promennych> <pocet_klauzuli>` následovaná jednotlivými klauzulemi ukončenými nulou).
2. Do konzole vypíše informaci o počtu vygenerovaných proměnných a klauzulí (`Number of variables`, `Number of clauses`).
3. Následně předá klauzule SAT solveru Glucose 4 a spustí hledání modelu.
4. Vypíše výsledek rozhodnutí (`result: SATISFIABLE` nebo `result: UNSATISFIABLE`).
5. Pokud je formule splnitelná (SAT), skript dekóduje nalezený model (ohodnocení proměnných) do čitelného rozpisu zápasů rozděleného po jednotlivých kolech.
6. Na posledním řádku vždy vypíše čistý čas běhu samotného SAT solveru v sekundách (`solver time`).

## 4. Přiložené instance a experimenty

- **Malá splnitelná instance (4 týmy, 3 kola):**
  - Vstup: `T = 4`, `R = 3`
  - Popis: Klasický malý turnaj systémem „každý s každým“, který lze snadno zkontrolovat ručně. Model obsahuje $36$ proměnných a $120$ klauzulí.
  - Výsledek: `SATISFIABLE`. Solver nalezne platný rozpis zápasů prakticky okamžitě.

- **Malá nesplnitelná instance (3 týmy, 2 kola):**
  - Vstup: `T = 3`, `R = 2`
  - Popis: Instance s lichým počtem týmů ($12$ proměnných, $30$ klauzulí). Z principu nelze lichý počet týmů v rámci jednoho kola spárovat tak, aby každý tým hrál právě jeden zápas. Podobně je nesplnitelná i jakákoliv instance, kde $R \ge T$ (např. `T = 4`, `R = 4`), protože po odehrání $T-1$ kol již týmy vyčerpají všechny dostupné soupeře.
  - Výsledek: `UNSATISFIABLE`. Solver okamžitě detekuje spor.

- **Hledání netriviálně těžké instance:**
  - Vstup: `T = 100`, `R = 60`
  - Popis a pozorování: Při snaze nalézt instanci, kterou by SAT solver řešil přibližně 10 sekund, jsem narazila na výraznou asymetrii mezi časem generování formule v Pythonu a časem samotného řešení solveru. Pro $T = 100$ týmů a $R = 60$ kol roste počet klauzulí pro zakázané dvojice kubicky s počtem týmů a kvadraticky s počtem kol – řádově $\mathcal{O}(R \cdot T^3 + R^2 \cdot T^2)$, což představuje desítky milionů klauzulí. Samotné vygenerování seznamů v Pythonu a zápis souboru `dimacs.cnf` trvá několik minut a spotřebovává značné množství operační paměti. Naproti tomu SAT solver dokázal i tuto obří instanci vyřešit s čistým časem 0.7812 sekund. Dalšímu navyšování nebrání výpočetní čas SAT solveru, ale paměťový limit v Pythonu.