"""
Module for working with the AWS Step Functions API

"""
import ast

import boto3

from .utils import search_dictionary_list


def get_execution_history(execution_arn, region='us-west-2'):
    sfn = boto3.client('stepfunctions', region_name=region)
    history = sfn.get_execution_history(executionArn=execution_arn)
    return history


def find_root_failure_state(execution_history):
    execution_events = execution_history['events']
    state = search_dictionary_list(execution_events, 'type', 'LambdaFunctionFailed')
    while state['type'] != 'TaskStateEntered':
        state_previous_event_id = state['previousEventId']
        search_result = search_dictionary_list(execution_events, 'id', state_previous_event_id)[0]
        state = search_result
    state_event_details = state['stateEnteredEventDetails']
    return {
        'state': state_event_details['name'],
        'input': ast.literal_eval(state_event_details['input'])
    }
