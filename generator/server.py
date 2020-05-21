from starlette.applications import Starlette
from starlette.responses import UJSONResponse
import uvicorn
import os
import gc
import variables
import random

from transformers import GPT2Config, GPT2Tokenizer, GPT2LMHeadModel
import torch
from torch.nn import functional as F

app = Starlette(debug=False)

temperature = 0.9
# top_k = 9
top_p = 0.9
repetition_penalty = 1.4

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("Loading model ...")
model = GPT2LMHeadModel.from_pretrained('./pytorch')
model.to(device)
print("Model loaded!")
tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')

# Needed to avoid cross-domain issues
response_header = {
    'Access-Control-Allow-Origin': '*'
}

generate_count = 0
text_length = variables.length()

prompts = []
with open('prompts.txt') as fh:
    for line in fh:
        prompts.append(line.rstrip("\n"))


@app.route('/', methods=['GET'])
async def hello(request):
    return UJSONResponse({'greeting': "hello"},
                         headers=response_header)


@app.route('/start', methods=['GET'])
async def start(request):
    p = random.sample(prompts, 5)

    return UJSONResponse({'prompts': p},
                         headers=response_header)


@app.route('/prompt', methods=['POST'])
async def prompt(request):
    params = await request.json()

    prefix = params.get('prefix')
    length = params.get('length', 22)
    length = min(length, 22)
    prompt = sequence(prefix, 1, length)[0]

    return UJSONResponse({'prompt': prompt},
                         headers=response_header)


@app.route('/generate', methods=['POST'])
async def generate(request):
    params = await request.json()

    prefix = params.get('prefix')
    length = params.get('length', 10)
    length = min(length, 10)
    generated_sequences = sequence(prefix, 5, length)

    return UJSONResponse({'prompts': generated_sequences},
                         headers=response_header)


def sequence(prefix, num_return_sequences, length):
    encoded_prompt = tokenizer.encode(
        prefix, add_special_tokens=False, return_tensors="pt")
    encoded_prompt = encoded_prompt.to(device)
    encoded_prompt_length = len(tokenizer.decode(encoded_prompt[0],
                                                 clean_up_tokenization_spaces=True))

    single_generate = True if num_return_sequences == 1 else False

    max_length = length + len(encoded_prompt[0]) + 1

    generated_sequences = []

    for s in range(num_return_sequences):
        generated_sequence = model.generate(
            input_ids=encoded_prompt,
            max_length=max_length,
            temperature=temperature + ((s-1) * 0.4),
            # top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            do_sample=True,
        )[0]

        # Decode text
        text = tokenizer.decode(
            generated_sequence, clean_up_tokenization_spaces=True)

        # Remove the excess text that was used for pre-processing
        total_sequence = (
            text[encoded_prompt_length:]
        )

        total_sequence = total_sequence.replace('\n', ' ')

        if single_generate:
            total_sequence = variables.truncate(total_sequence, 40)

        generated_sequences.append(total_sequence)

    gc.collect()

    return generated_sequences


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(
        os.environ.get('PORT', 8080)))
