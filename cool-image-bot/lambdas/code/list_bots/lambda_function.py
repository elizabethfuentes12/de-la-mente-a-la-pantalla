import json
import os
import boto3 
from botocore.exceptions import ClientError

client = boto3.client('lexv2-models')

def lambda_handler(event, context):

    # list current bots using boto3
    bots = list_detailed_bots()

    response = build_response(200, json.dumps({"bots":bots}))
    return response




def get_bots_summaries():
    print(f"get bot summary")

    response = client.list_bots()
    bots = []
    if response.get('botSummaries'):
        for bot in response['botSummaries']:
            if bot['botStatus'] == 'Available':
                bots.append({'botName': bot['botName'], 'botId': bot['botId'] })

    return bots

def get_bot_versions(bot_id):
    print(f"get bot version:{bot_id}")
    response = client.list_bot_versions(botId=bot_id, )
    versions = []
    if response.get('botVersionSummaries'):
        for ver in response['botVersionSummaries']:
            versions.append({'botVersion': ver['botVersion'] })
    return versions

def get_bot_aliases(bot_id):
    print(f"get bot aliases:{bot_id}")

    response = client.list_bot_aliases(botId=bot_id, )
    aliases = []
    if response.get('botAliasSummaries'):
        for alias in response['botAliasSummaries']:
            if alias['botAliasStatus'] == 'Available':
                aliases.append({
                    'botAliasId': alias['botAliasId'], 
                    'botAliasName': alias['botAliasName'], 
                    'botVersion': alias['botVersion']})
    return aliases


def get_bot_locales(bot_id, bot_version):
    print(f"get bot locales:{bot_id}, {bot_version}")

    response = client.list_bot_locales(botId=bot_id, botVersion= bot_version)
    locales = []
    if response.get('botLocaleSummaries'):
        for loc in response['botLocaleSummaries']:
            locales.append({
                'localeId': loc['localeId'] , 
                'localeName': loc['localeName'] , 
                'botLocaleStatus': loc['botLocaleStatus'] })
    return locales


def list_detailed_bots():
    detailed_bot_list = []
    bots = get_bots_summaries()
    for bot in bots:
        bot_id = bot['botId']
        aliases = get_bot_aliases(bot_id)

        for alias in aliases:
            botver = alias['botVersion']
            locales = get_bot_locales(bot_id, botver)

            for locale in locales:
                detailed_bot_list.append(dict(**bot, **alias, **locale))


    return detailed_bot_list
    


def build_response(status_code, json_content):
        
        return {
        'statusCode': status_code,
        "headers": {
            "Content-Type": "text/html;charset=UTF-8",
            "charset": "UTF-8",
            "Access-Control-Allow-Origin": "*"
        },
        'body': json_content
    }

