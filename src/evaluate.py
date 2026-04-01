# src/evaluate.py — Evaluation metrics for Sarathi AI
import numpy as np
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer


def bleu_score(prediction: str, reference: str) -> float:
    """Compute sentence BLEU score."""
    smoother = SmoothingFunction().method1
    return sentence_bleu(
        [reference.split()],
        prediction.split(),
        smoothing_function=smoother
    )


def rouge_scores(prediction: str, reference: str) -> dict:
    """Compute ROUGE-1, ROUGE-2, ROUGE-L scores."""
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    return scorer.score(reference, prediction)


def evaluate_dataset(pipeline_fn, test_pairs: list[tuple]) -> dict:
    """
    Evaluate Sarathi AI on a list of (question, expected_answer) pairs.
    Returns average BLEU and ROUGE scores.
    """
    bleu_scores, rouge1_scores = [], []

    for question, expected in test_pairs:
        prediction = pipeline_fn(question)
        bleu = bleu_score(prediction, expected)
        rouge = rouge_scores(prediction, expected)
        bleu_scores.append(bleu)
        rouge1_scores.append(rouge["rouge1"].fmeasure)
        print(f"Q: {question[:50]}...")
        print(f"BLEU: {bleu:.4f} | ROUGE-1: {rouge['rouge1'].fmeasure:.4f}")

    return {
        "avg_bleu": np.mean(bleu_scores),
        "avg_rouge1": np.mean(rouge1_scores),
    }


# Sample Indian test set
SAMPLE_TEST_PAIRS = [
    ("What is IPC Section 302?", "Section 302 of the IPC prescribes punishment for murder, with imprisonment for life or death penalty."),
    ("What does the Bhagavad Gita say about karma?", "The Gita teaches that one should perform their duty without attachment to the fruits of action."),
    ("Best budget hotel in Kolkata?", "Some popular budget hotels in Kolkata include Hotel Hindusthan International and Broadway Hotel."),
    ("What is Article 21 of the Indian Constitution?", "Article 21 guarantees the right to life and personal liberty to all persons."),
]
