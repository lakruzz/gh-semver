import json
import os
import re
import sys
import subprocess
import logging
import inspect
from io import StringIO

# Add directory of this class to the general class_path
# to allow import of sibling classes
class_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(class_path)

# Configure logging
import logging

# Configure logging for the log file
log_dir = 'logs'
if not os.path.exists(log_dir):
  os.makedirs(log_dir)
file_handler = logging.FileHandler('logs/app.log')
file_handler.setLevel(logging.DEBUG)

# Define the log formatter
log_formatter = logging.Formatter('\n%(asctime)s - %(levelname)s\n  Name: %(name)s\n  Function: %(funcName)s()\n  Module: %(module)s\n  File: %(filename)s(%(lineno)d)\n%(message)s', '%Y-%m-%d %H:%M:%S')


file_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.addHandler(file_handler)

logging.basicConfig(filename='logs/app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



class Ghutils:
  change_ghname_url =       "https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-personal-account-settings/changing-your-github-username#changing-your-username"
  about_codeowners_url =    "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners"
  about_readme_url =        "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes"
  about_contributing_url =  "https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors"
  about_license_url =       "https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository"
  gitginore_templates_url = "https://github.com/github/gitignore"
  __buffer = StringIO()
  __buffer2 = StringIO()
  
  @staticmethod
  def print_to_buffer(content):
      print(content, file=Ghutils.__buffer)

  @staticmethod
  def print_to_buffer2(content):
      print(content, file=Ghutils.__buffer2)
      
  @staticmethod
  def merge_buffers():
      Ghutils.__buffer.write(Ghutils.__buffer2.getvalue())
      Ghutils.__buffer2.close()
      
  @staticmethod
  def buffer_to_stdout():
      print(Ghutils.__buffer.getvalue())
      Ghutils.__buffer.close()
      
  @staticmethod
  def buffer_to_file(location: str = "reporeport.md"):
      with open(location, "w") as f:
          f.write(Ghutils.__buffer.getvalue())
      Ghutils.__buffer.close()

  @staticmethod
  def get_org_repo_from_current_directory():
    result = subprocess.run(['gh', 'repo', 'view', '--json', 'owner,name', '--jq', '.owner.login+"/"+.name'], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return None
    
  @staticmethod
  def details_summary_to_buffer(summary:str, details:str):
    template = '''
<details><summary>{}</summary>

---
{}

---
</details>
'''
    Ghutils.print_to_buffer2(
        template.format(summary, details))
  
  @staticmethod
  def get_element_count(json:json, key:str, value:str,):
    """
    Counts of elements in a json, where key=value
    Args:
        json (str): _description_
        key (str): _description_
        value (str): _description_
    Returns:
        int: count of elements in json where key=value
    """
    return sum(1 for element in json if element[key] == value)  

  @staticmethod
  def query_github_allpages(ghapi: str, die_on_error: bool = True):
      """
      Query GitHub's API and compiles the result from all pages if there's more than one.
      More details at https://docs.github.com/en/rest
      Args:
          ghapi (str): The API to query GitHub
          die_on_error: If True, exit the program on error. Default: True
      Returns:
          on success:
          int, []json: The return code from the query and the JSON output
  
          on error:
          int, str: The return code from the query and the error message
      """
      page = 1
      page_size = 100  # Adjust the desired page size here
      json_return = []
      
      # Append page size and page number to the original API call
      api_url = f"{ghapi}&per_page={page_size}&page={page}"
      
      # Let the first run die on error (essentially let query_github() handle the error
      _,json_part = Ghutils.query_github(api_url, True)
      
      # Compile the final result
      json_return.extend(json_part)
      
      # Continue if the page was full
      while len(json_part) == page_size:
          page += 1 # Move to the next page
          api_url = f"{ghapi}&per_page={page_size}&page={page}"
          _,json_part = Ghutils.query_github(api_url, False) #Ignore the error - will handle it by checking the length of the json
          json_return.extend(json_part)
      
      return 0,json_return

  @staticmethod
  def query_github(ghapi:str, die_on_error:bool=True):
      """
      Query GitHub's API. 
      More details at https://docs.github.com/en/rest
      Args:
          api (str): The API to query GitHub
          die_on_error: If True, exit the program on error. Default: True
      Returns:
          on success:
          int,[]json: The returncode from the query and the json output          
          
          on error:
          int,str: The returncode from the query and the error message
      """
      try:
          # Call the GitHub API
          response = subprocess.run(
              ['gh', 'api', ghapi], capture_output=True, text=True, check=True)
          
          # Parse the JSON output of the API call
          
          return response.returncode,json.loads(response.stdout)
      except subprocess.CalledProcessError as e:
          if die_on_error:
              print(f"Error: {e.stderr} {ghapi}", file=sys.stderr)
              sys.exit(1)
          else:
              return e.returncode, f"Error: {e.stderr} {ghapi}" 

  @staticmethod
  def query_github_incl_header(ghapi:str, die_on_error:bool=True):
      """
      Query GitHub's API. 
      More details at https://docs.github.com/en/rest
      Args:
          api (str): The API to query GitHub
          die_on_error: If True, exit the program on error. Default: True
      Returns:
          on success:
          int,[]json: The returncode from the query and the json output          
          
          on error:
          int,str: The returncode from the query and the error message
      """
      logger.info(Ghutils.get_function_realtime_reader())
      
      try:
          # Call the GitHub API
          response = subprocess.run(
              ['gh', 'api', "-i", ghapi], capture_output=True, text=True, check=True)
          
          # Parse the JSON output of the API call
          
          separator_index = response.stdout.find('\n\n')
          rawheader = response.stdout[:separator_index]
          body = json.loads(response.stdout[separator_index + 2:])  
          
          headers = {}
          for line in rawheader.strip().split("\n"):
              if ":" in line:
                  key, value = line.split(":", 1)
                  headers[key.strip()] = value.strip()
              else:
                  if line.startswith("HTTP/"):
                      # split on the first space
                      headers["Status-Text"] = line.split(" ", 1)[1]
                      headers["Status-Code"] = line.split(" ", 2)[1]
                      
          
          
          return response.returncode,body,headers
      
      except subprocess.CalledProcessError as e:
          if die_on_error:
              print(f"Error: {e.stderr} {ghapi}", file=sys.stderr)
              sys.exit(1)
          else:
              error_message = e.stderr
              header = {}
              header["Status-Code"] = re.search(r"HTTP (\d+)", error_message).group(1) if re.search(r"HTTP (\d+)", error_message) else None
 
              return e.returncode, f"Error: {e.stderr} {ghapi}", header 


  @staticmethod
  def get_element_by_regex(json:json,key:str,search:str):
    """
    Get first element from json where key matches regex
    Args:
        json (json): The json to search
        key (str): The key to the value to search
        regex (str): The regex to match
    Returns:
        On match:
            json: element from json where key matches regex

        On no match:
            None    
    """
    regex = re.compile(search)
    for element in json:
        if key in element and regex.search(element[key]):
            return element
    return None

  @staticmethod
  def get_pull_request_counts(owner: str, repo: str):
      try:
          open_prs_url = f"repos/{owner}/{repo}/pulls?state=open"
          closed_prs_url = f"repos/{owner}/{repo}/pulls?state=closed"
  
          open_prs_response = subprocess.run(
              ['gh', 'api', open_prs_url], capture_output=True, text=True, check=True
          )
          open_prs_count = Ghutils.get_total_count_from_header(open_prs_response.stdout)
  
          closed_prs_response = subprocess.run(
              ['gh', 'api', closed_prs_url], capture_output=True, text=True, check=True
          )
          closed_prs_count = Ghutils.get_total_count_from_header(closed_prs_response.stdout)
  
          return open_prs_count, closed_prs_count
  
      except subprocess.CalledProcessError as e:
          print(f"Error: {e.stderr}", file=sys.stderr)
          sys.exit(1)
  
  @staticmethod
  def get_total_count_from_header(header: str) -> int:
      match = re.search(r"page=1>; rel=\"last\", .* page=(\d+)", header)
      if match:
          return int(match.group(1))
      return 0
  
  @staticmethod
  def parse_response_header(header: str) -> dict:
      headers = {}
      for line in header.strip().split("\n"):
          if ":" in line:
              key, value = line.split(":", 1)
              headers[key.strip()] = value.strip()
      return headers
  
  @staticmethod
  def get_function_realtime_reader():
      frame = inspect.currentframe().f_back
      args, _, _, values = inspect.getargvalues(frame)
      function_name = frame.f_code.co_name
      parameter_values = {arg: values[arg] for arg in args}
      return f"Trace:\n  {function_name}({parameter_values})"
    