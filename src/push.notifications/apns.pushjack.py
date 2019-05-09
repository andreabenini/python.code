# -*- coding: UTF8 -*-
#
# @author Andrea Benini [at gmail]
#
# "pip install pushjack" to install this library for Apple Push Notifications
# Credit https://github.com/dgilland/pushjack
#
# This one uses "old" SSL method on TCP Port 2195
# - gateway.push.apple.com          - production stage
# - gateway.sandbox.push.apple.com  - devel stage
#
# Excellent tool for command line tests
#
import logging
from pushjack import APNSClient
from pushjack import APNSSandboxClient

logger = logging.getLogger('pushjack')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Comment/uncomment what you need
client = APNSClient(certificate='aps_production.pem',
#client = APNSSandboxClient(certificate='aps_test.pem',
                    default_error_timeout=10,
                    default_expiration_offset=2592000,
                    default_batch_size=100,
                    default_retries=5)

token = '<YOUR CLIENT TOKEN MUST BE INSERTED HERE>'
alert = 'Hello world'

# Send to single device.
# NOTE: Keyword arguments are optional.
res = client.send(token,
                  alert,
#                  badge='1',
#                  sound='sound to play',
#                  category='category',
#                  content_available=True,
                  title='Title',
#                  title_loc_key='t_loc_key',
#                  title_loc_args='t_loc_args',
#                  action_loc_key='a_loc_key',
#                  loc_key='loc_key',
#                  launch_image='path/to/image.jpg',
                  extra={'custom': 'data'}
)

# Send to multiple devices by passing a list of tokens.
#client.send([token], alert, **options)
