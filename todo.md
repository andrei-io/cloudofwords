1. unice pe toata baza de date(enrichment pe wos) - si tot asta va fi labelul de "cercetator"
2. de cautat o baza de date mai "vulgara" pentru label-ul "om normal" !!! de verificat: tehnica de selectie
3. pentru clasificare:
   - v1: cate cuvinte am in "cercetator" ponderat cu un scort tf-idf in input si cate cuvinte am in "om de rand1" ponderat cu tf-idf in input, aleg maximul
     c o c
     Ana are mere
     0.8 0.001 0.199
     c: 0.8 + 0.199
     o: 0.001 - v2: vector mediu pentru input, vector mediu pentru fiecare label, aleg distanta minima




Pairwise Cosine Similarities:
            crunchbase  wipo        cordis      wos         abstracts   
crunchbase  1.0000      0.7900      0.9514      0.9000      0.9000      
wipo        0.7900      1.0000      0.8603      0.9034      0.9034      
cordis      0.9514      0.8603      1.0000      0.9596      0.9596      
wos         0.9000      0.9034      0.9596      1.0000      1.0000      
abstracts   0.9000      0.9034      0.9596      1.0000      1.0000     