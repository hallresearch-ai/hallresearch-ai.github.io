# Basic ML Evaluation Example

This repository is a small educational example for evaluating supervised
machine learning model scores against known labels. It compares three sets of
binary classification probability scores using common metrics, then ranks the
models across repeated folds.

## Background Reading

This example is related to the broader topic of evaluating models with multiple
performance measures. For a classic discussion of model evaluation across
different supervised learning metrics, see:

Caruana, R., Joachims, T., & Backstrom, L. (2004). *KDD-Cup 2004: Results and
Analysis*. https://www.cs.cornell.edu/~lars/kdd04.pdf.


## Contents

- `Supervised_Eval_Apache2.ipynb`: Jupyter notebook that loads the data,
  evaluates the model scores, and ranks the models.
- `key.csv`: Known target labels. The target column is `high_priced`.
- `model_a.csv`, `model_b.csv`, `model_c.csv`: Model score files. Each file
  contains a `phat` column with predicted probabilities for the positive class.
- `requirements.txt`: Minimal Python dependencies.
- `LICENSE`: Apache License 2.0.

## What the Notebook Demonstrates

The notebook walks through a basic model-comparison workflow:

1. Load the known labels from `key.csv`.
2. Load predicted probabilities from the three model files.
3. Assign examples to reproducible random folds.
4. Evaluate each model on each fold with:
   - accuracy
   - ROC AUC
   - log loss
5. Rank the models for each metric and fold.
6. Average the ranks to summarize overall performance.

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

Then open `Supervised_Eval_Apache2.ipynb` and run the cells in order.

## License

This repository is licensed under the Apache License, Version 2.0. See
`LICENSE` for details.
