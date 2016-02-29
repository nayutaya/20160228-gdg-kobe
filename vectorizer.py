
import msgpackutil

# 追加された単語すべてを辞書に出力する辞書ジェネレータ。
class TermDictionaryGenerator:
    def __init__(self):
        """
        初期化する。

        >>> generator = TermDictionaryGenerator()
        >>> generator.terms
        set()
        """
        self.terms = set()

    def update(self, tokens):
        """
        更新する。

        >>> generator = TermDictionaryGenerator()
        >>> generator.update(['a', 'b', 'c'])
        >>> generator.to_array()
        ['a', 'b', 'c']

        >>> generator.update(['c', 'd', 'e'])
        >>> generator.to_array()
        ['a', 'b', 'c', 'd', 'e']
        """
        for token in tokens:
            self.terms.add(token)

    def to_array(self):
        """
        配列に変換する。

        >>> generator = TermDictionaryGenerator()
        >>> generator.update(['c', 'b', 'a'])
        >>> generator.to_array()
        ['a', 'b', 'c']
        """
        return sorted(list(self.terms))

    def to_dictionary(self):
        return TermDictionary(self.to_array())

# 追加された単語のうち、指定回数以上出現した単語のみを出力する辞書ジェネレータ。
class TermFrequencyDictionaryGenerator:
    def __init__(self, minimum):
        """
        初期化する。

        >>> generator = TermFrequencyDictionaryGenerator(minimum=5)
        >>> generator.terms
        {}
        >>> generator.minimum
        5
        """
        self.terms   = {}
        self.minimum = minimum

    def update(self, tokens):
        """
        更新する。

        >>> generator = TermFrequencyDictionaryGenerator(minimum=5)
        >>> generator.update(['a', 'b', 'c'])
        >>> sorted(generator.terms.items())
        [('a', 1), ('b', 1), ('c', 1)]

        >>> generator.update(['c', 'd', 'e'])
        >>> sorted(generator.terms.items())
        [('a', 1), ('b', 1), ('c', 2), ('d', 1), ('e', 1)]
        """
        for token in tokens:
            if token in self.terms:
                self.terms[token] += 1
            else:
                self.terms[token] = 1

    def to_array(self):
        """
        配列に変換する。

        >>> generator = TermFrequencyDictionaryGenerator(minimum=3)
        >>> generator.update(['a'])
        >>> generator.to_array()
        []
        >>> generator.update(['a', 'b'])
        >>> generator.to_array()
        []
        >>> generator.update(['a', 'b', 'c'])
        >>> generator.to_array()
        ['a']
        >>> generator.update(['a', 'b', 'c', 'd'])
        >>> generator.to_array()
        ['a', 'b']
        >>> generator.update(['a', 'b', 'c', 'd', 'e'])
        >>> generator.to_array()
        ['a', 'b', 'c']
        """
        return sorted([term for term, count in self.terms.items() if count >= self.minimum])

    def to_dictionary(self):
        return TermDictionary(self.to_array())

class TermDictionary:
    @classmethod
    def load(cls, filename):
        terms = msgpackutil.load(filename)
        return TermDictionary(terms)

    def __init__(self, terms):
        self.terms = terms
        self.table = {term:index for index, term in enumerate(self.terms)}

    def save(self, filename):
        msgpackutil.dump(filename, self.terms)

    def lookup_one(self, token):
        if token in self.table:
            return self.table[token]
        else:
            return None

    def lookup(self, tokens):
        return [self.lookup_one(token) for token in tokens]

class TermVectorizer:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def vectorize(self, tokens):
        term_ids = self.dictionary.lookup(tokens)
        term_ids = [term_id for term_id in term_ids if term_id is not None]
        term_ids = sorted(list(set(term_ids)))
        return term_ids

if __name__ == "__main__":
    import doctest
    doctest.testmod()
