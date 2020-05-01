import math
import numpy as np
from konlpy.tag import Komoran
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize
from collections import Counter, defaultdict

# https://lovit.github.io/nlp/2019/04/30/textrank/

## 키워드 추출
def komoran_tokenize(sent, komoran):
  words = komoran.pos(sent, join=True)
  words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
  return words

def scan_vocabulary(sents, tokenize, min_count=2):
  counter = Counter(w for sent in sents for w in komoran_tokenize(sent, tokenize))
  counter = {w:c for w,c in counter.items() if c >= min_count}
  idx_to_vocab = [w for w, _ in sorted(counter.items(), key=lambda x:-x[1])]
  vocab_to_idx = {vocab:idx for idx, vocab in enumerate(idx_to_vocab)}
  return idx_to_vocab, vocab_to_idx


def cooccurrence(tokens, vocab_to_idx, window=2, min_cooccurrence=2):
  counter = defaultdict(int)
  for s, tokens_i in enumerate(tokens):
    vocabs = [vocab_to_idx[w] for w in tokens_i if w in vocab_to_idx]
    n = len(vocabs)
    for i, v in enumerate(vocabs):
      if window <= 0:
        b, e = 0, n
      else:
        b = max(0, i - window)
        e = min(i + window, n)
      for j in range(b, e):
        if i == j:
          continue
        counter[(v, vocabs[j])] += 1
        counter[(vocabs[j], v)] += 1
  counter = {k:v for k,v in counter.items() if v >= min_cooccurrence}
  n_vocabs = len(vocab_to_idx)
  return dict_to_mat(counter, n_vocabs, n_vocabs)


def dict_to_mat(d, n_rows, n_cols):
  rows, cols, data = [], [], []
  for (i, j), v in d.items():
    rows.append(i)
    cols.append(j)
    data.append(v)
  return csr_matrix((data, (rows, cols)), shape=(n_rows, n_cols))


def word_graph(sents, tokenize=None, min_count=2, window=2, min_cooccurrence=2):
  idx_to_vocab, vocab_to_idx = scan_vocabulary(sents, tokenize, min_count)
  tokens = [komoran_tokenize(sent, tokenize) for sent in sents]
  g = cooccurrence(tokens, vocab_to_idx, window, min_cooccurrence)
  return g, idx_to_vocab


def pagerank(x, df=0.85, max_iter=30):
  assert 0 < df < 1
  # initialize
  A = normalize(x, axis=0, norm='l1')
  R = np.ones(A.shape[0]).reshape(-1,1)
  bias = (1 - df) * np.ones(A.shape[0]).reshape(-1,1)
  # iteration
  for _ in range(max_iter):
    R = df * (A * R) + bias
  return R


def textrank_keyword(sents, tokenize, min_count, window, min_cooccurrence, df=0.85, max_iter=30, topk=10):
  g, idx_to_vocab = word_graph(sents, tokenize, min_count, window, min_cooccurrence)
  R = pagerank(g, df, max_iter).reshape(-1)
  idxs = R.argsort()[-topk:]
  # keywords = [(idx_to_vocab[idx], R[idx]) for idx in reversed(idxs)]
  results = [ idx_to_vocab[idx] for idx in reversed(idxs)]
  return results

## 텍스트 요약

def sent_graph(sents, tokenize, min_count=2, min_sim=0.3):
  _, vocab_to_idx = scan_vocabulary(sents, tokenize, min_count)
  tokens = [[w for w in komoran_tokenize(sent, tokenize) if w in vocab_to_idx] for sent in sents]
  rows, cols, data = [], [], []
  n_sents = len(tokens)
  for i, tokens_i in enumerate(tokens):
    for j, tokens_j in enumerate(tokens):
      if i >= j:
        continue
      sim = textrank_sent_sim(tokens_i, tokens_j)
      if sim < min_sim:
        continue
      rows.append(i)
      cols.append(j)
      data.append(sim)
  return csr_matrix((data, (rows, cols)), shape=(n_sents, n_sents))


def textrank_sent_sim(s1, s2):
  n1 = len(s1)
  n2 = len(s2)
  if (n1 <= 1) or (n2 <= 1):
    return 0
  common = len(set(s1).intersection(set(s2)))
  base = math.log(n1) + math.log(n2)
  return common / base


def textrank_keysentence(sents, tokenize, min_count, df=0.85, max_iter=30, topk=1):
  g = sent_graph(sents, tokenize, min_count, 0.2)
  R = pagerank(g, df, max_iter).reshape(-1)
  idxs = R.argsort()[-1]
  keysent = sents[idxs]
  return keysent