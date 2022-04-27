import requests
import json
import logging
import os
import time
import random
import boto3
import pandas as pd
import hashlib
import numpy


class GlobalArgs:
    OWNER = "ramon.marrero"
    ENVIRONMENT = "Development"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def set_logging(lv=GlobalArgs.LOG_LEVEL):
    """ Helper to enable logging """
    logging.basicConfig(level=lv)
    logger = logging.getLogger()
    logger.setLevel(lv)
    return logger


LOG = set_logging()
client = boto3.client('s3')


def handler(event, context):
    resp = {"status": False}
    LOG.info(boto3.__version__)
    LOG.info(json.dumps(event))

    object_get_context = event["getObjectContext"]
    request_route = object_get_context["outputRoute"]
    request_token = object_get_context["outputToken"]
    s3_url = object_get_context["inputS3Url"]

    # Get object from S3
    response = requests.get(s3_url)
    original_object = json.loads(response.content.decode("utf-8"))
    LOG.info(json.dumps(original_object))

    df = pd.json_normalize(original_object)

    #Hash customer id
    df['customer_id_hashed'] = df['cust_id'].astype(str)

    df['customer_id_hashed'] = df['customer_id_hashed'].apply(
    lambda x: 
        hashlib.sha256(x.encode()).hexdigest()
    )

    df.drop('cust_id', axis=1, inplace=True)

    hashed_object = df.to_json(orient = 'records')

    LOG.info(json.dumps(hashed_object))

    transformed_object = json.dumps(hashed_object)


    # Write object back to S3 Object Lambda
    _r = client.write_get_object_response(
        Body=json.loads(transformed_object),
        RequestRoute=request_route,
        RequestToken=request_token
    )
    LOG.info(f'{{"resp":{json.dumps(_r)}}}')

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": resp
        })
    }