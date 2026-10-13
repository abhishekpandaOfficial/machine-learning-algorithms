# Machine Learning Foundations — Question Bank 001–050

> **Status:** v1 learning release · **Scope:** fundamentals, data preparation, algorithms, evaluation, debugging, and scenarios.
>
> Every question includes a direct answer, practical example, common pitfall, and practice prompt. Question IDs are stable and must not be renumbered after publication.

## How to use this file

- In VS Code, open this file and use Markdown Preview.
- In Jupyter or Colab, use the companion notebook for runnable experiments; this file is the theory and Q&A reference.
- The website build script converts this Markdown source into searchable, expandable question cards.
- Add new questions with the next unused ID.

## Coverage

- **001–010:** Foundations and lifecycle
- **011–020:** Data preparation and leakage
- **021–030:** Algorithms and ensembles
- **031–040:** Metrics and validation
- **041–050:** Debugging, production scenarios, and capstone

---

## ML-FND-001 — What is machine learning?

**Difficulty:** Beginner · **Type:** Concept · **Tags:** fundamentals, definition

### Answer

Machine learning (ML) is a field of AI in which a system learns statistical patterns from examples to make predictions or decisions on new inputs. Instead of manually writing every decision rule, we define an objective, provide data, choose a learning procedure, and evaluate the resulting model.

### Example

A model learns relationships between house size, location, and historical sale prices, then estimates the price of a new house.

### Common pitfall

ML does not automatically understand causality or guarantee correct predictions. It learns patterns shaped by the data and objective.

### Practice

Name one task where a learned pattern is more practical than a long list of hand-written rules.

---


## ML-FND-002 — How is AI different from machine learning and deep learning?

**Difficulty:** Beginner · **Type:** Concept · **Tags:** AI, ML, deep-learning

### Answer

Artificial intelligence is the broad goal of building systems that perform tasks associated with intelligence. Machine learning is one approach within AI that learns from data. Deep learning is a subset of ML that uses multi-layer neural networks.

### Example

A rule-based chess engine can be AI without ML; a spam classifier can use ML; a speech model can use deep learning.

### Common pitfall

The terms are related but not interchangeable. Not every AI system learns from data, and not every ML model is a neural network.

### Practice

Place a rule-based expert system, random forest, and transformer into the correct categories.

---


## ML-FND-003 — What are features, labels, parameters, and hyperparameters?

**Difficulty:** Beginner · **Type:** Concept · **Tags:** features, labels, training

### Answer

Features are input variables used for prediction. A label or target is the outcome the model is trained to predict. Parameters are values learned from data, while hyperparameters are settings chosen before or around training.

### Example

For house-price prediction, area and bedrooms are features, sale price is the label, regression coefficients are parameters, and regularization strength is a hyperparameter.

### Common pitfall

A column can be available in a dataset but still be invalid as a feature if it leaks the target or would not exist at prediction time.

### Practice

For a churn model, list two features, the label, one learned parameter, and one hyperparameter.

---


## ML-FND-004 — What is the difference between supervised, unsupervised, and reinforcement learning?

**Difficulty:** Beginner · **Type:** Comparison · **Tags:** learning-types

### Answer

Supervised learning uses labeled examples to predict targets. Unsupervised learning searches for structure in data without a target label. Reinforcement learning learns actions through rewards and interaction with an environment.

### Example

Predicting churn is supervised; grouping customers without known groups is unsupervised; training an agent to navigate a maze using rewards is reinforcement learning.

### Common pitfall

Do not choose an approach based on trendiness. Choose it based on available feedback and the actual problem objective.

### Practice

A retailer has no customer-segment labels but wants to discover groups. Which learning setup is a reasonable first experiment, and why?

---


## ML-FND-005 — When should a problem be framed as classification versus regression?

**Difficulty:** Beginner · **Type:** Problem framing · **Tags:** classification, regression

### Answer

Classification predicts a discrete class or class probability, while regression predicts a numeric quantity. The business decision and target definition matter more than the algorithm name.

### Example

Predicting whether a payment is fraudulent is classification; predicting the amount of next month's sales is regression.

### Common pitfall

A numeric-looking target is not automatically regression: product IDs are identifiers, not continuous quantities.

### Practice

Frame these targets: delivery time in minutes, disease category, and customer satisfaction rating from 1 to 5. State any ambiguity.

