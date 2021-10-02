###############################################################
####                                                       ####
#### Written By: Satyaki De                                ####
#### Written Date:  26-Jul-2021                            ####
#### Modified Date: 08-Sep-2021                            ####
####                                                       ####
#### Objective: This script will publish real-time         ####
#### streaming data coming out from a hosted API           ####
#### sources using another popular third-party service     ####
#### named Ably. Ably mimics pubsub Streaming concept,     ####
#### which might be extremely useful for any start-ups.    ####
####                                                       ####
###############################################################

from ably import AblyRest
import logging
import json

from random import seed
from random import random

import json
import math
import random

from clsConfig import clsConfig as cf

seed(1)

# Global Section

logger = logging.getLogger('ably')
logger.addHandler(logging.StreamHandler())

ably_id = str(cf.conf['ABLY_ID'])

ably = AblyRest(ably_id)
channel = ably.channels.get('sd_channel')

# End Of Global Section

class clsPublishStream:
    def __init__(self):
        self.msgSize = cf.conf['limRec']

    def pushEvents(self, srcJSON, debugInd, varVa):
        try:
            msgSize = self.msgSize

            # Capturing the inbound dataframe
            jdata_fin = json.dumps(srcJSON)

            print('IOT Events: ')
            print(str(jdata_fin))

            # Publish rest of the messages to the sd_channel channel
            channel.publish('event', jdata_fin)

            jdata_fin = ''

            return 0

        except Exception as e:

            x = str(e)
            print(x)

            logging.info(x)

            return 1
