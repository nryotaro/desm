"""
"""
import os
import tempfile
from unittest import TestCase
from click.testing import CliRunner
import gensim.models as mo
import desm
import desm.model as m
import desm.model_location as ml


class TestMain(TestCase):

    def setUp(self):
        self.word2vec_path = tempfile.mkstemp()[1]
        self.desm_path = tempfile.mkstemp()[1]

    def tearDown(self):
        for filename in [self.word2vec_path,
                         self.desm_path]:
            os.remove(filename)

    def test_smoke(self):
        runner = CliRunner()
        corpus_path = os.path.join(
            os.path.dirname(__file__),
            'test_main_corpus.txt')
        runner.invoke(
            desm.main,
            ['train',
             '--min-count',
             '1',
             corpus_path,
             self.word2vec_path])

        runner.invoke(
            desm.main,
            ['build',
             'inout',
             self.word2vec_path,
             self.desm_path])

        model_location = ml.ModelLocation.create(
            self.desm_path)
        with model_location.open_gz_readable_stream() as \
                stream:
            model = m.Desm.load(stream)
            self.assertIsInstance(model, m.DesmInOut)
            word2vec = model.word2vec
            self.assertIsInstance(word2vec, mo.Word2Vec)
