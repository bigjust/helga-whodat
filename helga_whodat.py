import boto3
import requests

from tempfile import TemporaryFile

from helga import settings
from helga.plugins import command

AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID', False)
AWS_SECRET_ACCESS_KEY = getattr(settings, 'AWS_SECRET_ACCESS_KEY', False)

@command('whodat', help='who dat?')
def whodat(client, channel, nick, message, cmd, args):
    """
    takes an image url, downloads it, uploads that to AWS rekognition.

    Upon receiving data back, will output celebrities, or other data.
    """

    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        return 'Must set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`'

    image_url = args[0]

    # create temporary file

    tmp_file = TemporaryFile()

    # retrieve url and save to tmp_file

    r = requests.get(image_url, stream=True)

    for chunk in r.iter_content(chunk_size=128):
        tmp_file.write(chunk)

    tmp_file.seek(0)

    # send image to rekognition

    boto_client = boto3.client(
        'rekognition',
        region_name='us-east-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    response = boto_client.recognize_celebrities(
        Image={
            'Bytes': tmp_file.read(),
        }
    )

    # iterate through results, just return somewhat certain celebs for now

    celebs = []
    for celeb in response['CelebrityFaces']:
        if celeb['MatchConfidence'] > 75:
            celebs.append(celeb['Name'])

    for celeb_name in celebs:
        client.msg(channel, celeb_name)

    if not celebs and response['CelebrityFaces']:
        top_result = response['CelebrityFaces'][0]

        return 'hmmm, {}? ({:.0%})'.format(
            top_result['Name'],
            top_result['MatchConfidence'] / 100,
        )

    if not celebs:
        return 'Don\'t rekognize anyone :('
