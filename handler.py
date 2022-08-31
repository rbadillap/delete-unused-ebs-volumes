import datetime
import logging
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# boto instances
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

def run(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Your cron function " + name + " ran at " + str(current_time))

    # get full list of volumes currently in state available
    volumes = ec2.volumes.filter(
        Filters = [{
            'Name': 'status',
            'Values': ['available']
        }]
    )

    # print a debug information about the amount of instances to be deleted
    volume_ids = [v.id for v in volumes]

    if len(volume_ids) >= 1:
        logger.info(str(len(volume_ids)) + " volumes were found that can be deleted")
    else:
        logger.info("No volumes to be deleted were found")

    # iterate the object to start deleting the volumes
    # since boto3's collections are iterable we don't need to validate the amount of items returned to start this loop
    for volume in volumes:
        response = client.delete_volume(
            VolumeId = volume.id
        )
        code = response['ResponseMetadata']['HTTPStatusCode']
        if code == 200:
            logger.info("The volume: " + volume.id + " was successfully deleted")

