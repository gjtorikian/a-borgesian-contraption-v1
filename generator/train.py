import gpt_2_simple as gpt2
import os
import requests
import variables

model_name = variables.model_name()
file_name = variables.file_name()
run_name = variables.run_name()

if not os.path.isdir(os.path.join("models", model_name)):
    print(f"Downloading {model_name} model...")
    gpt2.download_gpt2(model_name=model_name)


sess = gpt2.start_tf_sess()
gpt2.finetune(sess,
              run_name=run_name,
              dataset=file_name,
              model_name=model_name,
              restore_from='fresh',
              steps=10000,
              print_every=100,
              sample_every=2000,
              save_every=500
              )

