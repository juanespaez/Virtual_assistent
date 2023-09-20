class NaturalLanguajeModel:

    pass


class Bert(NaturalLanguajeModel):

    def __init__(self, qa_input, model_name="deepset/roberta-base-squad2"):
        self.qa_input = qa_input      # Dictionary with context and question
        self.model_name = model_name  # We use Model "deepset/roberta-base-squad2"

    def loadmodel(self):

        from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline  # Import Libraries
        model = AutoModelForQuestionAnswering.from_pretrained(self.model_name)  # Set the model
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)  # Set the tokenizer
        nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)  # Set the NaturalLanguajeModel
        res = nlp(self.qa_input)
        """
        This return a dictionary with the score, 
        the position of the vector of where the response begins and where it ends and the last key is the answer
        """
        return res

