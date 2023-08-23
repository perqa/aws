#!/usr/bin/env python

"""
This is the starter code to detecting the faces/labels
in our images of Kyle.

It's mostly complete but we didn't know all the specifics
to the API calls.

If you look at the boto3 documentation you will be able to find
all the answers!
"""

import boto3
import json
import os

######
# Getting our environment variables
# Make sure to set these in your lambda function
######
# this is the name of the rekognition collection you've created
rekognition_collection_id = os.environ['collection']
# output on the dashboard
sns_topic_arn = os.environ['sns_arn']
# this is your "Team ID" you see at the top of the player 
# dashboard like: 5a0e59338b894b57b48828b315a40afb
# **IT IS NOT YOUR TEAM NAME**
team_id = os.environ['team_id']


# Rekognition allows you to specify a "tag" with your image.
# so later when we detect a matching face, we read this tag
# so we know the name or title of the person we've matched
external_image_id = 'Kyle'

# our boto3 rekognition client
rekognition_client=boto3.client('rekognition')
sns_client=boto3.client('sns')

def facial_recognition(key, bucket):
    response = rekognition_client.index_faces(
        CollectionId=rekognition_collection_id,
        Image={
            ????????
        }
    )
    print "Index Faces response:\n %s" % response
    # see if Rekognition detected any faces in this image
    if not response['FaceRecords']:
        # no faces detected, so we send back a false
        return False

    # we found faces, so let's see if they match our CEO
    # iterating through the faces found in the submitted image
    for face in response['FaceRecords']:
        face_id = face['Face']['FaceId']
        print "Face ID: %s" % face_id
        # send the detected face to Rekognition to see if it matches
        # anything in our collection
        response = rekognition_client.search_faces(
            ???????
        )
        print "Searching faces response:\n %s" % response
        # checking if there were any matches
        if not response['FaceMatches']:
            # not our CEO
            return False

        # we recognized a face, let's see if it matches our CEO
        for match in response['FaceMatches']:
            if "ExternalImageId" in match['Face'] and match['Face']["ExternalImageId"] == external_image_id:
                # we have a picture of our CEO
                print "We've found our CEO!! Huzzah!"
                return True

        # At this point, we have other faces in our collection that 
        # match this face, but it didn't match our CEO
        print "not kyle :("
        return False

def get_labels(key, bucket):
    response = rekognition_client.detect_labels(
        Image={
            ????????
        },
        MinConfidence=50
    )
    raw_labels = response['Labels']
    top_five=[]
    for x in range(0,5):
        top_five.append(raw_labels[x]['Name'])

    return top_five

def send_sns(message):
    """
    We'll use SNS to send our response back to the master account
    with our labels
    """
    print message
    response = sns_client.publish(
        ??????
    )

    return

def lambda_handler(event, context):
    """
    Main Lambda handler
    """
    print json.dumps(event)
    # our incoming event is the S3 put event notification
    s3_message = event
    # get the object key and bucket name
    key = s3_message['Records'][0]['s3']['object']['key']
    bucket = s3_message['Records'][0]['s3']['bucket']['name']

    # first we need to see if our CEO is in this picture
    proceed = facial_recognition(key, bucket)

    return_message={
        "key":key,
        "team_id":team_id
    }

    # now we move on to detecting what's in the image
    if proceed:
        labels = get_labels(key, bucket)
        return_message['labels']=labels
        return_message['kyle_present']=True
    else:
        # we need to signal back that our CEO wasn't in the picture
        return_message['kyle_present']=False
    
    send_sns(return_message)
