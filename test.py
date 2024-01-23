#!/usr/local/bin/python3
import boto3
import click
from botocore.exceptions import ClientError
import re

regions = ['ap-south-1']

ec2 = None

@click.group()
def cli():
    '''
    Helper commands for Snapshots and Volumes management.
    '''
    pass

@cli.command()
def snapshot_delete():
    '''
    Delete specific snapshots by ID if they are unused.
    '''
    global ec2
    snapshots_to_delete =  ['snap-08caa4e76834b2084']
    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        print('Processing snapshots in region:', region)
        for snapshot_id in snapshots_to_delete:
            try:
                print('Processing snapshot:', snapshot_id)
                snapshot = get_snapshot(snapshot_id)
                volume_id = snapshot['volume_id']
                
                # Check if the volume associated with the snapshot exists
                if not volume_exists(volume_id):
                    print('Volume does not exist for snapshot:', snapshot_id)
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print('Deleted snapshot:', snapshot_id)
                elif not is_snapshot_in_use(snapshot_id) and not is_volume_attached(volume_id):
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print('Deleted snapshot:', snapshot_id)
                    if not is_volume_attached(volume_id):
                        ec2.delete_volume(VolumeId=volume_id)
                        print('Deleted volume:', volume_id)
                else:
                    print('Skipping snapshot:', snapshot_id, 'as it is in use or its volume is attached.')
            except ClientError as e:
                print('Failed to delete snapshot:', snapshot_id)
                print('Error:', e)


def is_snapshot_in_use(snapshot_id):
    # Check if the snapshot is associated with any volumes
    response = ec2.describe_volumes(Filters=[{'Name': 'snapshot-id', 'Values': [snapshot_id]}])
    volumes = response['Volumes']
    return bool(volumes)

def is_volume_attached(volume_id):
    # Check if the volume is attached to an EC2 instance
    response = ec2.describe_volumes(VolumeIds=[volume_id])
    volume = response['Volumes'][0] if response['Volumes'] else None
    if volume and volume.get('Attachments'):
        # Volume is attached to an instance
        return True
    return False

def volume_exists(volume_id):
    if not volume_id:
        return False
    try:
        ec2.describe_volumes(VolumeIds=[volume_id])
        return True
    except ClientError:
        return False

def get_snapshot(snapshot_id):
    '''
    Get a single snapshot by ID.
    '''
    snapshot = ec2.describe_snapshots(SnapshotIds=[snapshot_id])['Snapshots'][0]
    instance_id, image_id = parse_description(snapshot['Description'])
    return {
        'id': snapshot['SnapshotId'],
        'description': snapshot['Description'],
        'start_time': snapshot['StartTime'],
        'size': snapshot['VolumeSize'],
        'volume_id': snapshot['VolumeId'],
        'instance_id': instance_id,
    }

def parse_description(description):
    regex = r"^Created by CreateImage\((.?)\) for (.?) "
    matches = re.finditer(regex, description, re.MULTILINE)
    for matchNum, match in enumerate(matches):
        return match.groups()
    return '', ''

if _name_ == '_main_':
    cli()
