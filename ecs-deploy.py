#!/bin/python

import os
import boto3

def pp(name):
    # pp as in plugin parameter 
    param = os.environ.get('{}_{}'.format('PLUGIN', name.upper()))
    if param:
        return param
    else:
        print 'No such variable {}'.format(name)
        return None


def port_handler(paramString):
    omap = []
    portSets = paramString.split(',')
    for set in portSets:
        omap.append(
            {
                'containerPort': int(set.split(' ')[1]),
                'hostPort': int(set.split(' ')[0])
            }
        )

    return omap


def env_handler(paramString):
    omap = []
    envSets = paramString.split(',')
    for set in envSets:
        value = os.environ.get(set.split('=')[0]) if not set.split('=')[1] and os.environ.get(set.split('=')[0]) else set.split('=')[1]
            
        omap.append(
            {
                'name': set.split('=')[0],
                'value': value
            }
        )

    return omap  


def options_handler(paramString):
    opts = {}
    optSets = paramString.split(',')
    for set in optSets:
        opts[set.split('=')[0]] = set.split('=')[1]

    return opts 


def register_task_definition():
    try:
        taskResponse = client.register_task_definition(
            family = pp('family'),
            containerDefinitions = [
                {
                    'name': '{}-container'.format((pp('family'))),
                    'image': '{}:{}'.format(pp('image_name'), pp('image_tag')),
                    'memory': int(pp('memory')),
                    'portMappings': port_handler(pp('port_mappings')),
                    'environment': env_handler(pp('environment_variables')),
                    'logConfiguration': {
                        'logDriver': pp('log_driver'),
                        'options': options_handler(pp('log_options'))
                    },
                }
            ]
        )
        print 'Completing new task registration...'
        print taskResponse
        print 'Revision: {}'.format(taskResponse['taskDefinition']['revision'])
        return taskResponse['taskDefinition']['taskDefinitionArn']
    except Exception as e:
        print 'Error registring TaskDefinition: {}'.format(e)
        exit(1)


def register_task_definition_dockersock():
    try:
        taskResponse = client.register_task_definition(
            family = pp('family'),
            containerDefinitions = [
                {
                    'name': '{}-container'.format((pp('family'))),
                    'image': '{}:{}'.format(pp('image_name'), pp('image_tag')),
                    'memory': int(pp('memory')),
                    'portMappings': port_handler(pp('port_mappings')),
                    'environment': env_handler(pp('environment_variables')),
                    'logConfiguration': {
                        'logDriver': pp('log_driver'),
                        'options': options_handler(pp('log_options'))
                    },
                    'mountPoints': [
                        {
                            'sourceVolume': 'dockersock',
                            'containerPath': '/var/run/docker.sock'
                        },
                    ],
                }
            ],
            volumes = [
                {
                    'name': 'dockersock',
                    'host': {
                        'sourcePath': '/var/run/docker.sock'
                    }
                },
            ],
        )
        print 'Completing new task registration...'
        print taskResponse
        print 'Revision: {}'.format(taskResponse['taskDefinition']['revision'])
        return taskResponse['taskDefinition']['taskDefinitionArn']
    except Exception as e:
        print 'Error registring TaskDefinition: {}'.format(e)
        exit(1)

def register_task_definition_mount():
    try:
        taskResponse = client.register_task_definition(
            family = pp('family'),
            containerDefinitions = [
                {
                    'name': '{}-container'.format((pp('family'))),
                    'image': '{}:{}'.format(pp('image_name'), pp('image_tag')),
                    'memory': int(pp('memory')),
                    'portMappings': port_handler(pp('port_mappings')),
                    'environment': env_handler(pp('environment_variables')),
                    'logConfiguration': {
                        'logDriver': pp('log_driver'),
                        'options': options_handler(pp('log_options'))
                    },
                    'mountPoints': [
                        {
                            'sourceVolume': pp('source_volume'),
                            'containerPath': pp('container_path')
                        },
                    ],
                }
            ],
            volumes = [
                {
                    'name': pp('source_volume'),
                    'host': {
                        'sourcePath': pp('source_path')
                    }
                },
            ],
        )
        print 'Completing new task registration...'
        print taskResponse
        print 'Revision: {}'.format(taskResponse['taskDefinition']['revision'])
        return taskResponse['taskDefinition']['taskDefinitionArn']
    except Exception as e:
        print 'Error registring TaskDefinition: {}'.format(e)
        exit(1)


def update_service(taskArn):
    try:
        updateResponse = client.update_service(
            cluster = pp('cluster'),
            service = pp('service'),
            taskDefinition = taskArn
        )
        print 'Completing service update to cluster'
        print updateResponse

    except Exception as e:
        print 'Error updating service: {}'.format(e)
        exit(1)


ACCESS_KEY = pp('access_key')
SECRET_KEY = pp('secret_key')
AWS_REGION = pp('region')


if __name__ == "__main__":
    global client 
    client = boto3.client(
        'ecs',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=AWS_REGION
    )
    
    if pp('source_volume') and pp('container_path') and pp('source_path'):
        update_service(register_task_definition_mount()) 
    else:
        update_service(register_task_definition()) if not pp('mount_dockersock') else update_service(register_task_definition_dockersock())
 