---


## ML-FND-006 — What are training, validation, and test sets for?

**Difficulty:** Beginner · **Type:** Concept · **Tags:** splits, generalization

### Answer

The training set fits model parameters. The validation set helps select models and tune hyperparameters. The test set estimates final performance after decisions are complete.

### Example

Use training data to fit models, validation data to compare regularization strengths, and a held-out test set once for final reporting.

### Common pitfall

Repeatedly choosing models based on test performance leaks information from the test set into development decisions.

### Practice

Explain why a test set should not be used to choose the best hyperparameter.

---


## ML-FND-007 — What is generalization in machine learning?

**Difficulty:** Beginner · **Type:** Concept · **Tags:** generalization, evaluation

### Answer

Generalization is the ability of a trained model to perform well on new examples drawn from the intended deployment setting. It is estimated using data that was not used to fit or select the model.

### Example

A loan-risk model should work on future eligible applications, not just the historical records used during training.

### Common pitfall

High training accuracy is not proof of generalization. Distribution changes, leakage, and unrepresentative evaluation data can all mislead.

### Practice

Give one reason a model may fail after deployment even if its test score was strong.

---


## ML-FND-008 — What are underfitting and overfitting?

**Difficulty:** Beginner · **Type:** Comparison · **Tags:** bias-variance, overfitting

### Answer

Underfitting occurs when a model cannot capture important structure in the data. Overfitting occurs when it captures training-specific noise or quirks that do not transfer to new data.

### Example

A straight line may underfit a strongly nonlinear relationship; a very deep tree may memorize a small training dataset.

### Common pitfall

Increasing model complexity is not always the solution. Compare training and validation performance and check data quality first.

### Practice

A model scores poorly on both training and validation sets. Which failure is more likely, and what else should you inspect?

---


## ML-FND-009 — What is the end-to-end machine learning lifecycle?

**Difficulty:** Beginner · **Type:** Workflow · **Tags:** lifecycle, mlops

### Answer

A practical lifecycle includes problem framing, data collection, data validation, splitting, preprocessing, baseline creation, training, evaluation, deployment, monitoring, and retraining or retirement.

### Example

A churn project starts with defining churn and its prediction horizon, then builds a leakage-safe dataset, evaluates a baseline, deploys predictions, and monitors drift and business outcomes.

### Common pitfall

The lifecycle is iterative. Monitoring can reveal data problems or a changed objective that requires revisiting earlier steps.

### Practice

Which lifecycle stage catches a feature that becomes available only after a customer has already churned?

---


## ML-FND-010 — Why should a machine learning project start with a baseline?

**Difficulty:** Beginner · **Type:** Problem solving · **Tags:** baseline, metrics

### Answer

A baseline is a simple, explicit reference that a more complex approach must beat. It reveals whether the data, metric, and workflow provide useful signal before spending effort on sophisticated models.

### Example

For imbalanced fraud detection, compare against a simple rule or a model that predicts no fraud, but use metrics that expose the baseline's limitations.

### Common pitfall

A baseline is not necessarily a useful production model. It is a comparison point, and the baseline metric must match the problem.

### Practice

Choose a baseline for numeric demand forecasting and explain which metric you would compare.

---


## ML-FND-011 — How do you distinguish numerical, categorical, ordinal, and datetime features?

**Difficulty:** Beginner · **Type:** Data understanding · **Tags:** data-types, preprocessing

### Answer

Numerical features represent quantities; nominal categorical features represent unordered groups; ordinal features have meaningful order; datetime features encode calendar or time structure. Their semantics determine preprocessing.

### Example

Income is numeric, browser is nominal categorical, satisfaction level may be ordinal, and order timestamp is datetime.

### Common pitfall

Integer encoding does not make a category numeric. Treating category IDs as magnitudes can create false relationships.

### Practice

Classify postal code, temperature, education level, and signup date. Explain the tricky case.

---


## ML-FND-012 — How should missing values be handled?

**Difficulty:** Beginner · **Type:** Technique · **Tags:** missing-data, imputation

### Answer

First measure missingness by column, row, time, and subgroup. Then decide whether to remove records, impute values, add missingness indicators, or investigate the data collection process. Fit imputation rules on training data only.

### Example

Median imputation can be a robust starting point for skewed numeric features; most-frequent or an explicit unknown category can work for some categorical fields.

