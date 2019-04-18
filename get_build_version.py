import os
import time


tag = os.environ.get('CIRCLE_TAG')
if tag:
    print(tag)
else:
    last_tag = os.popen('git describe --abbrev=0 --tags').read().strip()
    cur_epoch = int(time.time())
    print('{}.post{}'.format(last_tag, cur_epoch))
