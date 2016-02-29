
class Strategy:
    def __init__(self, normalizer, tokenizer):
        self.normalizer = normalizer
        self.tokenizer  = tokenizer

    def tokenize(self, str):
        return self.tokenizer.tokenize(self.normalizer.normalize(str))
