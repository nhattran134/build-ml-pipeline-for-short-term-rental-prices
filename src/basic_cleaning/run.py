#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    logger.info("download artifact: %s", args.input_artifact)
    df = pd.read_csv(artifact_local_path)
    
    # Drop outliers
    logger.info("Removing outliers, with price threshold [min-max]: %i - %i", args.min_price, args.max_price)
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    #Convert last review to datetome
    df['last_review'] = pd.to_datetime(df['last_review'])
    
    # Save the results to a CSV file
    logger.info("Save preprocessed data to CSV")
    df.to_csv(args.output_artifact, index=False)

    # Build artifact
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )

    logger.info("Log artifact: clean_sample.csv")
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Name for input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name for output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="CSV",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Clean data",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum price willing to pay",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum proce willing to pay",
        required=True
    )



    args = parser.parse_args()

    go(args)
