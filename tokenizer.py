
import janome.tokenizer

class NormalizedTokenizer:
    def __init__(self, normalizer, tokenizer):
        self.normalizer = normalizer
        self.tokenizer  = tokenizer

    def tokenize(self, str):
        return self.tokenizer.tokenize(self.normalizer.normalize(str))

class LetterUnigramTokenizer:
    def tokenize(self, str):
        """
        文字単位に日本語文字列を分割し、1-gramを適用する。

        >>> tokenizer = LetterUnigramTokenizer()
        >>> tokenizer.tokenize('我が輩は猫である')
        ['我', 'が', '輩', 'は', '猫', 'で', 'あ', 'る']

        >>> tokenizer.tokenize('すもももももももものうち')
        ['す', 'も', 'も', 'も', 'も', 'も', 'も', 'も', 'も', 'の', 'う', 'ち']
        """
        tokens = [str[i] for i in range(0, len(str))]
        return tokens

class LetterBigramTokenizer:
    def tokenize(self, str):
        """
        文字単位に日本語文字列を分割し、2-gramを適用する。

        >>> tokenizer = LetterBigramTokenizer()
        >>> tokenizer.tokenize('我が輩は猫である')
        ['我が', 'が輩', '輩は', 'は猫', '猫で', 'であ', 'ある']
        >>> tokenizer.tokenize('すもももももももものうち')
        ['すも', 'もも', 'もも', 'もも', 'もも', 'もも', 'もも', 'もも', 'もの', 'のう', 'うち']
        """
        tokens = [str[i] for i in range(0, len(str))]
        return [a + b for a, b in zip(tokens, tokens[1:])]

class LetterTrigramTokenizer:
    def tokenize(self, str):
        """
        文字単位に日本語文字列を分割し、3-gramを適用する。

        >>> tokenizer = LetterTrigramTokenizer()
        >>> tokenizer.tokenize('我が輩は猫である')
        ['我が輩', 'が輩は', '輩は猫', 'は猫で', '猫であ', 'である']
        >>> tokenizer.tokenize('すもももももももものうち')
        ['すもも', 'ももも', 'ももも', 'ももも', 'ももも', 'ももも', 'ももも', 'ももの', 'ものう', 'のうち']
        """
        tokens = [str[i] for i in range(0, len(str))]
        return [a + b + c for a, b, c in zip(tokens, tokens[1:], tokens[2:])]

class JanomeUnigramTokenizer:
    def __init__(self):
        self.tokenizer = janome.tokenizer.Tokenizer()

    def tokenize(self, str):
        """
        形態素解析ライブラリ「janome」を使って日本語文字列を分かち書きし、1-gramを適用する。

        >>> tokenizer = JanomeUnigramTokenizer()
        >>> tokenizer.tokenize('我が輩は猫である')
        ['我が', '輩', 'は', '猫', 'で', 'ある']
        >>> tokenizer.tokenize('すもももももももものうち')
        ['すもも', 'も', 'もも', 'も', 'もも', 'の', 'うち']
        """
        tokens = self.tokenizer.tokenize(str)
        return [token.surface for token in tokens]

class JanomeBigramTokenizer:
    def __init__(self):
        self.tokenizer = janome.tokenizer.Tokenizer()

    def tokenize(self, str):
        """
        形態素解析ライブラリ「janome」を使って日本語文字列を分かち書きし、2-gramを適用する。

        >>> tokenizer = JanomeBigramTokenizer()
        >>> tokenizer.tokenize('我が輩は猫である')
        ['我が輩', '輩は', 'は猫', '猫で', 'である']
        >>> tokenizer.tokenize('すもももももももものうち')
        ['すももも', 'ももも', 'ももも', 'ももも', 'ももの', 'のうち']
        """
        tokens = [token.surface for token in self.tokenizer.tokenize(str)]
        return [a + b for a, b in zip(tokens, tokens[1:])]

class JanomeTrigramTokenizer:
    def __init__(self):
        self.tokenizer = janome.tokenizer.Tokenizer()

    def tokenize(self, str):
        """
        形態素解析ライブラリ「janome」を使って日本語文字列を分かち書きし、2-gramを適用する。

        >>> tokenizer = JanomeTrigramTokenizer()
        >>> tokenizer.tokenize('我が輩は猫である')
        ['我が輩は', '輩は猫', 'は猫で', '猫である']
        >>> tokenizer.tokenize('すもももももももものうち')
        ['すももももも', 'もももも', 'ももももも', 'もももの', 'もものうち']
        """
        tokens = [token.surface for token in self.tokenizer.tokenize(str)]
        return [a + b + c for a, b, c in zip(tokens, tokens[1:], tokens[2:])]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
