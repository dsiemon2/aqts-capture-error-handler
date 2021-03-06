"""
Module containing functions for persisting inputs that cause failures in for a particular state.

"""
import boto3

from .utils import select_delay_seconds


def send_message(queue_url, message_body, region='us-west-2'):
    """
    Send a message to an SQS standard queue. Messages are sent
    with a randomized delay for message delivery. The delay improves
    survivability by spreading out large data surges from the retriever,
    thereby reducing load on the database per unit time.

    :param str queue_url: http url of the SQS queue
    :param str message_body: the message body
    :param str region: AWS region
    :return: message send response
    :rtype: dict

    """
    sqs = boto3.client('sqs', region_name=region)

    resp = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body,
        DelaySeconds=select_delay_seconds()
    )
    return resp
