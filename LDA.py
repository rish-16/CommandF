from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import  string
import gensim
from gensim import corpora

doc1 = 'Sugar is bad to consume. My sister likes to have sugar, but not my father.'
doc2 = 'My father spends a lot of time driving my sister around to dance practice.'
doc3 = 'Doctors suggest that driving may cause increased stress and blood perssure.'
doc4 = 'Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better.'
doc5 = 'Health experts say that Sugar is not good for your lifestyle.'

doc_complete = [doc1, doc2, doc3, doc4, doc5]

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def clean(doc):
    stop_free = ' '.join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalised = ' '.join(lemma.lemmatize(word) for word in punc_free.split())
    return normalised
    
doc_clean = [clean(doc).split() for doc in doc_complete]

dictionary = corpora.Dictionary(doc_clean)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

Lda = gensim.models.ldamodel.LdaModel

ldamodel = Lda(doc_term_matrix, num_topics=5, id2word=dictionary, passes=50)
topics = ldamodel.print_topics(num_topics=5, num_words=5)

for t in topics:
    print (t)