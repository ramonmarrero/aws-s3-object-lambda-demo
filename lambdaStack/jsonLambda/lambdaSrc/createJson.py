import json
import logging
import datetime
import os
import random
import uuid

import boto3


class LambdaArgs:
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    S3_BKT_NAME = "aws-s3-object-lambda-json"
    S3_PREFIX = "events"
    EVNT_WEIGHTS = {"success": 80, "fail": 20}


def set_logging(lv=LambdaArgs.LOG_LEVEL):
    logging.basicConfig(level=lv)
    logger = logging.getLogger()
    logger.setLevel(lv)
    return logger


logger = set_logging()


def _rand_coin_flip():
    if random.randint(1, 100) < LambdaArgs.EVNT_WEIGHTS["fail"]:
        return True


def _gen_uuid():
    return str(uuid.uuid4())


def put_object(_pre, data):
    try:
        _r = _s3.put_object(
            Bucket=LambdaArgs.S3_BKT_NAME,
            Key=f"{LambdaArgs.S3_PREFIX}/{_pre}/dt={datetime.datetime.now().strftime('%Y_%m_%d')}/{datetime.datetime.now().strftime('%s%f')}.json",
            Body=json.dumps(data).encode("UTF-8"),
        )
        logger.debug(f"resp: {json.dumps(_r)}")
    except Exception as e:
        logger.info(f"ERROR: For PREFIX:{_pre}")
        # logger.exception(f"ERROR:{str(e)}")


_s3 = boto3.client("s3")


def handler(event, context):
    resp = {"status": False}
    logger.debug(f"Event: {json.dumps(event)}")

    _categories = ["Books", "Games", "Mobiles", "Groceries", "Shoes", "Stationaries", "Laptops",
                   "Tablets", "Notebooks", "Camera", "Printers", "Monitors", "Speakers", "Projectors", "Cables", "Furniture"]

    _evnt_types = ["sales_event", "inventory_event"]

    _variants = ["black", "red"]

    try:
        t_msgs = 0
        p_cnt = 0
        s_evnts = 0
        inventory_evnts = 0
        t_sales = 0
        while context.get_remaining_time_in_millis() > 100:
            _s = round(random.random() * 100, 2)
            _evnt_type = random.choice(_evnt_types)
            _u = _gen_uuid()
            p_s = bool(random.getrandbits(1))
            evnt_body = {
                "request_id": _u,
                "cust_id": random.randint(100, 999),
                "category": random.choice(_categories),
                "store_id": random.randint(1, 10),
                "evnt_time": datetime.datetime.now().isoformat(),
                "evnt_type": _evnt_type,
                "price": _s,
                "discount": round(random.random() * 20, 1),
                "sku": random.randint(18981, 189281),
                "item_variant": random.choice(_variants),
                "gift_wrap": bool(random.getrandbits(1)),
                "qty": random.randint(1, 38),
                "priority_shipping": p_s
            }
            evnt_attr = {
                "evnt_type": {
                    "DataType": "String",
                    "StringValue": _evnt_type
                },
                "priority_shipping": {
                    "DataType": "String",
                    "StringValue": f"{p_s}"
                }
            }

            # Make the order type as return
            if bool(random.getrandbits(1)):
                evnt_body["is_return"] = True

            if _rand_coin_flip():
                evnt_body.pop("store_id", None)
                evnt_body["bad_msg"] = True
                p_cnt += 1

            if _evnt_type == "sales_event":
                s_evnts += 1
            elif _evnt_type == "inventory_event":
                inventory_evnts += 1

            put_object(
                _evnt_type,
                evnt_body
            )
            t_msgs += 1
            t_sales += _s

        resp["tot_msgs"] = t_msgs
        resp["bad_msgs"] = p_cnt
        resp["sales_evnts"] = s_evnts
        resp["inventory_evnts"] = inventory_evnts
        resp["tot_sales"] = t_sales
        resp["status"] = True
        logger.info(f'{{"resp":{json.dumps(resp)}}}')

    except Exception as e:
        logger.error(f"ERROR:{str(e)}")
        resp["err_msg"] = str(e)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": resp
        })
    }