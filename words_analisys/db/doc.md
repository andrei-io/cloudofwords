keywords.db - all the words concatenated from every source, even numbers
core_words.db - unique words, no numbers, those in initial db but not in gnews - 7096

unique.db - unique words, no numbers - 28613
filtered.db - applied tf-idf on keywords.db for every category
refined.db - keywords from filtered.db also in gnews

Loaded 28613 unique (keyword, origin) pairs from db/keywords.db.
Total words before filtering: 28613
Filtered out 831 words containing numbers.
Total words after removing numbers: 27782
Inserted 27782 unique (keyword, origin) pairs into db/unique.db.

Process completed successfully!
Final count of unique (keyword, origin) pairs in db/unique.db: 27782

Loading Word2Vec model...
Loaded Word2Vec model with 3000000 words.
Found 28613 (keyword, origin) pairs in db/keywords.db.
Total words before filtering: 28613
Filtered out 831 words containing numbers.
Total words after removing numbers: 27782
Filtered out 20686 words found in Word2Vec model.
Remaining words to insert: 7096
Inserted 7096 unique (keyword, origin) pairs into db/final_unique.db.

Process Complete!
Total words before filtering: 28613
Words removed (contained numbers): 831
Words missing from Word2Vec model: 7096
Total unique (keyword, origin) pairs inserted into final_unique.db: 7096
