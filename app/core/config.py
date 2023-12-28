import platform
import os
import getpass
from app.core.log import get_logger
import configparser
from enum import Enum

logger = get_logger(__name__)

def get_aws_credentials(profile: str):
    """
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY를 가져오는 함수

    :return:
    """

    PROFILE = profile

    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID'] if 'AWS_ACCESS_KEY_ID' in os.environ else None
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY'] if 'AWS_SECRET_ACCESS_KEY' in os.environ else None

    if AWS_SECRET_ACCESS_KEY is not None and AWS_ACCESS_KEY_ID is not None:
        return AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    else:
        logger.info('AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY Not Found in Environment Variables')
        if platform.system() == 'Windows':
            logger.info(f'GET AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from C:\\Users\\{getpass.getuser()}\\.aws\\credentials')
            config = configparser.ConfigParser()
            config.read(f'C:\\Users\\{getpass.getuser()}\\.aws\\credentials')
            try:
                AWS_ACCESS_KEY_ID = config[PROFILE]['aws_access_key_id']
                AWS_SECRET_ACCESS_KEY = config[PROFILE]['aws_secret_access_key']
                logger.info(f'GET PROFILE: "{PROFILE}"')
            except KeyError:
                logger.info(f'>> {PROFILE} << Not Found in C:\\Users\\{getpass.getuser()}\\.aws\\credentials')

        return AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


class AWS(Enum):

    def __init__(self, profile: str = 'default'):
        self.profile = profile
        aws_access_key_id, aws_secret_access_key = get_aws_credentials(self.profile)
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

