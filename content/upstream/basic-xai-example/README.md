# Basic XAI Example

This repository is a small educational example for exploring explainability
signals from LLM outputs. It uses the OpenAI API to ask two simple questions,
prints the model's answers and reasoning summaries, embeds the answer text line
by line, and visualizes the resulting embeddings with UMAP.

The notebook is intentionally compact. It is meant to show how generated
answers, model-provided reasoning summaries, and embedding plots can support
basic inspection of model behavior. It does not expose hidden chain-of-thought,
and it is not compliance or legal advice.

## Background Reading

This example is related to reasoning-oriented prompting, human review of model
outputs, and embedding-based inspection of generated text. Useful background
references include:

- Wei, Jason, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi,
  Quoc V. Le, and Denny Zhou. "Chain-of-thought prompting elicits reasoning in
  large language models." *Advances in Neural Information Processing Systems*
  35 (2022): 24824-24837.

  https://proceedings.neurips.cc/paper_files/paper/2022/file/9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf

- Sudjianto, Agus, Aijun Zhang, Srinivas Neppalli, Tarun Joshi, and Michal
  Malohlava. "Human-calibrated automated testing and validation of generative
  language models." arXiv preprint arXiv:2411.16391 (2024).

  https://arxiv.org/pdf/2411.16391

## Contents

- `CoT_Summary_Embeddings_Code_Apache2.ipynb`: Jupyter notebook that requests
  model answers and reasoning summaries, embeds response lines, and plots the
  embedding projection.
- `requirements.txt`: Python dependencies for running the notebook.
- `LICENSE`: Apache License 2.0.

## What the Notebook Demonstrates

The notebook walks through a basic XAI-oriented inspection workflow:

1. Connect to the OpenAI API using `OPENAI_API_KEY` or a secure notebook prompt.
2. Ask a simple arithmetic question and print the model answer.
3. Print the model-provided reasoning summary for that answer.
4. Ask a short conceptual comparison question and print the model answer.
5. Print the model-provided reasoning summary for the second answer.
6. Split both answer texts into lines and embed those lines with an OpenAI
   embedding model.
7. Normalize the embeddings, project them into two dimensions with UMAP, and
   plot the two response sets for visual comparison.

## Setup

From the repository root, create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start Jupyter:

```bash
jupyter notebook
```

Then open `CoT_Summary_Embeddings_Code_Apache2.ipynb` and run the cells in
order.

## Supplying an OpenAI API Key

The notebook looks for an API key in the `OPENAI_API_KEY` environment variable.
If that variable is not set, the notebook asks you to paste the key into a
secure prompt.

### macOS or Linux

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Then start Jupyter or run the notebook from the same terminal session.

### Windows PowerShell

```powershell
$env:OPENAI_API_KEY = "your_api_key_here"
```

Then start Jupyter or run the notebook from the same PowerShell session.

### Secure Notebook Prompt

If you do not set `OPENAI_API_KEY`, run the connection cell and paste your key
when prompted:

```python
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    api_key = getpass("Enter your OpenAI API key: ")

client = OpenAI(api_key=api_key)
```

Do not commit API keys to this repository.

## License

Code in this repository is licensed under the Apache License, Version 2.0. See
`LICENSE` for details.
