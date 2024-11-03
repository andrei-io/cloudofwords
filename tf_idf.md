## Model TF-IDF

Etape:

1. Preprocesare
   - tokenizare
   - eliminare stopwords("the", "and", ....)
   - lematizare (trece verbul la infinit, samd)
1. Extragere cuvinte importante, prin TF-IDF (Term Frequency-Inverse Document Frequency)
   **Formula TF-IDF**

   - TF-IDF (Term Frequency-Inverse Document Frequency) este o metrică utilizată pentru a evalua importanța unui termen într-un document într-un set de documente. Formula poate fi împărțită în două părți: **TF** și **IDF**.

   - **Frecvența termenului (TF)**:
     $$\text{TF}(t, d) = \frac{\text{numărul de apariții al termenului } t \text{ în documentul } d}{\text{numărul total de termeni în documentul } d}$$
   - **Frecvența inversă a documentului (IDF)**:
     $$\text{IDF}(t, D) = \log\left(\frac{\text{numărul total de documente } |D|}{\text{numărul de documente care conțin termenul } t}\right)$$
   - **Calculul TF-IDF**:
     $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$
