# GenerateHaikus

A haiku is a poem of three lines with syllable counts of 5, 7 and 5 respectively. 

Given a text of words, we count the syllables of each word. We then generate a haiku with these words. 

We start by seeding the program with a random word chosen from our text. Then using a Markov model of order 1, we select the next word. 
The word after that is selected with a Markov model of order 2, to keep track of the number of syllables of the two words before it. 
