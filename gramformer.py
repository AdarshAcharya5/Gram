class Gramformer:

  def __init__(self, models=1, use_gpu=False):
    from transformers import AutoTokenizer
    from transformers import AutoModelForSeq2SeqLM
    
    if use_gpu:
        device= "cuda:0"
    else:
        device = "cpu"      
    self.device = device
    correction_model_tag = "prithivida/grammar_error_correcter_v1"
    self.model_loaded = False

    if models == 1:
        #Load the tokenizer from pretrained model
        self.correction_tokenizer = AutoTokenizer.from_pretrained(correction_model_tag)
        #Load Seq2Seq2 pretrained dataset model
        self.correction_model     = AutoModelForSeq2SeqLM.from_pretrained(correction_model_tag)
        self.correction_model     = self.correction_model.to(device)
        self.model_loaded = True
        print("[Gram] Grammar error correction model loaded..")

  def correct(self, input_sentence, max_candidates=1):
      if self.model_loaded:
        correction_prefix = "gec: "
        input_sentence = correction_prefix + input_sentence
        input_ids = self.correction_tokenizer.encode(input_sentence, return_tensors='pt')
        input_ids = input_ids.to(self.device)
        preds = self.correction_model.generate(input_ids, do_sample=True, max_length=128, num_beams=7, early_stopping=True, num_return_sequences=max_candidates)
        corrected = set()
        for pred in preds:  
          corrected.add(self.correction_tokenizer.decode(pred, skip_special_tokens=True).strip())

        return corrected
      else:
        print("Model is not loaded")  
        return None