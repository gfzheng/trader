# coding=utf-8
#
# Copyright 2016 timercrack
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import sys
import os
import django
if sys.platform == 'darwin':
    sys.path.append('/Users/jeffchen/Documents/gitdir/dashboard')
else:
    sys.path.append('/home/cyh/bigbrother/dashboard')
os.environ["DJANGO_SETTINGS_MODULE"] = "dashboard.settings"
django.setup()
import asyncio
from trader.strategy.brother2 import TradeStrategy
from trader.utils.read_config import *
import trader.utils.logger as my_logger

logger = my_logger.get_logger('main')


def main():
    loop = asyncio.get_event_loop()
    big_brother = None
    try:
        pid_path = os.path.join(app_dir.user_cache_dir, 'trader.pid')
        if not os.path.exists(pid_path):
            if not os.path.exists(app_dir.user_cache_dir):
                os.makedirs(app_dir.user_cache_dir)
        with open(pid_path, 'w') as pid_file:
            pid_file.write(str(os.getpid()))
        big_brother = TradeStrategy(io_loop=loop)
        print('Big Brother is watching you!')
        print('used config file:', config_file)
        print('log stored in:', app_dir.user_log_dir)
        print('pid file:', pid_path)
        loop.create_task(big_brother.install())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    except Exception as ee:
        logger.info('发生错误: %s', repr(ee), exc_info=True)
    finally:
        big_brother and loop.run_until_complete(big_brother.uninstall())
        logger.info('程序已退出')


if __name__ == '__main__':
    main()
