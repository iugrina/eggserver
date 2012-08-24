"""

Egg server deployment scripts

Available targets:
  * export_latest_revision -- exports the latest revision of the server from the
    current branch of the Git repository into /tmp/eggserver-export/
  * deploy -- copy the exported revision to the Egg server
  * install_upstart_scripts -- install the necessary upstart scripts for easier
    starting / restarting of the server
  * venv_update -- update the virtualenv environment on the Egg server

"""

from fabric.api import *
import os

env.hosts = [ 'hatch.et-ego.com' ]

def install_upstart_scripts():
  """
  enables process management of Egg servers via the upstart init system

  allows starting, stopping and restarting servers using these commands:
    service eggserver_api start
    service eggserver_api stop
    service eggserver_api restart
  """
  with cd("/var/eggserver/src/"):
    sudo("cp upstart_templates/eggserver_api.conf /etc/init/")

def venv_update(username=""):
  """
  update the virtualenv on the server
  TODO: add an 'upgrade' option
  """
  with cd("/var/eggserver/src/"):
    run("source ../bin/activate && pip install -r deps.txt")

def export_latest_revision():
  """
  locally exports the latest Git revision to /tmp/eggserver-export
  NOTE: this will always export the current Git branch on the user's computer;
  one should be careful to always use the master branch
  """
  if os.path.exists("/tmp/eggserver-export/"):
    local("rm -r /tmp/eggserver-export")
  
  local("mkdir -p /tmp/eggserver-export/")
  local("git checkout-index -f -a --prefix=/tmp/eggserver-export/")

  with lcd("app/lib/voluptuous"):
    local("git checkout-index -f -a --prefix=/tmp/eggserver-export/app/lib/voluptuous/")

def deploy(username=""):
  """
  copies the previously exported repo to the server
  """
  if len(username) is 0:
    raise Exception("Please pass a username, i.e. fab deploy:username=foo")

  if not os.path.exists("/tmp/eggserver-export/"):
    raise Exception("Please run 'fab export_latest_revision' before running 'fab deploy'")

  local("rsync -avz -e ssh /tmp/eggserver-export/ " + username + "@hatch.et-ego.com:/var/eggserver/src/")
