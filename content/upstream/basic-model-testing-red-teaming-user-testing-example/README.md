# Basic Model Testing, Red Teaming, and Field Testing Example

This repository contains a small educational example for running basic LLM evaluation workflows.

## Background Reading

The example is inspired by the layered evaluation approach described in NIST AI 700-2, *Assessing Risks and Impacts of AI (ARIA): ARIA 0.1: Pilot Evaluation Report*, which discusses model testing, red teaming, and field testing as complementary parts of AI system evaluation.

NIST. *Assessing Risks and Impacts of AI (ARIA): ARIA 0.1: Pilot Evaluation Report*. NIST AI 700-2, November 2025. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.700-2.pdf.


## Contents

- `Model_Testing_Simple_Code_Apache2.ipynb`: a toy multiple-choice model testing benchmark.
- `Red_Teaming_Simple_Code_Apache2.ipynb`: a simple red-teaming prompt example for evaluating validity and reliability.
- `Red_Teaming_Multitasking_Counterfactuals_Code_Apache2.ipynb`: prompt examples for evaluating fairness and bias management, making use of BISG.
- `Field_Testing_Rubric_CC_By.md`: a basic user-/field-testing rubric for human evaluation.
- `requirements.txt`: Python dependencies for running the notebooks.


## What the Notebook Demonstrates

These examples show a minimal version of a more comprehensive LLM evaluation workflow, aligned with the model testing, red teaming, and field testing layers discussed in NIST AI 700-2. The goal is to demonstrate that useful evaluation should look at more than one kind of evidence.

The model testing notebook shows how to check basic model assumptions and task performance by sending a small set of benchmark questions to a model, collecting the model's responses, comparing them to expected answers, and calculating a simple accuracy score. In a real evaluation, this kind of test set should be adapted to the intended use case, expanded beyond a few examples, and rerun to understand performance variation.

The red-teaming notebook shows how to probe model behavior under a more challenging or adversarial usage scenario. This kind of testing helps identify issues that ordinary benchmark questions may miss, such as unsupported claims, incorrect or misleading instructions, unsafe guidance, privacy concerns, or failure to stay within an intended operating boundary.

The user-/field-testing rubric shows how human reviewers can evaluate model outputs in realistic interaction contexts. It provides a simple scoring structure for dimensions such as accuracy, relevance, completeness, clarity, instruction following, usefulness, and safety. This complements automated model testing and adversarial probing by capturing how outputs may affect actual users.

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

Then open `Model_Testing_Simple_Code_Apache2.ipynb`,
`Red_Teaming_Simple_Code_Apache2.ipynb`, or
`Red_Teaming_Multitasking_Counterfactuals_Code_Apache2.ipynb` and run the cells
in order.


## Supplying an OpenAI API Key

The notebooks look for an API key in the `OPENAI_API_KEY` environment variable. If that variable is not set, the notebooks ask you to paste the key into a secure prompt.

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

If you do not set `OPENAI_API_KEY`, run the connection cell and paste your key when prompted:

```python
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    api_key = getpass("Enter your OpenAI API key: ")

client = OpenAI(api_key=api_key)
```

Do not commit API keys to this repository.

## Licenses

Code in this repository is licensed under the Apache License, Version 2.0. See
`CODE_LICENSE` for details. Other materials in this repository are licensed under the
Creative Commons Attribution 4.0 International License (CC BY 4.0). See
`MATERIAL_LICENSE` for details.
