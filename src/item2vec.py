import sys, random, json
from gensim.models import Word2Vec
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path

__dir__= Path(__file__).absolute().parent.parent


class DirSentences(object):
    def __init__(self, *args, **kwargs):
        self.dirs = args
        self.len = None
        self.sep = kwargs.get("sep", " ")
        self.shuffle = kwargs.get("shuffle", False)
        self.ext = kwargs.get("ext", "csv")

    def __len__(self):
        if self.len is not None:
            return self.len
        ret = 0
        for dirname in self.dirs:
            for p in Path(dirname).glob("*."+self.ext):
                with p.open("rb") as f:
                    content = f.read().decode("utf-8", "ignore")
                    ret += len(content.split("\n"))
        self.len = ret
        return ret

    def __iter__(self):
        total_len = 0
        for dirname in self.dirs:
            for p in Path(dirname).glob("*."+self.ext):
                with p.open("rb") as f:
                    content = f.read().decode("utf-8", "ignore")
                    for line in content.split("\n"):
                        ret = line.strip(' \r\n"\'\t\xa0`').split(self.sep)
                        if self.shuffle:
                            random.shuffle(ret)
                        yield ret
                        total_len += 1
        self.len = total_len
    
    def build_vocab(self, output=None):
        vocab = Counter()
        for dirname in self.dirs:
            for p in Path(dirname).glob("*."+self.ext):
                with p.open("rb") as f:
                    content = f.read().decode("utf-8", "ignore")
                    for line in content.split("\n"):
                        vocab+=Counter(line.strip().split(self.sep))
        vocab = dict(vocab)
        if output is not None:
            with open(output, "w") as f:
                json.dump(vocab, f)
        return vocab


def main(params):
    train_sentences = DirSentences(*params.input.split(','),
    sep=params.sep, shuffle=params.shuffle,ext=params.input_file_extension)
    if Path(params.model).exists():
        print ("Loading previous model " + params.model)
        model = Word2Vec.load(params.model)
    else:
        print("Creating new model and building vocab")
        model = Word2Vec(epochs=1, min_count=params.minTF, workers=params.workers, vector_size=params.size, window=params.window)
        if Path(params.vocab).exists():
            with open(params.vocab, 'r') as f:
                vocab_freq = json.load(f)
        else:
            print("Vocab file not found, building vocab")
            vocab_freq = train_sentences.build_vocab(output=params.vocab)
        model.build_vocab_from_freq(vocab_freq)
        print("Vocab generation done {c} words".format(c=len(model.wv.index_to_key)))
    print("Training model")
    model.train(train_sentences, total_examples=len(train_sentences), epochs=1)
    print("Saving model to " + params.model)
    model.save(params.model)
    return 0


if __name__ == "__main__":
    argparse = ArgumentParser()
    argparse.add_argument('--window', default=5, type=int, help='window size')
    argparse.add_argument('--size', default=50, type=int, help='vector size')
    argparse.add_argument('--shuffle', default=True, type=bool, help='shuffle order of tokens')
    argparse.add_argument('--sep', default=',', type=str, help='token seperator')
    argparse.add_argument('--input_file_extension', default='csv', type=str, help='input files to process')
    argparse.add_argument('--workers', default=4, type=int, help='number of processes')
    argparse.add_argument('--minTF', default=4, type=int, help='minimum term frequency')
    argparse.add_argument('--model', default=str(__dir__/'w2v.pickle'), type=str, help='model file')
    argparse.add_argument('--input', default=str(__dir__/'data'), type=str, help='dirs to learn from, comma separated')
    argparse.add_argument('--vocab', default=str(__dir__ / 'vocab.json'), type=str, help='vocab frequency file, in json format')
    params = argparse.parse_args()
    sys.exit(main(params))