### Common pitfall

Missingness may itself carry signal, and a missing value can mean not applicable rather than unknown. Never compute imputation statistics using the test set.

### Practice

A medical test is absent more often for one patient group. What checks should precede choosing an imputation method?

---


## ML-FND-013 — When should numerical features be scaled?

**Difficulty:** Beginner · **Type:** Technique · **Tags:** scaling, preprocessing

### Answer

Scaling changes feature magnitudes. Standardization subtracts the training mean and divides by the training standard deviation; min-max scaling maps values to a chosen range. Distance-based and gradient-based models often benefit from scaling.

### Example

K-nearest neighbors and regularized logistic regression can be sensitive to feature scales; many tree-based models are much less sensitive.

### Common pitfall

Fit the scaler on training data and reuse that fitted scaler at inference. Scaling the whole dataset before splitting leaks test-set information.

### Practice

Why could a distance-based model treat annual income as more important than age if neither is scaled?

---


## ML-FND-014 — How do one-hot encoding and ordinal encoding differ?

**Difficulty:** Beginner · **Type:** Comparison · **Tags:** categorical-encoding

### Answer

One-hot encoding creates indicator columns for categories without imposing an order. Ordinal encoding maps categories to ordered integers and is appropriate when that order is meaningful or the estimator handles categorical values accordingly.

### Example

Color can be one-hot encoded; a genuinely ordered level such as low, medium, high may use ordinal encoding.

### Common pitfall

Encoding red=1, green=2, blue=3 does not imply blue is three times red or that green lies between them in a meaningful numeric sense.

### Practice

Which encoding would you try first for city names in a linear model, and why?

---


## ML-FND-015 — What is data leakage, and why is it dangerous?

**Difficulty:** Intermediate · **Type:** Failure analysis · **Tags:** data-leakage, validation

### Answer

Data leakage occurs when training or model selection uses information that would not legitimately be available at prediction time. It produces overly optimistic evaluation and often disappointing deployment performance.

### Example

Using a post-discharge diagnosis to predict hospital admission risk, or scaling all data before splitting, can leak information.

### Common pitfall

Leakage can come from timestamps, duplicate entities, target-derived fields, preprocessing, or careless split design—not just an obvious target column.

### Practice

Give two ways leakage can occur in a customer churn dataset.

---


## ML-FND-016 — What is a preprocessing pipeline, and why use one?

**Difficulty:** Intermediate · **Type:** Engineering · **Tags:** pipeline, reproducibility

### Answer

A preprocessing pipeline chains transformations and an estimator into one fitted workflow. It ensures the same learned transformations are applied during training, validation, and inference and makes cross-validation safer.

### Example

A scikit-learn pipeline can impute missing values, one-hot encode categories, scale numeric features, and fit logistic regression as one estimator.

### Common pitfall

Preprocessing outside the pipeline can accidentally fit transformations on validation data or cause training-serving skew.

### Practice

Name three transformations you would keep inside a pipeline for mixed numeric and categorical tabular data.

---


## ML-FND-017 — What is feature engineering?

**Difficulty:** Beginner · **Type:** Technique · **Tags:** feature-engineering

### Answer

Feature engineering converts raw inputs into representations that better expose relevant signal to a model. It relies on domain understanding and must respect when each value becomes available.

### Example

For transaction fraud, features may include transaction amount relative to a customer's historical median and the count of recent transactions in a time window.

### Common pitfall

Engineered features must be computed using only information available at prediction time and should be validated for subgroup effects.

### Practice

Propose a leakage-safe feature for predicting whether a subscription customer will renew next month.

---


## ML-FND-018 — What is the difference between feature selection and dimensionality reduction?

**Difficulty:** Intermediate · **Type:** Comparison · **Tags:** feature-selection, pca

### Answer

Feature selection keeps a subset of original features. Dimensionality reduction transforms data into a smaller representation, potentially combining information from many features.

### Example

Selecting the ten most useful columns is feature selection; PCA transforms correlated numeric columns into principal components.

### Common pitfall

PCA components can be harder to interpret and must be fitted on training data only. Feature selection can also leak if done before cross-validation.

### Practice

Which approach better preserves the original feature names for a regulated model explanation?

---


## ML-FND-019 — How do you detect and handle duplicate records?

**Difficulty:** Intermediate · **Type:** Data quality · **Tags:** duplicates, entities

