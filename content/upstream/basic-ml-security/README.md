## Basic ML Security Example

Shows simple attacks on a classifier based model extraction and adversarial examples. 

## Background Reading

- Tramèr, Florian, Fan Zhang, Ari Juels, Michael K. Reiter, and Thomas
  Ristenpart. "Stealing machine learning models via prediction APIs." In 25th
  USENIX security symposium (USENIX Security 16), pp. 601-618. 2016. https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/tramer.

  
- Barreno, Marco, Blaine Nelson, Anthony D. Joseph, and J. Doug Tygar. "The
  security of machine learning." Machine learning 81, no. 2 (2010): 121-148. https://people.eecs.berkeley.edu/~adj/publications/paper-files/SecML-MLJ2010.pdf.


- Hall, Patrick, James Curtis, and Parul Pandey. Machine learning for high-risk
  applications: approaches to responsible AI. O'Reilly Media, Inc., 2023.
  Chapter 11. https://www.oreilly.com/library/view/machine-learning-for/9781098102425/. 

## Contents

- `Red_Teaming_an_XGBoost_model_Code_Apache2.ipynb`: Jupyter notebook that
  loads `credit_line_increase.csv`, trains an XGBoost classifier, demonstrates
  a model extraction attack, and demonstrates a tree-informed adversarial
  example attack.
- `credit_line_increase.csv`: Example credit line dataset used for model
  training and attack demos.
- `requirements.txt`: Minimal Python dependencies needed to run the notebook.
- `LICENSE`: Apache License 2.0.

## What the Notebook Demonstrates

1. Load the credit line dataset and define the model features and target.
2. Split the data into train, validation, and test sets.
3. Train one unconstrained XGBoost model on the training data.
4. Inspect the fitted model with basic explanations such as score quality and
   feature importance.
5. Run a simple model extraction attack by querying the black-box model on
   synthetic inputs and training a surrogate model to imitate its outputs.
6. Demonstrate a tree-informed adversarial example attack that uses the
   extracted surrogate model to infer a subtle, plausible one-feature edit to a
   customer record.

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

Then open `Red_Teaming_an_XGBoost_model_Code_Apache2.ipynb` and run the cells
in order.

## License

This repository is licensed under the Apache License, Version 2.0. See
`LICENSE` for details.
