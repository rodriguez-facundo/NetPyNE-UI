import setuptools
from setuptools.command.install import install
import subprocess
import json
import os, sys
from shutil import copyfile

branch = "development"

#by default clones branch (which can be passed as a parameter python install.py branch test_branch)
#if branch doesnt exist clones the default_branch
def clone(repository, folder, default_branch, cwdp='', recursive = False):
    global branch
    print("Cloning "+repository)
    if recursive:
        subprocess.call(['git', 'clone', '--recursive', repository], cwd='./'+cwdp)
    else:
        subprocess.call(['git', 'clone', repository], cwd='./'+cwdp)
    checkout(folder, default_branch, cwdp)

def checkout(folder, default_branch, cwdp):
    currentPath = os.getcwd()
    print(currentPath)
    newPath = currentPath+"/"+cwdp+folder
    print(newPath)
    os.chdir(newPath)
    python_git=subprocess.Popen("git branch -a",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    outstd,errstd=python_git.communicate()
    if branch in str(outstd):
        subprocess.call(['git', 'checkout', branch], cwd='./')
    else:
        subprocess.call(['git', 'checkout', default_branch], cwd='./')
    os.chdir(currentPath)

def main(argv):
    global branch
    if(len(argv) > 0):
        if(argv[0] == 'branch'):
           branch = argv[1]

if __name__ == "__main__":
    main(sys.argv[1:])

os.chdir(os.getcwd()+"/../")
# Cloning Repos
clone('https://github.com/openworm/pygeppetto.git','pygeppetto','development')
subprocess.call(['pip', 'install', '-e', '.'], cwd='./pygeppetto/')

clone('https://github.com/Neurosim-lab/netpyne.git','netpyne','ui')
subprocess.call(['pip', 'install', '-e', '.'], cwd='./netpyne/')

clone('https://github.com/openworm/org.geppetto.frontend.jupyter.git','org.geppetto.frontend.jupyter','py3','', True )
checkout('geppetto', 'py3','org.geppetto.frontend.jupyter/src/jupyter_geppetto/')
clone('https://github.com/MetaCell/geppetto-netpyne.git','geppetto-netpyne','0.4','org.geppetto.frontend.jupyter/src/jupyter_geppetto/geppetto/src/main/webapp/extensions/')

print("Enabling Geppetto NetPyNE Extension ...")
geppetto_configuration = os.path.join(os.path.dirname(__file__), './utilities/GeppettoConfiguration.json')
copyfile(geppetto_configuration, './org.geppetto.frontend.jupyter/src/jupyter_geppetto/geppetto/src/main/webapp/GeppettoConfiguration.json')

# Installing and building
print("NPM Install and build for Geppetto Frontend  ...")
subprocess.call(['npm', 'install'], cwd='./org.geppetto.frontend.jupyter/src/jupyter_geppetto/geppetto/src/main/webapp/')
subprocess.call(['npm', 'run', 'build-dev-noTest'], cwd='./org.geppetto.frontend.jupyter/src/jupyter_geppetto/geppetto/src/main/webapp/')

print("Installing jupyter_geppetto python package ...")
subprocess.call(['pip', 'install', '-e', '.'], cwd='./org.geppetto.frontend.jupyter')
print("Installing jupyter_geppetto Jupyter Extension ...")
subprocess.call(['jupyter', 'nbextension', 'install', '--py', '--symlink', '--user', 'jupyter_geppetto'], cwd='./org.geppetto.frontend.jupyter')
subprocess.call(['jupyter', 'nbextension', 'enable', '--py', '--user', 'jupyter_geppetto'], cwd='./org.geppetto.frontend.jupyter')
subprocess.call(['jupyter', 'nbextension', 'enable', '--py', 'widgetsnbextension'], cwd='./org.geppetto.frontend.jupyter')
subprocess.call(['jupyter', 'serverextension', 'enable', '--py', 'jupyter_geppetto'], cwd='./org.geppetto.frontend.jupyter')

print("Installing NetPyNE UI python package ...")
subprocess.call(['pip', 'install', '-e', '.'], cwd='.')