### Answer

Identify exact duplicates and semantic duplicates separately. Determine whether repeated rows represent ingestion errors, multiple valid events, or repeated measurements before removing anything.

### Example

Two identical customer profiles may be duplicate imports, while two identical product purchases can be separate legitimate transactions.

### Common pitfall

Dropping duplicates without understanding entity IDs and timestamps can remove valid observations or leave near-duplicates across train and test sets.

### Practice

Why can near-duplicate customer records across training and test sets inflate evaluation scores?

---


## ML-FND-020 — How should data be split when observations are time-dependent or grouped?

**Difficulty:** Intermediate · **Type:** Validation design · **Tags:** time-series, group-split

### Answer

Use a time-aware split for forecasting future observations and group-aware splitting when rows from the same person, patient, device, or account must not cross partitions. Random splitting is appropriate only when its assumptions fit the data.

### Example

Train on earlier months and validate on later months for demand forecasting; keep all visits from one patient in the same partition when evaluating generalization to new patients.

### Common pitfall

A random split can leak future patterns or entity-specific information. The split should mimic the deployment question.

### Practice

For a model intended for new hospitals, what group should guide the split?

---


## ML-FND-021 — How does linear regression make predictions?

**Difficulty:** Beginner · **Type:** Algorithm · **Tags:** linear-regression, regression

### Answer

Linear regression predicts a numeric target using a weighted sum of input features, often with an intercept. Ordinary least squares chooses coefficients that minimize the sum of squared residuals on the training data.

### Example

A simple model can estimate house price from floor area: predicted price = intercept + coefficient × area.

### Common pitfall

A linear model is linear in its parameters, not necessarily restricted to raw straight-line relationships; engineered transformations can represent nonlinear patterns.

### Practice

What does a positive coefficient mean, and why does it not automatically prove causation?

---


## ML-FND-022 — How does logistic regression perform classification?

**Difficulty:** Beginner · **Type:** Algorithm · **Tags:** logistic-regression, classification

### Answer

For binary classification, logistic regression maps a linear score through the sigmoid function to estimate a probability between zero and one. A decision threshold converts that probability into a class prediction.

### Example

A churn model might estimate a 0.78 probability of churn; the chosen action threshold depends on intervention cost and benefit.

### Common pitfall

Despite its name, logistic regression is commonly used for classification. Its probabilities still need calibration checks, and the default threshold of 0.5 is not universally optimal.

### Practice

Why might a business choose a threshold of 0.25 instead of 0.5?

---


## ML-FND-023 — What does a decision tree learn?

**Difficulty:** Beginner · **Type:** Algorithm · **Tags:** decision-tree

### Answer

A decision tree recursively splits data using feature-based rules chosen to improve a criterion such as impurity reduction or loss. Predictions are produced by the terminal leaf reached by an example.

### Example

A loan tree might split first on debt-to-income ratio and then on missed payments to estimate default risk.

### Common pitfall

Deep trees can overfit, and small data changes can produce different tree structures. Control complexity and validate performance.

### Practice

What happens to bias and variance when an unconstrained tree is allowed to grow very deep?

---


## ML-FND-024 — Why can a random forest outperform a single decision tree?

**Difficulty:** Intermediate · **Type:** Algorithm · **Tags:** random-forest, ensembles

### Answer

A random forest averages predictions from many trees trained with bootstrap samples and randomized feature subsets. This reduces variance compared with relying on one unstable tree, often improving generalization.

### Example

For customer-risk classification, a forest can combine many different tree decision boundaries instead of depending on one tree's splits.

### Common pitfall

More trees increase compute and do not guarantee better results on every dataset. Forests can be less interpretable than a single tree.

### Practice

Why does randomizing features help decorrelate trees in a forest?

---


## ML-FND-025 — What is gradient boosting?

**Difficulty:** Intermediate · **Type:** Algorithm · **Tags:** boosting, ensembles

### Answer

Gradient boosting builds an additive sequence of weak learners, where later learners reduce the loss left by the current ensemble. Learning rate, tree depth, number of estimators, and regularization affect its behavior.

### Example

Gradient-boosted trees are strong candidates for many tabular prediction tasks such as demand, churn, and credit-risk scoring.

### Common pitfall

Boosting can overfit noisy data and requires careful validation. A smaller learning rate often needs more boosting rounds.

