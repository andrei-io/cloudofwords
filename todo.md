1. unice pe toata baza de date(enrichment pe wos) - si tot asta va fi labelul de "cercetator"
2. de cautat o baza de date mai "vulgara" pentru label-ul "om normal" !!! de verificat: tehnica de selectie
3. pentru clasificare:
   - v1: cu 2 dataset-uri - cate cuvinte am in "cercetator" ponderat cu un scort tf-idf in input si cate cuvinte am in "om de rand1" ponderat cu tf-idf in input, aleg maximul
     ```
      c   o     c
     Ana are   mere
     0.8 0.001 0.199
     c: 0.8 + 0.199
     o: 0.001
     ```
   - v2: vector mediu pentru input, vector mediu pentru fiecare label, aleg distanta minima
   - v3: doar cu dataset-ul "cercetator" - fac suma la scorurile tf-idf si le normalizez, apoi vad suma la cele ce fac parte din "cercetator"
     ```
      	c         c
     	Ana are   mere
     	0.8 0.001 0.199
     	c: 0.8 + 0.199
     	=> Sansa sa fie cercetator de 0.999
     ```
