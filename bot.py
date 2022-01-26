import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria
import pickle
import torch
import os

#needs about 11 gigs of VRAM. instead, you can use "CPU" if u dont have big enough card, but it will be slow
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
device = "cuda"
model_name = "EleutherAI/gpt-neo-1.3B"

transformers.logging.set_verbosity_error()




# with open('model.pkl', 'rb') as f:
#     model = pickle.load(f)







class AI():
    
    memory = []
    model = None
    story = []

    def __init__(self):
        print("Loading model")
        if not os.path.isdir(os.path.expanduser('~')+"\\.cache\\huggingface"):
            print("Model not downloaded... Downloading from huggingface now. This may take a while :)")

        
        self.model = AutoModelForCausalLM.from_pretrained(model_name, low_cpu_mem_usage=True).to(device)

        # print("saving model")
        # self.model.save_pretrained("model/")
        
        print("Loading tokenizer")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        # print("saving tokenizer")
        # self.tokenizer.save_pretrained("tokenizer/")
        self.tokenizer.padding_side = "left"
        self.tokenizer.pad_token = self.tokenizer.eos_token
        # try:
        #     with open('model.pkl', 'rb') as f:
        #         print("loading model pickle")
        #         self.model = pickle.load(f)
        #         print("Loaded model!")
        # except FileNotFoundError:
        #     print("building model")
        #     self.model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
        #     with open('model.pkl', 'wb') as f:
        #         print("saving model")
        #         pickle.dump(self.model, f)
        #         print("saved")
        


        
    def processMessage(self, user_message, bot_param):

        self.story = bot_param['story']

        if user_message.lower() == "bonk":
            self.memory = []
            return "*has concussion*"

        else:
            if len(self.memory) > 12:
                self.memory = self.memory[2:]

            context = self.story + self.memory
            context_size = len(context)
            
            #convert context list to string
            context = "\n".join(context)

            self.memory.append(bot_param['ai_name'] +": " + user_message) 

            context += "\n" + bot_param['ai_name']  + ": " + user_message + "\n"+ bot_param['ai_name'] +":"

            encoding = self.tokenizer(context, padding=True, return_tensors='pt').to(device)
            encoding_size = encoding.data['input_ids'].shape[1]

            #no_repeat_ngram_size=1 made the conversation hilarious. before it was getting stuck in repetition loops
            # for some reason it is extremely interested in using smilies in responses
            
            with torch.no_grad():
                generated_ids = self.model.generate(
                    **encoding, 
                    do_sample=True, 
                    temperature=bot_param['temp'], 
                    no_repeat_ngram_size=bot_param['no_repeat_ngram_size'], 
                    max_length=encoding_size + bot_param['max_length'],
                    length_penalty = bot_param['length_penalty'],
                    repetition_penalty = bot_param['repetition_penalty'],
                    )
                
            
            generated_texts = self.tokenizer.batch_decode(
                generated_ids, skip_special_tokens=True)

            generated_texts_list = generated_texts[0].split('\n')
            result = generated_texts_list[context_size+1]
            self.memory.append(result)

            return result