### Practice

How would you diagnose a boosted model whose training score improves while validation score deteriorates?

---


## ML-FND-026 — How does k-nearest neighbors make a prediction?

**Difficulty:** Beginner · **Type:** Algorithm · **Tags:** knn, distance

### Answer

K-nearest neighbors finds the k training examples closest to a new point under a chosen distance measure, then aggregates their labels or values. It is a local, instance-based method.

### Example

For classification, a new customer can receive the majority class among nearby historical customers.

### Common pitfall

KNN is sensitive to scaling, irrelevant dimensions, the distance metric, and the choice of k. Prediction can be expensive on large datasets.

### Practice

What is the likely effect of increasing k on a noisy classification problem?

---


## ML-FND-027 — What is the core idea behind a support vector machine?

**Difficulty:** Intermediate · **Type:** Algorithm · **Tags:** svm, margin

### Answer

A support vector machine seeks a decision boundary with a large margin between classes. Kernel methods can represent nonlinear boundaries by comparing examples through a kernel function.

### Example

An RBF-kernel SVM may separate a nonlinear pattern that a straight linear boundary cannot capture.

### Common pitfall

SVMs can be sensitive to scaling and hyperparameters; kernel SVMs may become costly as the training set grows.

### Practice

Why should you usually scale features before fitting an SVM?

---


## ML-FND-028 — What does k-means clustering optimize?

**Difficulty:** Beginner · **Type:** Algorithm · **Tags:** k-means, clustering

### Answer

K-means partitions observations into k clusters by iteratively assigning points to the nearest centroid and recomputing centroids to reduce within-cluster squared distances.

### Example

A retailer can explore groups of stores based on normalized sales and footfall features.

### Common pitfall

K-means requires choosing k and works best for cluster structures compatible with its distance and centroid assumptions. It is sensitive to scaling and outliers.

### Practice

Why can one extreme outlier pull a cluster centroid away from the main group?

---


## ML-FND-029 — What is principal component analysis (PCA)?

**Difficulty:** Intermediate · **Type:** Algorithm · **Tags:** pca, dimensionality-reduction

### Answer

PCA transforms correlated numeric features into orthogonal principal components ordered by the variance they explain. It can compress data or help visualize high-dimensional structure.

### Example

Reducing many correlated sensor measurements to a few components can simplify exploration or downstream modeling.

### Common pitfall

High explained variance does not guarantee preservation of predictive signal or interpretability. Scale features when their units otherwise dominate variance.

### Practice

Why might PCA be unsuitable if preserving original feature-level explanations is essential?

---


## ML-FND-030 — What is the difference between bagging and boosting?

**Difficulty:** Intermediate · **Type:** Comparison · **Tags:** ensembles, bagging, boosting

### Answer

Bagging trains models independently or in parallel on resampled data and aggregates them, primarily reducing variance. Boosting trains learners sequentially so later learners address errors represented by the current objective, often reducing bias and improving fit.

### Example

Random forests use bagging-style sampling; gradient-boosted trees build an additive sequence of learners.

### Common pitfall

These are broad tendencies, not guarantees. Both methods can trade accuracy, variance, robustness, and interpretability differently by dataset.

### Practice

Which family is naturally parallel across its base learners, and why?

---


## ML-FND-031 — What is a confusion matrix?

**Difficulty:** Beginner · **Type:** Metric · **Tags:** classification, confusion-matrix

### Answer

A binary confusion matrix counts true positives, true negatives, false positives, and false negatives at a chosen threshold. It exposes the types of classification errors, not just their total.

### Example

For fraud detection, a false negative is a fraudulent transaction missed by the system; a false positive is a legitimate transaction flagged as fraud.

### Common pitfall

Always state which class is considered positive. Confusion-matrix counts change with the threshold and evaluation population.

### Practice

In a disease-screening setting, which error is a false negative and why might it be costly?

---


## ML-FND-032 — When is accuracy a misleading metric?

**Difficulty:** Beginner · **Type:** Metric · **Tags:** accuracy, imbalance

### Answer

Accuracy is the fraction of all predictions that are correct. It can hide poor minority-class performance when classes are imbalanced or when different error types have different costs.

### Example

If only 1% of transactions are fraudulent, predicting every transaction as legitimate yields 99% accuracy but detects no fraud.

### Common pitfall

