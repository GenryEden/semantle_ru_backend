import gensim
import zipfile
import wget
import random
import os


if 'model.bin' not in os.listdir():
    model_url = 'http://vectors.nlpl.eu/repository/20/220.zip'

    m = wget.download(model_url, out='model.zip', bar=lambda *x: None)

    with zipfile.ZipFile('model.zip', 'r') as archive:
        archive.extractall(".")

model = gensim.models.KeyedVectors.load_word2vec_format("model.bin", binary=True)




