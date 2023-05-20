import configparser
import os.path

import boto3.exceptions


def get_aws_credentials(config_path="/.aws/credentials", verbose=True):
    try:
        print(f"Reading AWS credentials from {config_path}") if verbose else None
        if not os.path.exists(config_path):
            print(f"{config_path} doesn\'t exist") if verbose else None
            return None, None
        print(f"{config_path} exists") if verbose else None
        config = configparser.ConfigParser()
        config.read(config_path)
        var_a = config.get("default", "aws_access_key_id")
        var_b = config.get("default", "aws_secret_access_key")
        print(f"Found AWS credentials: {var_a}, {var_b}") if verbose else None
        return var_a, var_b
    except Exception as e:
        print(f"DEBUG [{__file__}]: {e}") if verbose else None


def parse_aws_credentials(config_path="/.aws/credentials", verbose=False):
    try:
        print("Checking python file with aws keys...")
        from db_utils.aws_keys import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
        aws_secrets = (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    # else:  # for docker we should get variables from os environment
    except ModuleNotFoundError:
        print("The file with aws keys is missing. Checking environment variables...")
        if os.environ.get('LAMBDA_TASK_ROOT'):
            aws_secrets = os.environ.get("AWS_ACCESS_KEY_ID_"), os.environ.get("AWS_SECRET_ACCESS_KEY_")
        else:
            aws_secrets = os.environ.get("AWS_ACCESS_KEY_ID"), os.environ.get("AWS_SECRET_ACCESS_KEY")

        if None in aws_secrets:
            print("AWS credentials are not set in the environment. Looking for the local file with aws credentials...")
            aws_secrets = get_aws_credentials(config_path=config_path, verbose=verbose)

        if None in aws_secrets:
            raise boto3.exceptions.Boto3Error("Credentials are not found")

    return aws_secrets


if __name__ == "__main__":
    print(get_aws_credentials("C:/Users/mary-/.aws/credentials"))
    print(parse_aws_credentials(config_path="C:/Users/mary-/.aws/credentials", verbose=True))