from fabric.api import run, local, cd
import os

def venv_update(username=""):
  with cd("/var/eggserver/src/"):
    run("source ../bin/activate && pip install -r deps.txt")

def export_latest_revision():
  if os.path.exists("/tmp/eggserver-export/"):
    local("rm -r /tmp/eggserver-export")
  
  local("mkdir -p /tmp/eggserver-export/")
  local("git checkout-index -f -a --prefix=/tmp/eggserver-export/")

def deploy(username=""):
  if len(username) is 0:
    raise Exception("Please pass a username, i.e. fab deploy:username=foo")

  if not os.path.exists("/tmp/eggserver-export/"):
    raise Exception("Please run 'fab export_latest_revision' before running 'fab deploy'")

  local("rsync -avz -e ssh /tmp/eggserver-export/ " + username + "@hatch.et-ego.com:/var/eggserver/src/")
