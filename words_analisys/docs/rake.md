## Model RAKE

Etape

1. Tokenizarea textului în propoziții și cuvinte
   RAKE folosește cuvinte delimitatoare și stopwords pentru a identifica limitele frazelor și a le separa.

1. Identificarea candidaților pentru cuvinte cheie
   Algoritmul grupează cuvintele ce nu sunt stopwords în fraze candidate pentru cuvinte cheie.
   De exemplu, dintr-un text precum „machine learning is a field of artificial intelligence,” RAKE ar putea genera fraze candidate precum „machine learning” și „artificial intelligence”.

1. Calcularea metricilor de relevanță pentru fiecare cuvânt
   RAKE calculează două valori importante pentru fiecare cuvânt candidat:
   Frecvența: De câte ori apare cuvântul în text.
   Gradul de co-ocurență: De câte ori apare cuvântul împreună cu alte cuvinte în același context.
   Pentru fiecare cuvânt, RAKE calculează un scor de relevanță utilizând raportul dintre gradul de co-ocurență și frecvență (sau suma acestor două valori). Cu cât gradul este mai mare în raport cu frecvența, cu atât cuvântul este considerat mai important.

1. Calcularea scorurilor pentru fraze
   Pentru fiecare frază candidat, RAKE adună scorurile individuale ale cuvintelor ce o compun.
   Frazele cu scoruri ridicate sunt considerate mai relevante și sunt clasificate mai sus în lista de cuvinte cheie.

1. Ordinea relevanței cuvintelor și frazelor
   RAKE sortează frazele și cuvintele candidate după scorul total obținut.
   Aceasta permite extragerea celor mai importante cuvinte cheie și fraze dintr-un text într-o manieră rapidă și eficientă.