Do not discard accuracy automatically; use it alongside metrics that reflect the class distribution and business objective.

### Practice

Name two metrics you would inspect in addition to accuracy for an imbalanced fraud classifier.

---


## ML-FND-033 — How do precision and recall differ?

**Difficulty:** Beginner · **Type:** Metric · **Tags:** precision, recall

### Answer

Precision is the fraction of predicted positives that are truly positive. Recall is the fraction of actual positives that the model successfully finds. Increasing one can reduce the other as the threshold changes.

### Example

High precision matters when fraud alerts are expensive to investigate; high recall matters when missing fraud is especially costly.

### Common pitfall

Precision depends on prevalence, and neither precision nor recall alone fully describes performance.

### Practice

If a review team can investigate only 100 alerts a day, why might precision at that workload matter?

---


## ML-FND-034 — What do F1 score and F-beta score measure?

**Difficulty:** Intermediate · **Type:** Metric · **Tags:** f1, f-beta

### Answer

F1 is the harmonic mean of precision and recall, giving them equal weight. F-beta generalizes the balance: beta greater than one emphasizes recall, while beta below one emphasizes precision.

### Example

A screening workflow may prefer an F2 score when missed positive cases are substantially more costly than extra follow-up checks.

### Common pitfall

F-scores ignore true negatives and do not directly encode financial costs. They should not replace explicit utility analysis when costs are known.

### Practice

Which F-beta choice gives more weight to recall: beta=0.5 or beta=2?

---


## ML-FND-035 — What is ROC-AUC, and what does it not tell you?

**Difficulty:** Intermediate · **Type:** Metric · **Tags:** roc-auc, ranking

### Answer

ROC-AUC measures how well a score ranks positive examples above negative examples across possible thresholds, using the true-positive and false-positive rates. It is a threshold-independent ranking summary.

### Example

It can compare fraud scores across thresholds when no single operating threshold has yet been chosen.

### Common pitfall

ROC-AUC does not tell you whether predicted probabilities are calibrated, how many alerts operations can handle, or the precision at a specific threshold.

### Practice

Why should a high ROC-AUC model still be evaluated at the intended production threshold?

---


## ML-FND-036 — When is PR-AUC more informative than ROC-AUC?

**Difficulty:** Intermediate · **Type:** Metric · **Tags:** pr-auc, imbalance

### Answer

The precision-recall curve shows the precision-recall trade-off across thresholds. Its area is often more revealing than ROC-AUC when positive cases are rare and the quality of positive predictions is central.

### Example

For a rare fraud or defect-detection task, PR-AUC emphasizes how well the model finds positives without overwhelming the team with false alarms.

### Common pitfall

PR-AUC depends strongly on positive-class prevalence and implementation conventions. Compare models on comparable evaluation populations.

### Practice

What baseline precision would a random ranking roughly have when 2% of examples are positive?

---


## ML-FND-037 — How do MAE, MSE, and RMSE differ?

**Difficulty:** Beginner · **Type:** Metric · **Tags:** regression, mae, rmse

### Answer

MAE averages absolute errors and is easy to interpret in target units. MSE averages squared errors and penalizes large misses more heavily. RMSE is the square root of MSE, restoring the target's units while retaining stronger sensitivity to large errors.

### Example

For delivery-time predictions, MAE communicates typical absolute error in minutes; RMSE highlights models with occasional very large misses.

### Common pitfall

Metric choice encodes priorities. Outliers can strongly influence MSE and RMSE, while MAE is more robust to extreme errors.

### Practice

If large forecast misses are especially costly, which of MAE or RMSE would you examine and why?

---


## ML-FND-038 — What is cross-validation, and when should it be used?

**Difficulty:** Intermediate · **Type:** Validation design · **Tags:** cross-validation, model-selection

### Answer

Cross-validation repeats model fitting and evaluation across multiple training-validation folds to estimate variability and use limited data more efficiently. Hyperparameter selection must happen within the training process, not on the final test set.

### Example

Stratified k-fold can preserve class proportions for classification; grouped or time-aware schemes are needed when observations are dependent.

### Common pitfall

Standard random k-fold is not suitable for every dataset. Choose folds that reflect entities, time, and the intended deployment setting.

### Practice

Why might random k-fold be inappropriate for forecasting next month's demand?

---


