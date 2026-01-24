# src/app.py

import argparse
import pandas as pd
import os

from train_model import train_model_and_version
from evaluate_model import evaluate_model
from validate import evaluate_and_save
from compare import compare
from model_registry import EXPERIMENTS_CSV


def list_models():
    if not os.path.exists(EXPERIMENTS_CSV):
        print("No experiment registry found yet.")
        return

    df = pd.read_csv(EXPERIMENTS_CSV)
    print("\nSaved model versions and metrics:\n")
    print(df)


def main():
    parser = argparse.ArgumentParser(
        description="AegisAI IDS Command Line Interface"
    )

    parser.add_argument(
        "action",
        choices=["train", "evaluate", "validate", "compare", "list_models"],
        help="Action to perform"
    )

    parser.add_argument(
        "--notes",
        "-n",
        type=str,
        default="",
        help="Optional note for training"
    )

    args = parser.parse_args()

    if args.action == "train":
        print("Training model...")
        train_model_and_version(notes=args.notes)

    elif args.action == "evaluate":
        print("Evaluating model...")
        evaluate_model()

    elif args.action == "validate":
        print("Validating model (confusion matrix)...")
        evaluate_and_save()

    elif args.action == "compare":
        print("Comparing ML vs Rule-based IDS...")
        compare()

    elif args.action == "list_models":
        list_models()


if __name__ == "__main__":
    main()
