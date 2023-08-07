from src.git_tool import Git
from src.logger import Log
from src import REPOS, LOG_LEVEL, LOG_FILE_DISABLE
import os


"""
遍歷出所有 檔案
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

        files = g.get_modified_files()
        output_dir = 'output'

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(f'{output_dir}/all_files.txt', 'a') as f:
            for file in files:
                logger.debug(f'{file} 寫入 {output_dir}/all_files.txt')
                f.write(f'{file}\n')
