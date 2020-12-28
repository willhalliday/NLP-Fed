# Modules
import nltk
## Might need to download these
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
##
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

## Adding sentences columns
beigeBookExtracts['OverallEconomicActivity_sentences'] = beigeBookExtracts['OverallEconomicActivity'].apply(lambda x: sent_tokenize(x))
beigeBookExtracts['EmploymentPrices_sentences'] = beigeBookExtracts['EmploymentPrices'].apply(lambda x: sent_tokenize(x))

## Adding words columns

stopWords = set(stopwords.words("english"))

wnl = WordNetLemmatizer() # I've chosen this over stemmer because it is more nuanced and sophisticated. More detail here : https://stackoverflow.com/questions/1787110/what-is-the-difference-between-lemmatization-vs-stemming

def remove_stop_lemma_words(col: str):
    
    col = re.sub(r'\\s{2,}', ' ', col)
    
    words = word_tokenize(col)
    
    updated_words = []
    for w in words:
        
        if w not in [stopWords, '']: # Only keep if word isn't a stop word
            
            w = wnl.lemmatize(w) # get lemma of word
            
            updated_words.append(w)
            
    return updated_words        

beigeBookExtracts['OverallEconomicActivity_words'] = beigeBookExtracts['OverallEconomicActivity'].apply(lambda x: remove_stop_lemma_words(x))
beigeBookExtracts['EmploymentPrices_words'] = beigeBookExtracts['EmploymentPrices'].apply(lambda x: remove_stop_lemma_words(x))

print(beigeBookExtracts)