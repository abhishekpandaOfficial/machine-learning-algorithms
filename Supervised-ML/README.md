# Supervised Machine Learning

Supervised learning uses labelled examples to learn a mapping from inputs `X` to a target `y`.

$$
\hat{f}: X \rightarrow y
$$

Use this area for projects where the target is known during training.

## Tracks

- [Classification](Classification/README.md) — predict discrete classes or probabilities.
- [Regression](Regression/README.md) — predict continuous numeric values.

## Shared project workflow

1. Define the target, intended use and decision boundaries.
2. Document the dataset source, terms, schema and feature timing.
3. Split data before fitting preprocessing and prevent leakage.
4. Establish a simple baseline.
5. Train, tune and validate the model.
6. Evaluate errors, subgroups and calibration where relevant.
7. Save the complete preprocessing-and-model pipeline.
8. Test loading, serving inputs and failure paths.
9. Export the executed notebook to HTML and PDF.
10. Document limitations, monitoring and deployment links.