## ML-FND-039 — What is a learning curve, and how can it diagnose model problems?

**Difficulty:** Intermediate · **Type:** Debugging · **Tags:** learning-curves, bias-variance

### Answer

A learning curve plots training and validation performance as training data size or training progress changes. The pattern can help distinguish high bias, high variance, insufficient data, or optimization issues.

### Example

A persistent gap between excellent training performance and weaker validation performance suggests overfitting; both curves performing poorly can suggest underfitting or poor features.

### Common pitfall

Learning curves are diagnostic evidence, not a single definitive rule. Ensure the metric direction and validation design are correct.

### Practice

What experiment would you try if training and validation performance are both poor and close together?

---


## ML-FND-040 — What is probability calibration?

**Difficulty:** Advanced · **Type:** Metric · **Tags:** calibration, probabilities

### Answer

A classifier is calibrated when predictions assigned probability p are positive about p proportion of the time over an appropriate population. Calibration matters when decisions use probability magnitude, not just ranking.

### Example

If customers assigned 0.8 churn risk churn only 0.4 of the time, the model may rank customers well but be poorly calibrated.

### Common pitfall

Calibration is population-dependent and can drift. Use a separate calibration procedure or cross-validated predictions without contaminating the final test set.

### Practice

Why might a well-ranked model still produce poor expected-cost decisions?

---


## ML-FND-041 — A model has 99% training accuracy and 72% validation accuracy. What would you investigate?

**Difficulty:** Intermediate · **Type:** Scenario · **Tags:** overfitting, debugging

### Answer

The gap suggests overfitting, leakage in the split design, or a validation population that differs from training. Check split correctness and duplicates first, then examine model complexity, feature leakage, sample size, and data quality.

### Example

Compare learning curves, simplify or regularize the model, improve leakage-safe validation, and consider more representative training examples. Evaluate changes on the validation process, not the final test set.

### Common pitfall

Do not jump straight to collecting more data before ruling out leakage or a flawed split.

### Practice

Write a prioritized three-step debugging plan and explain why each step comes first.

---


## ML-FND-042 — Fraud recall is high, but investigators are overwhelmed by false positives. What should you do?

**Difficulty:** Intermediate · **Type:** Scenario · **Tags:** fraud, threshold, precision

### Answer

Treat this as an operating-point and capacity problem. Inspect precision-recall behavior, costs of false positives and false negatives, alert volume at each threshold, and whether ranking can prioritize the limited investigation capacity.

### Example

Choose a threshold or top-k policy based on expected utility and team capacity; consider calibrated scores, a second-stage review model, or additional features if justified.

### Common pitfall

Do not optimize accuracy or arbitrarily raise the threshold without measuring missed-fraud cost and workload impact.

### Practice

Define two operational metrics and one safety constraint for a threshold experiment.

---


## ML-FND-043 — Your offline model score is strong, but production performance drops. What could explain it?

**Difficulty:** Advanced · **Type:** Incident response · **Tags:** distribution-shift, production

### Answer

Possible causes include training-serving skew, feature pipeline bugs, data or concept drift, changed user behavior, label delays, feedback loops, or an offline evaluation that did not mimic deployment.

### Example

Compare feature distributions and missingness, verify online/offline feature parity, inspect prediction and label pipelines, segment performance, and check changes around the incident time.

### Common pitfall

A lower online business outcome is not automatically model drift; investigate product changes, policy changes, and measurement changes too.

### Practice

Name three monitoring signals you would inspect before retraining.

---


## ML-FND-044 — A churn model uses a cancellation-reason field. Why might this be leakage?

**Difficulty:** Intermediate · **Type:** Scenario · **Tags:** churn, target-leakage

### Answer

If cancellation reason is recorded only after the customer cancels, it reveals the target or information from after the prediction point. The model may appear excellent offline but cannot use that field for an earlier intervention.

### Example

Define a prediction timestamp and feature availability contract. Remove post-outcome fields and rebuild evaluation using only information known at that timestamp.

### Common pitfall

A feature can be correlated with the target and still be invalid. Availability timing is as important as predictive power.

### Practice

How would you redesign the training table to predict churn 30 days before cancellation?

---


## ML-FND-045 — A dataset has only 0.5% positive cases. How would you evaluate a classifier?

**Difficulty:** Intermediate · **Type:** Scenario · **Tags:** rare-events, imbalance

