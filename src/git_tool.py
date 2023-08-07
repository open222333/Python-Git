import git
import os


class Git:
    '''使用git做一個類別'''

    def __init__(self, user: str, token: str, git_domain: str) -> None:
        """建立 驗證檔案

        Args:
            user (str): 用戶名
            token (str): 驗證token
            git_domain (str): git主機
        """
        self.user = user
        self.token = token
        self.git_domain = git_domain
        self.branch = None

    def set_git_repo_dir(self, repo_path: str):
        """設置 git專案資料夾

        Args:
            dir_path (str): 專案資料夾路徑
        """
        self.repo_path = repo_path
        self.repo = git.Repo(repo_path)

    def set_branch(self, branch: str):
        """設置 分支

        Args:
            branch (str, optional): 分支名稱
        """
        self.branch = branch

    def is_git_repo(self, dir_path: str) -> bool:
        """檢查是否為git專案

        Args:
            dir_path (str): 專案資料夾路徑

        Returns:
            bool: _description_
        """
        all_items = os.listdir(dir_path)
        return '.git' in all_items

    def get_remote(self):
        """獲取Git存儲庫(repository)中的所有遠端(remote)分支

        Returns:
            _type_: _description_
        """
        return self.repo.remotes

    def get_all_branches(self) -> list:
        """取得所有分支

        Returns:
            list: 分支名稱串列
        """
        branches = self.repo.branches
        all_branch_names = [branch.name for branch in branches]

        return all_branch_names

    def get_modified_files(self) -> list:
        """取得 分支所有提交 修改檔案

        若無使用set_branch指定分支(branch) 則遍歷所有分支

        Returns:
            list: 修改檔案串列
        """
        modified_files = set()
        if self.branch:
            branchs = [self.branch]
        else:
            branchs = self.get_all_branches()

        for branch in branchs:
            commits = self.repo.iter_commits(branch)
            for commit in commits:
                if commit.parents:
                    diff_index = commit.parents[0].diff(commit, create_patch=True)
                    for diff in diff_index:
                        if diff.a_blob and diff.b_blob:
                            modified_files.add(diff.a_blob.path)
                            modified_files.add(diff.b_blob.path)
                        elif diff.a_blob:
                            modified_files.add(diff.a_blob.path)
                        elif diff.b_blob:
                            modified_files.add(diff.b_blob.path)
        return list(modified_files)

    def do_pull(self) -> list:
        """執行pull

        Returns:
            list: 執行的結果
        """
        git_action = self.repo.remote()
        result = git_action.pull()
        return [i.__str__() for i in result]

    def find_file_commit(self, filename: str):
        """遍歷所有分支的提交 搜尋檔案是否在提交中

        Args:
            filename (str): 檔名

        Returns:
            _type_: 回傳None為不存在
        """
        # 遍歷所有分支的提交
        all_commits = []
        for branch in self.repo.branches:
            commits = self.repo.iter_commits(branch)

            for commit in commits:
                # 使用git的指令檢查檔案是否在提交中
                # command = f"git ls-tree {commit.hexsha} {filename}"
                # result = self.repo.git.execute(command, with_extended_output=True)

                # if result.exit_code == 0:
                #     return commit
                files = [os.path.basename(f) for f in commit.stats.files]
                if filename in files:
                    all_commits.append(commit)

        if len(all_commits):
            return all_commits
        else:
            return None
