A Hidden Markov Model based part-of-speech tagger.

The hmmlearn3.py program creates the model from the given tagged input file; dumps the model parameter to a file called "hmmmodel.txt"

The hmmdecode3.py program takes an untagged data set as input and tags them on the basis of the model parameters present in hmmmodel.txt file; 
The word/TAG output is stored in hmmoutput.txt

Invocation:

python hmmlearn3.py /path/to/training/data

python hmmdecode3.py /path/to/untagged/data
