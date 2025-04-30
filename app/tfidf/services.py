import re
from collections import Counter

from app.tfidf.schemas import WordSchema


def process_text(text):
    words = re.findall(r'\w+', text.lower())

    word_counts = Counter(words)
    total_words = len(words)
    word_stats = []
    for word, tf in word_counts.items():
        idf = total_words / tf
        word_stats.append(WordSchema(word=word, tf=tf, idf=float('{:.2f}'.format(idf))))
    word_stats_sorted = sorted(word_stats, key=lambda x: x.idf, reverse=True)

    return word_stats_sorted
