from flask import Flask
from flask import request
from threading import Thread
import time
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

global time_
time_ = time.time()

def get_from_env(token):
  return os.environ.get(token)

SUCCESS_COMPLETE = 'YES'

TIMER = int(get_from_env('TIMER_SEC'))
PORT = get_from_env('PORT')

ACCESS_KEY = get_from_env('ACCESS_KEY')
ACCESS_KEY_NAME = get_from_env('ACCESS_KEY_NAME')

SCRIPT_KEY_NAME = get_from_env('SCRIPT_KEY_NAME')
SCRIPT_KEY_RATING_TEAMS = get_from_env('SCRIPT_KEY_RATING_TEAMS')
SCRIPT_KEY_STUDENT_RATING = get_from_env('SCRIPT_KEY_STUDENT_RATING')
SCRIPT_KEYS = [SCRIPT_KEY_RATING_TEAMS, SCRIPT_KEY_STUDENT_RATING]


SH_DIRECTORY="../sh/"

get_file_path = lambda file : SH_DIRECTORY + file

SCR_CHECK_UPDATE_PATH = get_file_path(get_from_env('SCR_CHECK_UPDATE_FILE'))
SCR_STOP_PM2_PATH = get_file_path(get_from_env('SCR_STOP_PM2_FILE'))
SCR_RESTART_PM2_PATH = get_file_path(get_from_env('SCR_RESTART_PM2_FILE'))
SCR_UPDATE_REPO_PATH = get_file_path(get_from_env('SCR_UPDATE_REPO_FILE'))

app = Flask('')
@app.route('/')
def root():
  check_keys_result = check_keys()
  if check_keys_result != True:
    return check_keys_result

  check_cooldown_result = check_cooldown()
  if check_cooldown_result != True:
    return check_cooldown_result

  script_key = request.headers.get(SCRIPT_KEY_NAME)
  if script_key not in SCRIPT_KEYS: return 'invalid script key'

  return refresh(script_key)

def check_keys():
  access_key = request.headers.get(ACCESS_KEY_NAME)
  script_key = request.headers.get(SCRIPT_KEY_NAME)
  if access_key != ACCESS_KEY:
    return 'invalid access key'
  if script_key == None or script_key == '':
    return 'script key is empty'
  return True

def check_cooldown():
  global time_
  if int(time.time() - time_) < TIMER:
    return 'please, wait for ' + str(TIMER - int(time.time() - time_)) + 's'

  time_ = time.time()
  return True

def refresh(key):
  const_source = get_script_consts_source(key)

  try:
    # launch_sh_wrap(SCR_CHECK_UPDATE_PATH, const_source, 'repo in already up to date | ')
    launch_sh_wrap(SCR_STOP_PM2_PATH, const_source, 'stop process by name with pm2 was failed | ')
    launch_sh_wrap_update_repo(SCR_UPDATE_REPO_PATH, const_source, 'git pull script failed | ', get_project_branch(key))
    launch_sh_wrap(SCR_RESTART_PM2_PATH, const_source, 'restart process by name with pm2 was failed | ')
  except Exception as e:
    return e

  return 'success, project is reloading...'

def launch_sh_wrap_update_repo(path, const_source, msg, branch):
  print('path: {0} source: {1} branch: {2}'.format(path, const_source, branch))
  result = str(subprocess.check_output([path, const_source, branch]))
  if SUCCESS_COMPLETE not in result:
    raise msg + path + '\n'

def launch_sh_wrap(path, const_source, msg):
  print('path: {0} source: {1}'.format(path, const_source))
  result = str(subprocess.check_output([path, const_source]))
  if SUCCESS_COMPLETE not in result:
    raise msg + path + '\n'


def get_script_consts_source(key):
  directory = "../sh/"
  return {
    SCRIPT_KEY_RATING_TEAMS: directory+"consts-rating-teams.sh",
    SCRIPT_KEY_STUDENT_RATING: directory+"consts-student-rating.sh"
  }[key]

def get_project_branch(key):
  return {
    SCRIPT_KEY_RATING_TEAMS: "main",
    SCRIPT_KEY_STUDENT_RATING: "master"
  }[key]

def run():
  app.run(host='0.0.0.0', port=PORT)


def keep_alive():
  t = Thread(target=run)
  t.start()
