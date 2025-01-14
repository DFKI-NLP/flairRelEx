import pytest
from typing import Tuple

from flairrelex.data import Dictionary, TaggedCorpus
from flairrelex.data_fetcher import NLPTaskDataFetcher, NLPTask
from flairrelex.embeddings import WordEmbeddings, DocumentLSTMEmbeddings
from flairrelex.models.text_classification_model import TextClassifier


@pytest.fixture
def init() -> Tuple[TaggedCorpus, Dictionary, TextClassifier]:
    corpus = NLPTaskDataFetcher.fetch_data(NLPTask.AG_NEWS)
    label_dict = corpus.make_label_dictionary()

    glove_embedding: WordEmbeddings = WordEmbeddings('en-glove')
    document_embeddings: DocumentLSTMEmbeddings = DocumentLSTMEmbeddings([glove_embedding], 128, 1, False, 64, False, False)

    model = TextClassifier(document_embeddings, label_dict, False)

    return corpus, label_dict, model


def test_labels_to_indices():
    corpus, label_dict, model = init()

    result = model._labels_to_indices(corpus.train)

    for i in range(len(corpus.train)):
        expected = label_dict.get_idx_for_item(corpus.train[i].labels[0].name)
        actual = result[i].item()

        assert(expected == actual)


def test_labels_to_one_hot():
    corpus, label_dict, model = init()

    result = model._labels_to_one_hot(corpus.train)

    for i in range(len(corpus.train)):
        expected = label_dict.get_idx_for_item(corpus.train[i].labels[0].name)
        actual = result[i]

        for idx in range(len(label_dict)):
            if idx == expected:
                assert(actual[idx] == 1)
            else:
                assert(actual[idx] == 0)