import argparse
import json
import sys

from sqlmodel import Session

from utu.db.eval_datapoint import DatasetSample
from utu.utils.sqlmodel_utils import SQLModelUtils


def upload_dataset(file_path: str, dataset_name: str):
    """
    Connects to the database and uploads datapoints from a local JSONL file.
    """
    engine = SQLModelUtils.get_engine()

    print("Connecting to the database...")
    with Session(engine) as session:
        print(f"Uploading datapoints from {file_path} to dataset '{dataset_name}'...")

        with open(file_path, encoding="utf-8") as f:
            for i, line in enumerate(f):
                try:
                    data: dict = json.loads(line.strip())

                    # Ensure the dataset name from the argument is used
                    data["dataset"] = dataset_name
                    if "id" in data:
                        data.pop("id")

                    # Create a DatasetSample object from the dictionary
                    dataset_sample = DatasetSample(**data)

                    session.add(dataset_sample)

                except json.JSONDecodeError:
                    print(f"Warning: Skipping invalid JSON on line {i + 1}", file=sys.stderr)
                    continue
                except Exception as e:  # pylint: disable=broad-except
                    print(f"Error processing line {i + 1}: {e}", file=sys.stderr)
                    session.rollback()
                    sys.exit(1)

            print("Committing changes to the database...")
            session.commit()

    print("Upload complete.")


def main():
    parser = argparse.ArgumentParser(description="Upload a dataset from a JSONL file to the database.")
    parser.add_argument("--file_path", type=str, help="The path to the input JSONL file.")
    parser.add_argument("--dataset_name", type=str, help="The name to assign to the dataset in the database.")

    args = parser.parse_args()

    upload_dataset(args.file_path, args.dataset_name)


if __name__ == "__main__":
    main()
