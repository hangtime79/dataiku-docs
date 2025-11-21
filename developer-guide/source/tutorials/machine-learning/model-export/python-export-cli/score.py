import click
import pandas as pd
from dataikuscoring import load_model

@click.command()
@click.option("-i", 
              "--input-file", 
              type=click.Path(exists=True),
              help="Path to the input file")
@click.option("-o",
              "--output-file",
              type=click.File(mode='w'),
              help="Path to the generated output file")
@click.option("-m", 
              "--model-file", 
              type=click.Path(exists=True),
              help="Path to the model to use for predictions")
@click.option("--proba",
              is_flag=True,
              help="Output predicted probability columns for each class")
def score(input_file, output_file, model_file, proba):
    """
    Scoring CLI: computes predictions from CSV file records using
    a trained model exported from Dataiku.
    """

    # Load model:
    model = load_model(model_file)

    # Load input file data in a pandas DataFrame
    df = pd.read_csv(input_file, sep=None, engine='python')
    if proba:
        # Compute probabilities for each class
        predictions = model.predict_proba(df)
        for label in predictions.keys():
            proba_col = f"proba_{label}"
            df[proba_col] = predictions[label]
    else:
        # Compute predictions
        df["predictions"] = model.predict(df)

    # Write result to output file
    df.to_csv(output_file)

if __name__ == "__main__":
    score()
