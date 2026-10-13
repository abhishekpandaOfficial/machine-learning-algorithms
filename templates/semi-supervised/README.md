# Semi-Supervised Project Template

Document both the labelled and unlabelled populations and the risks of using inferred labels.

## Required sections

1. Label availability and sampling process
2. Dataset source, terms and feature timing
3. Baseline trained only on trusted labels
4. Algorithm intuition and confidence threshold
5. Pseudo-label or propagation audit
6. Validation using untouched trusted labels
7. Confirmation-bias and subgroup analysis
8. Save/reload artifact smoke test
9. Streamlit serving contract and limitations
10. HTML/PDF export and final checklist

## Definition of done

- [ ] Inferred labels are distinguishable from trusted labels.
- [ ] Confidence thresholds and rejection rules are documented.
- [ ] Evaluation uses trusted labels not used for pseudo-labelling.
- [ ] Outputs are reproducible and print-ready.
