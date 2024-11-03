# TODO: trebuie rulat pe documentul full, nu pe rezumate

## LDA

Latent Dirichlet Allocation (LDA) este un algoritm de modelare tematică folosit pentru a descoperi subiecte latente într-un set mare de documente textuale.

### Cum funcționează LDA?

LDA este un model generativ de tip probabilistic care presupune că documentele dintr-un corp sunt generate pe baza unui număr fix de teme (subiecte), iar fiecare temă este o distribuție de cuvinte. LDA folosește ipoteze probabilistice pentru a asocia fiecare document cu anumite teme și pentru a asocia teme cu seturi de cuvinte.

Etape

1. Inițializare aleatoare:
   LDA începe prin a asocia temele și cuvintele documentelor într-un mod aleatoriu.

1. Îmbunătățirea distribuției:
   Algoritmul parcurge fiecare cuvânt din fiecare document și ajustează probabilitatea de apariție a cuvântului în temele disponibile. Ajustările se fac iterativ, prin metode cum ar fi Gibbs sampling sau Variational Inference, până când modelul converge la o distribuție stabilă.

1. Alocarea probabilistică a temelor:
   În fiecare iterație, LDA actualizează probabilitatea ca un document să aparțină unei teme, precum și probabilitatea ca un cuvânt să fie asociat unei teme, ținând cont de alte cuvinte și teme din document și corpul de text.

1. Identificarea temelor dominante:
   La finalul algoritmului, fiecare document are o distribuție de probabilități peste teme, iar fiecare temă are o distribuție de probabilități peste cuvinte. Astfel, putem determina care sunt temele dominante într-un document și care sunt cuvintele dominante într-o temă.

### Pros&Cons

Avantaje și Limitări ale LDA

- Avantaje:

  - Extrage structuri latente din date, ajutând la înțelegerea conținutului într-un mod semantic.
  - Flexibil și scalabil: Poate fi aplicat pe seturi mari de date, oferind perspective valoroase pentru analiza de conținut, cercetare și marketing.
  - Diminuează zgomotul și oferă o descriere mai concentrată a conținutului unui text.

- Limitări:
  - Sensibilitate la parametrizare: Necesită o ajustare corectă a parametrilor (de exemplu, numărul de teme).
  - Interdependență limitată a cuvintelor: Nu captează structura secvențială a cuvintelor, deci contextul lingvistic complet poate fi ignorat.
  - Ipoteze simplificatoare: Ipoteza că documentele și temele sunt generate de distribuții independente poate să nu reflecte realitatea completă a limbajului natural.

## AJUSTARE PARAMETRII

Numărul de Teme (num_topics):

    Pentru articole științifice despre AI, ar trebui să alegi un număr de teme care să reflecte diversitatea subiectelor din acest domeniu.
    Pentru început, poți testa cu valori între 5 și 20, dar o regulă generală ar fi să începi cu 10-15 teme și să ajustezi în funcție de rezultate.
    Poți folosi metrici precum coerența tematică pentru a evalua calitatea temelor și a găsi un număr optim de subiecte.

Dimensiunea Vocabularului:

    Folosește un filtru pentru a elimina cuvintele extrem de frecvente și foarte rare, deoarece acestea pot introduce zgomot în model.
    În gensim, poți seta no_below și no_above pentru a elimina cuvintele care apar în mai puțin de X documente și mai mult de Y% documente.
    Pentru articole științifice, încearcă valori precum no_below=5 (elimină cuvintele care apar în mai puțin de 5 documente) și no_above=0.5 (elimină cuvintele care apar în mai mult de 50% din documente).

Numărul de Passes și Iterații:

    passes (numărul de treceri prin toate documentele) și iterations (numărul de actualizări interne pe document) influențează calitatea ajustărilor probabilistice.
    Pentru articole științifice, poți începe cu valori passes=10 și iterations=50. Poți crește aceste valori pentru seturi de date mari și complexe, dar cu costul unei creșteri a timpului de calcul.

Alpha și Beta:

    Alpha (distribuția Dirichlet pentru documente pe teme): Controlează distribuția temelor în documente. Un Alpha mic (<0.1) presupune că documentele au doar câteva teme predominante, în timp ce un Alpha mare (>1) încurajează mai multe teme în fiecare document.
    Beta (distribuția Dirichlet pentru cuvinte pe teme): Controlează distribuția cuvintelor în teme. Beta mic înseamnă că temele au câteva cuvinte dominante, iar Beta mare permite o distribuție mai uniformă a cuvintelor.
    Pentru articole științifice, poți începe cu valori de alpha='auto' și beta='auto'; acestea ajustează dinamic distribuția în funcție de datele tale.

Coerența tematică:

    În gensim, poți calcula scorul de coerență pentru a evalua calitatea temelor. Scorul de coerență măsoară cât de semnificative și consistente sunt temele identificate, fiind un indicator esențial pentru evaluarea parametrilor.