### Answer

Start with a leakage-safe split and inspect PR-AUC, precision, recall, confusion matrices, calibration where relevant, and performance at realistic alert capacity. Use stratification when appropriate and ensure each evaluation partition has enough positives.

### Example

Compare against a simple baseline; choose a threshold using validation data and business costs. If resampling is used, apply it only inside training folds.

### Common pitfall

Do not oversample before splitting, because duplicates or synthetic neighbors can leak into validation and test data.

### Practice

Why is a 99.5% accuracy score nearly meaningless if the model predicts every example as negative?

---


## ML-FND-046 — A feature has a very high importance score. Does that mean it causes the outcome?

**Difficulty:** Intermediate · **Type:** Scenario · **Tags:** interpretability, causality

### Answer

No. Feature importance indicates a model's predictive reliance under a particular definition and dataset. Correlation, proxies, leakage, and confounding can all produce high importance without causality.

### Example

Check whether the feature is available at prediction time, compare importance methods, inspect subgroup behavior, and use a causal design if the question is about intervention effects.

### Common pitfall

Permutation importance and SHAP explain aspects of model behavior; neither alone proves a causal effect.

### Practice

What additional evidence would you need before claiming that changing a feature will change the outcome?

---


## ML-FND-047 — A model performs well overall but poorly for one customer segment. What next?

**Difficulty:** Advanced · **Type:** Scenario · **Tags:** fairness, subgroup-evaluation

### Answer

Treat aggregate metrics as incomplete. Validate sample sizes and label quality, compare error rates and calibration across relevant segments, investigate data coverage and feature quality, and assess whether the difference creates material harm.

### Example

Work with domain and policy stakeholders to define acceptable criteria, test mitigation options, and monitor subgroup performance after deployment.

### Common pitfall

Do not assume every metric must be identical across groups or apply a blind correction without understanding context and legal requirements.

### Practice

List two subgroup metrics and one data-quality check for a high-impact decision model.

---


## ML-FND-048 — Your validation score changes dramatically across random seeds. What does that tell you?

**Difficulty:** Intermediate · **Type:** Debugging · **Tags:** variance, reproducibility

### Answer

Large variation can indicate a small dataset, unstable splits, high model variance, rare classes, or an evaluation procedure with too few examples. Report uncertainty rather than presenting one favorable score.

### Example

Repeat evaluation with an appropriate cross-validation design, inspect fold-level scores and class counts, fix seeds for reproducibility, and gather more representative data if needed.

### Common pitfall

A fixed seed makes an experiment repeatable but does not eliminate statistical uncertainty or make a weak evaluation valid.

### Practice

How would you report performance if cross-validation scores vary widely?

---


## ML-FND-049 — How would you choose between a simple model and a more accurate complex model?

**Difficulty:** Advanced · **Type:** Decision making · **Tags:** tradeoffs, interpretability

### Answer

Compare validated performance against operational constraints: latency, cost, explainability, maintainability, robustness, privacy, and the cost of mistakes. Prefer the simplest model that satisfies the requirements unless measured benefits justify added complexity.

### Example

A logistic regression may be preferable when transparent coefficients and fast inference are crucial; boosted trees may be justified if they materially improve validated outcomes and can be governed.

### Common pitfall

A tiny offline metric gain may disappear under drift or fail to justify a larger operational burden.

### Practice

Define a decision rule with at least three criteria for model promotion.

---


## ML-FND-050 — Design a leakage-safe baseline for predicting next-month product demand.

**Difficulty:** Intermediate · **Type:** Capstone scenario · **Tags:** forecasting, baseline, time-series

### Answer

Define the forecast origin, target horizon, aggregation level, and available information. Create a chronological split, compare against a naive last-period or seasonal-naive forecast, and evaluate with a metric aligned to the business. Build features only from data available at the forecast origin.

### Example

For weekly demand, train on earlier weeks and validate on later weeks. A seasonal-naive baseline predicts the value from the comparable week in the prior seasonal cycle when enough history exists. Compare MAE or another justified metric and inspect performance by product and horizon.

### Common pitfall

Random row splitting and future-derived rolling statistics can leak future information. Check intermittent demand, stockouts, promotions, and changes in product availability.

### Practice

Deliverable: write the target definition, split rule, baseline formula, primary metric, and two monitoring signals before training a complex model.

---

