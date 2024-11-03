## TextRank

TextRank este un algoritm folosit în procesarea limbajului natural pentru a identifica cele mai importante propoziții dintr-un text sau pentru a extrage cuvintele-cheie. TextRank se bazează pe principiile algoritmului PageRank dezvoltat de Google.

### Etape

Algoritmul TextRank se bazează pe reprezentarea unui text sub forma unui graf de cuvinte sau propoziții, unde nodurile reprezintă unități de text (cuvinte sau propoziții), iar muchiile indică legătura (sau similaritatea) dintre ele. Procesul este următorul:

1. Preprocesare: Textul este împărțit în unități mai mici. Pentru extragerea cuvintelor-cheie, textul este de obicei tokenizat în cuvinte și este aplicată eliminarea de stopwords și, eventual, lematizarea.

1. Construirea graficului:
   În cazul cuvintelor-cheie, TextRank construiește un graf de cuvinte. Fiecare cuvânt este un nod, și există o legătură între două cuvinte dacă acestea apar în aceeași "fereastră" (o secvență limitată de cuvinte). Lungimea ferestrei poate fi ajustată; de obicei, se folosește o valoare între 2 și 5.
1. Ponderarea nodurilor: Pe baza similarităților, graficele sunt ponderate prin conectarea nodurilor. Asemenea PageRank-ului, fiecare nod primește un "scor" bazat pe numărul și importanța conexiunilor sale.

1. Algoritmul TextRank folosește o formulă iterativă pentru a calcula scorul fiecărui nod \( V_i \) din graf, similar cu algoritmul PageRank. Scorul unui nod este influențat de numărul și importanța nodurilor vecine.

   Formula pentru scorul nodului \( V_i \) este:

   $$S(V_i) = (1 - d) + d \sum_{V_j \in \text{In}(V_i)} \frac{S(V_j)}{\text{Out}(V_j)}$$

   unde:

   - \( $S(V_i)$ \) reprezintă scorul nodului \( V_i \).
   - \( $d$ \) este factorul de amortizare, de obicei setat între 0.85 și 0.95, care ajustează influența legăturilor vecine asupra scorului.
   - \( $\text{In}(V_i)$ \) reprezintă nodurile care au legături directe către \( V_i \).
   - \( $\text{Out}(V_j)$ \) este numărul de muchii (sau legături) de ieșire ale nodului \( V_j \).

   ### Explicație

   În această formulă:

   1. Fiecare nod începe cu un scor inițial.
   2. Scorul fiecărui nod este ajustat iterativ pe baza scorurilor nodurilor vecine și a legăturilor dintre ele.
   3. Factorul de amortizare \( d \) controlează cât de mult contează legăturile din graf, limitând influența excesivă a unor noduri foarte conectate.

   Procesul se repetă până când scorurile nodurilor converg, adică diferențele dintre scoruri devin minime, indicând stabilitatea.

## Pros&Cons

Avantajele TextRank

    - Fără supraveghere: Nu necesită date pre-etichetate, fiind aplicabil pe diverse domenii.
    - Adaptabilitate: Funcționează atât pentru extragerea de cuvinte-cheie, cât și pentru sumarizare, prin simpla schimbare a unității de text.
    - Simplitate: Implementarea este relativ simplă și se bazează pe relații de co-ocurență sau similaritate în text.

Dezavantajele TextRank

    - Limitări în textele foarte scurte: În cazul textelor foarte scurte, poate fi mai puțin eficient din cauza lipsei de contexte multiple pentru a construi conexiuni.
    - Sensibil la dimensiunea ferestrei: Alegerea dimensiunii ferestrei afectează calitatea rezultatului și poate necesita optimizare.
