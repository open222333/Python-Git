import os
from src.git import Git
from src.logger import Log
from src import REPOS, LOG_LEVEL, LOG_FILE_DISABLE

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-f', '--filename', help='要尋找的檔案名稱', required=True)
args = parser.parse_args()

"""
搜尋指定檔案
"""

logger = Log()
logger.set_level(LOG_LEVEL)
if not LOG_FILE_DISABLE:
    logger.set_file_handler()
logger.set_msg_handler()

if __name__ == "__main__":
    for repo in REPOS:
        logger.info(f'執行 {repo["repo_dir_path"]}')
        g = Git(
            user=repo['user'],
            token=repo['token'],
            git_domain=repo['git_domain']
        )
        if os.path.exists(repo['repo_dir_path']):
            g.set_git_repo_dir(repo['repo_dir_path'])
        else:
            logger.error(f"{repo['repo_dir_path']} 不存在")
            exit()

        if repo['branch']:
            g.set_branch(repo['branch'])

        info = g.find_file_commit(args.filename)
        logger.info(f'搜尋結果: {info}')
