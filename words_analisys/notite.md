Initial agregate:

- abstracts: 331730
- cordis: 3737
- crunchbase: 8228
- wipo: 9590
- wos: 331730

Rafinate(trecute prin tf-idf is pastrat doar cele cu scort pozitiv)

- cordis: 1415
- crunchbase: 2175
- wipo: 2203
- wos: 18120

| Categorie  | Inițial | Rafinare | Reducere (%) | Scor mediu          |
| ---------- | ------- | -------- | ------------ | ------------------- |
| cordis     | 3,737   | 1,415    | 62.14%       | 0.0143541428647975  |
| crunchbase | 8,228   | 2,175    | 73.56%       | 0.0082715074915485  |
| wipo       | 9,590   | 2,203    | 77.02%       | 0.00622495647189688 |
| wos        | 331,730 | 18,120   | 94.54%       | 0.00115583242856545 |

Voi folosi modelul de word2vec de google-news - nu are nevoie de multe resurse si e rapid, ca dezavantaj e destul de vechi si nu contine multe cuvinte

| Categorie  | Rafinare | Filtrate | Reducere Filtrare (%) |
| ---------- | -------- | -------- | --------------------- |
| cordis     | 1,415    | 1,235    | 12.72%                |
| crunchbase | 2,175    | 1,679    | 22.81%                |
| wipo       | 2,203    | 1,978    | 10.21%                |
| wos        | 18,120   | 11,957   | 34.02%                |
