# TODO: Remove all TODO comments once the implementation is complete.
"""
TODO: Add the Paper Title on this line.
TODO: Add the paper's PDF URL (preferably from arXiv) on this line.

TODO: Write a Short Description of the task.

Homepage: TODO: Add the URL to the task's Homepage here.
"""
from lm_eval.base import Task, rf
from lm_eval.metrics import mean
from lm_eval.temporal_metrics import exact_match_score, f1_score, normalize_answer

# TODO: Add the BibTeX citation for the task.
_CITATION = """\
"""

class TempReasonL3(Task):
    VERSION = 1
    DATASET_PATH = "/home/charvi-jain/RINO/temporal_datasets/TempReason/L3"
    DATASET_NAME = None
        
    def has_training_docs(self):
        return True

    def has_validation_docs(self):
        return True

    def has_test_docs(self):
        return True

    def training_docs(self):
        return self.dataset["train"]

    def validation_docs(self):
        return self.dataset["validation"]

    def test_docs(self):
        return self.dataset["test"]

    def doc_to_text(self, doc):
        return f"Date: {doc['date']}\nQuestion: {doc['question']}\nAnswer:"

    def doc_to_target(self, doc):
        return " " + doc["text_answers"]["text"][0]

    def construct_requests(self, doc, ctx):
        """Uses RequestFactory to construct Requests and returns an iterable of
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural
            language description, as well as the few shot examples, and the question
            part of the document for `doc`.
        """
        continuation = rf.greedy_until(ctx, {"until": ["\n",":", "Answer:"]})
        return continuation

    def process_results(self, doc, results):
        """Take a single document and the LM results and evaluates, returning a
        dict where keys are the names of submetrics and values are the values of
        the metric for that one document

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param results:
            The results of the requests created in construct_requests.
        """
        pred = results[0]
        em=exact_match_score(pred, doc["text_answers"]["text"], normalize_answer)
        f1=f1_score(pred, doc["text_answers"]["text"], normalize_answer)  
        return {"em":em, "f1":f1}
        
    def aggregation(self):
        """
        :returns: {str: [float] -> float}
            A dictionary where keys are the names of submetrics and values are
            functions that aggregate a list of metrics
        """
        return {"em": mean, "f1": mean}
                
    def higher_is_better(self):
        """
        :returns: {str: bool}
            A dictionary where keys are the names of submetrics and values are
            whether a higher value of the submetric is better
        """
        return {"em": True, "f1": True}
