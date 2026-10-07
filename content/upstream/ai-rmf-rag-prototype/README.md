# ai-rmf-rag-prototype

Prototype RAG system for NIST AI RMF materials. 

#### Install Instructions

$ `git clone https://github.com/hallresearch-ai/ai-rmf-rag-prototype.git`

$ `cd ai-rmf-rag-prototype`

$ `python3 -m venv ./ai_rmf_rag_env` # Prototype tested on Python 3.8.16, GCC 7.5.0 on linux

$ `source ai_rmf_rag_env/bin/activate`

$ `ai_rmf_rag_env/bin/pip install --upgrade pip` 

$ `ai_rmf_rag_env/bin/pip install -r requirements.txt`

##### Additional configuration steps (if necessary)
- OpenAI account, authentication key, and authentication 

#### Wave app instructions
$ `export H2O_WAVE_APP_READ_TIMEOUT=-1; wave run form.form --no-reload`

Open browswer and navigate to: `http://localhost:10101/form`

#### Jupyter interface instructions
$ `ai_rmf_rag_env/bin/jupyter notebook`

Open `RAG_query_jupyter_client.ipynb` and follow instructions

#### Current contents

`$ tree -f -I '.git|__pycache__|ai_rmf_rag_env|.idea'`
```commandline
├── ./form
    └── ./form/form.py                                          # wave app client 
├── ./LICENSE                                                   # MIT License
├── ./pipe
    ├── ./pipe/get_embeddings.ipynb                             # jupyter notebook for embedding AI RMF text
│   └── ./pipe/text_tagger.ipynb                                # jupyter notebook for applying topic model tags
├── ./rag_data
    ├── ./rag_data/20241106_ada_action_embeddings.csv           # embeddings for actions
    ├── ./rag_data/20241106_ada_topic_embeddings.csv            # embeddings for topics
    └── ./rag_data/rmf_all_actions_redlined_tagged.csv          # AI RMF categories, subcategories, and actions as CSV spreadsheet 
├── ./RAG_query_jupyter_client.ipynb                            # jupyter notebook client                     
├── ./README.md                                                 # this README.md file 
├── ./requirements.txt                                          # required Python packages
├── ./ann_search_dict.pkl                                       # dictionary used for handling app state
├── ./search_dict.pkl                                           # dictionary used for handling app state
├── ./state_dict.pkl                                            # dictionary used for handling app state
└── ./utils.py                                                  # simple backed module

3 directories, 14 files
```

#### Unit test instructions


