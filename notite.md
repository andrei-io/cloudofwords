Initial agregate:

- abstracts: 331730
- cordis: 3737
- crunchbase: 8228
- wipo: 9590
- wos: 331730

Rafinate(trecute prin tf-idf is pastrat doar cele cu scort pozitiv)

- abstracts: 18120
- cordis: 1415
- crunchbase: 2175
- wipo: 2203
- wos: 18120

| Categorie  | Inițial | Rafinare | Reducere (%) |
| ---------- | ------- | -------- | ------------ |
| abstracts  | 331,730 | 18,120   | 94.54%       |
| cordis     | 3,737   | 1,415    | 62.14%       |
| crunchbase | 8,228   | 2,175    | 73.56%       |
| wipo       | 9,590   | 2,203    | 77.02%       |
| wos        | 331,730 | 18,120   | 94.54%       |

| Categorie  | Scor mediu          |
| ---------- | ------------------- |
| abstracts  | 0.00115582861581333 |
| cordis     | 0.0143541428647975  |
| crunchbase | 0.0082715074915485  |
| wipo       | 0.00622495647189688 |
| wos        | 0.00115583242856545 |

abstracts
cordis
crunchbase
wipo
wos

TODO: drop la abstracts ca e acelasi lucru cu wos
