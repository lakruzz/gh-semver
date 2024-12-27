import subprocess
import json
import sys
import re
import base64
import os
import time

# Add directory of this class to the general class_path
# to allow import of sibling classes
class_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(class_path)

from ghutils import Ghutils

class Repo:
    """
    A class to represent a GitHub repository.
    """    
    def __init__(self, org_name, repo_name):
        self.org_name = org_name
        self.repo_name = repo_name
        
        print(Ghutils.get_pull_request_counts(self.org_name, self.repo_name))
        
        
        _,self.repo, responseheader = Ghutils.query_github_incl_header(f'repos/{self.org_name}/{self.repo_name}')
        print(responseheader)
        _,self.contributors = Ghutils.query_github(f'repos/{self.org_name}/{self.repo_name}/contributors')
    
        _,self.issues = Ghutils.query_github_allpages(f"repos/{self.org_name}/{self.repo_name}/issues?state=all")
        _,self.prs = Ghutils.query_github_allpages(f'repos/{self.org_name}/{self.repo_name}/pulls?state=all')
        _,self.commits = Ghutils.query_github(f'repos/{self.org_name}/{self.repo_name}/commits')
        
        self.open_issues_count = self.repo['open_issues_count']
        self.closed_prs_count = Ghutils.get_element_count(self.prs, 'state', 'closed')
        self.open_prs_count = Ghutils.get_element_count(self.prs, 'state', 'open')
        self.closed_issues_count = Ghutils.get_element_count(self.issues, 'state', 'closed')
        self.issue_title_template = self.org_name+"/"+self.repo_name+" - Report"        
        
    def get_issue_by_title(self,regex):
        json_obj = Ghutils.get_element_by_regex(self.issues,'title',regex)
        if json_obj is not None:
            return json_obj['number']
        elif json_obj is None:
            return None

    @staticmethod
    def full_report(org_name, repo_name, target: str = 'stdout'):
        my_ghrepo = Repo(org_name, repo_name)
        my_ghrepo.md_repo()
        my_ghrepo.md_contributors()
        my_ghrepo.md_community_standards()
        Ghutils.merge_buffers()
        if target == 'stdout':
            Ghutils.buffer_to_stdout()
        elif target == 'issue':
            my_ghrepo.update_issue()
        else:
            Ghutils.buffer_to_file(target)
            
    def update_issue(self):
        Ghutils.buffer_to_file('tmp_issue_body.md')
        retval = 101
        issue_number = self.get_issue_by_title("^"+self.issue_title_template+"$")
        try:
            if issue_number is not None:
                print(f"Updating issue {issue_number}")
                result = subprocess.run(['gh', 'issue', 'edit', "{issue_number}", '--body-file', 'tmp_issue_body.md'], capture_output=True, text=True)
                if result.returncode == 0:                
                  print(result.stdout)
                  retval = 0
                  
                print(f"Making sure issue {issue_number} is open")
                result = subprocess.run(['gh', 'issue', 'reopen', str(issue_number) ], capture_output=True, text=True)
                print(result.stdout)
                print(result.stderr)
            else:
                print(f"Creating issue '{self.issue_title_template}'")
                result = subprocess.run(['gh', 'issue', 'create', '--title', self.issue_title_template, '--body-file', 'tmp_issue_body.md'], capture_output=True, text=True)
                if result.returncode == 0:
                  print (result.stdout)
                  retval = 0
                else:
                  print (result.stderr) 
                  retval = 1
        finally:
            subprocess.run(['rm', 'tmp_issue_body.md'])
            return retval 

        
    def md_community_standards(self):
        Ghutils.print_to_buffer(f"### Community standards\n")
        self.md_get_codeowners()
        self.md_get_readme()
        self.md_get_contributing()
        self.md_get_license()
        self.md_get_gitginore()
        
    def md_get_license(self):
        status,license_file = Ghutils.query_github(f'repos/{self.org_name}/{self.repo_name}/contents/LICENSE',False)     
        if status != 0:
            Ghutils.print_to_buffer(f"- [ ] `LICENSE` file [(Set it up!)]({Ghutils.about_license_url})")
        else:
            Ghutils.print_to_buffer(f"- [x] `LICENSE` file")
            Ghutils.details_summary_to_buffer("See content of <code>LICENSE</code>","```\n"+base64.b64decode(license_file['content']).decode('utf-8')+"\n```")
    
    def md_get_gitginore(self):
        status,gitignore_file = Ghutils.query_github(f'repos/{self.org_name}/{self.repo_name}/contents/.gitignore',False)     
        if status != 0:
            Ghutils.print_to_buffer(f"- [ ] `.gitignore` file [(Set it up!)]({Ghutils.gitginore_templates_url})")
        else:
            Ghutils.print_to_buffer(f"- [x] `.gitignore` file")
            Ghutils.details_summary_to_buffer("See content of <code>.gitignore</code>","```gitginore\n"+base64.b64decode(gitignore_file['content']).decode('utf-8')+"\n```")
    
    def md_get_readme(self):
        status,readme_file = Ghutils.query_github(f'repos/{self.org_name}/{self.repo_name}/contents/README.md',False)     
        if status != 0:
            Ghutils.print_to_buffer(f"- [ ] `README.md` file [(Set it up!)]({Ghutils.about_readme_url})")
        else:
            Ghutils.print_to_buffer(f"- [x] `README.md` file")
            Ghutils.details_summary_to_buffer("See content of <code>README.md</code>",base64.b64decode(readme_file['content']).decode('utf-8'))
    
    def md_get_contributing(self):
        status,contributing_file = Ghutils.query_github(f'repos/{self.org_name}/{self.repo_name}/contents/CONTRIBUTING.md',False)     
        if status != 0:
            # Special case: CONTRIBUTING.md file is not found, but CONTRIBUTE.md is found
            status,contributing_file = Ghutils.query_github(f'repos/{self.org_name}/{self.repo_name}/contents/CONTRIBUTE.md',False)     
            if status != 0: 
                Ghutils.print_to_buffer(f"- [ ] `CONTRIBUTING.md` file")
            else:
                Ghutils.print_to_buffer(f"- [x] `CONTRIBUTE.md` file - **Note:** [Consider renaming it to `CONTRIBUTING.md`]({Ghutils.about_contributing_url})")
                Ghutils.details_summary_to_buffer("See content of <code>CONTRIBUTE.md</code>",base64.b64decode(contributing_file['content']).decode('utf-8'))
        else:
            Ghutils.print_to_buffer(f"- [x] `CONTRIBUTING.md` file")
            Ghutils.details_summary_to_buffer("See content of <code>CONTRIBUTING.md</code>",base64.b64decode(contributing_file['content']).decode('utf-8'))
    
    def md_get_codeowners(self):
        # Retrieve the CODEOWNERS file content and decode it from base64
           status,codeowners_file = Ghutils.query_github(f'repos/{self.org_name}/{self.repo_name}/contents/CODEOWNERS',False)  
           if status != 0:
               Ghutils.print_to_buffer(f"- [ ] `CODEOWNERS` file [(Set it up!)]({Ghutils.about_codeowners_url})")
           else:
               Ghutils.print_to_buffer(f"- [x] `CODEOWNERS` file")
               codeowners = base64.b64decode(codeowners_file['content']).decode('utf-8')
               # Regular expression pattern to match mentions of @user or @team
               owner_pattern = r"@([\w\-\/]+)"
               # Loop through each line in the codeowners file, extract the owners and print them
               owners = []
               for line in codeowners.split("\n"):
                   # Skip comments and blank lines
                   if line.lstrip().startswith("#") or not line.strip():
                       continue
                   
                   # Use the regular expression to find all owners in the line
                   line_owners = re.findall(owner_pattern, line)
                   # Remove duplicates and print the owners found in the line
                   if line_owners:
                       owners.extend(line_owners)
               unique_owners ='' 
               for owner in list(set(owners)):
                   unique_owners += f" - @{owner}\n"
               Ghutils.details_summary_to_buffer("See list of mentioned CODEOWNERS",unique_owners) 
 
    def md_repo(self):
        """Output in MarkDown the details of the repository.

        Returns:
            None
        """

        # Print the full name of the repo in a header and link to both org and repo
        Ghutils.print_to_buffer(
            f"## [{self.repo['owner']['login']}]({self.repo['owner']['html_url']})/[{self.repo['name']}]({self.repo['html_url']})")
        
        # Print the description of the repo if it exists
        if self.repo['description'] is not None:
            Ghutils.print_to_buffer( f"\n_{self.repo['description']}_")
        
        # Print a mermaid pie with numbers of open and closed issues and PRs
        template = '''
### Issues and PRs\n
```mermaid
pie showData title Issues and PRs
"Issues: open" : {}
"Issues: closed" : {}
"PRs : open" : {}
"PRs :closed" : {}
```'''
        Ghutils.print_to_buffer(
            template.format(self.open_issues_count, self.closed_issues_count, self.open_prs_count, self.closed_prs_count))
                  
    def md_contributors(self):
        """
        Qutput in MarkDown the list of contributors to the repository.

        Returns:
            None
        """
        Ghutils.print_to_buffer(f"\n### Contributors\n")
        mermaid = '''
```mermaid
pie showData title Contributors (number of commits)
'''
        for contributor in self.contributors:
            _,user = Ghutils.query_github(f"users/{contributor['login']}")
            bullet = '- [ ]'
            name = f'_Name is not set - [fix it!]({Ghutils.change_ghname_url})_ '
            if user['name'] is not None:
                bullet = f'- [x]'
                name = f"_{user['name']}_"
            Ghutils.print_to_buffer(
                f"{bullet} [{contributor['login']}]({contributor['html_url']}) {name} ([{contributor['contributions']}](https://github.com/{self.org_name}/{self.repo_name}/commits?author={contributor['login']}))")
            mermaid += f'"{contributor["login"]}" : {contributor["contributions"]}\n'
        Ghutils.print_to_buffer(       mermaid + "\n```\n")
    

