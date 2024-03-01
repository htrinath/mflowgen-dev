import os
import re
import shutil
import subprocess
import sys
import wget

from mflowgen.utils import bold, yellow
from mflowgen.utils import read_yaml, write_yaml

test_dir = "/home/tharikri/ee599/mflowgen-intel16/steps"
virtual_env = os.environ['VIRTUAL_ENV']
mflowgen_libs_path = virtual_env + '/mflowgen_libs' # Abstract it out to $MFLOWGEN_PATH
zip_file = "https://github.com/mflowgen/mflowgen/archive/refs/heads/master.zip"

class PkgHandler:

  def __init__( p ):
    p.commands = [
      'foo',
      'help',
      'find',
      'pull',
    ]
 
  
  def launch( p, args, help_, wildcard, force ):

    if help_ and not args:
      p.launch_help()
      return

    try:
      command = args[0]
      assert command in p.commands # valid commands only
    except Exception as e:
      print( 'pkg: Unrecognized commands (see "mflowgen pkg help")' )
      sys.exit( 1 )

    try:
      assert len( args ) <= 1 # no further positional args are allowed
    except Exception as e:
      print()
      print( 'pkg: Unrecognized positional args' )
      # Allow this exception to pass, but force set the "help" flag so
      # users can see what they should be doing instead.
      help_ = True

    if   command == 'foo' : p.launch_foo( help_ )
    elif command == 'find': p.launch_find( help_, wildcard )
    elif command == 'pull': p.launch_pull( help_, wildcard, force )
    else                  : p.launch_help()


  def launch_foo( p, help_):

    def print_help():
      print()
      print( bold( 'Usage:' ), 'mflowgen pkg foo' )
      print()

    if help_:
      print_help()
      return
    else: print( bold('Hello World!'))


  def launch_find( p, help_, wildcard):
    def print_help():
      print()
      print( bold( 'Usage:' ), 'mflowgen pkg find -w/--wildcard <wildcard>')
      print()
      print( bold( 'Example:' ), 'mflowgen pkg find -w innovus-*')
      print()

    def remove_directory(directory_path):
      try:
        shutil.rmtree(directory_path)
        print(f"\nDirectory '{directory_path}' removed successfully.")
      except FileNotFoundError:
        print(f"\nDirectory '{directory_path}' does not exist.")
      except PermissionError:
        print(f"\nPermission denied to remove directory '{directory_path}'.")
    
    def find_helper(wildcard):
      path_to_zip = mflowgen_libs_path + "/zip"
      
      if not os.path.exists(mflowgen_libs_path):
        os.system(f'mkdir {mflowgen_libs_path}')
      if not os.path.exists(path_to_zip):
        os.system(f'mkdir {path_to_zip}')
      
      if len(os.popen(f"find {mflowgen_libs_path} -type d -iname {wildcard}").read()):
        print(bold("Relevant Nodes found in the local repository!\n"))
        os.system(f"find {mflowgen_libs_path} -type d -iname {wildcard}")
        print(bold("------------------------------------------------------"))
      else:
        fileName = zip_file.split('/')[-1]
        dest_file_path = path_to_zip + "/" + fileName
        wget.download(zip_file, dest_file_path, bar=None)
        shutil.unpack_archive(dest_file_path, path_to_zip)
        print(bold("Relevant Nodes if found in the remote repository are as follows:"))
        os.system(f"find {path_to_zip} -type d -iname {wildcard}")
      remove_directory(path_to_zip)
   
    if help_ or not wildcard:
      print_help()
      return
    else: find_helper(wildcard)


  def launch_pull( p, help_, wildcard, force):
    def print_help():
      print()
      print(bold( 'Usage:' ), 'mflowgen pkg pull -w/--wildcard <wildcard> -f/--force true')
      print()
      print(bold( 'Example: '), 'mflowgen pkg pull -w mentor-calibre-drc')
      print()

    def remove_directory(directory_path):
      try:
        shutil.rmtree(directory_path)
        print(f"\nDirectory '{directory_path}' removed successfully.")
      except FileNotFoundError:
        print(f"\nDirectory '{directory_path}' does not exist.")
      except PermissionError:
        print(f"\nPermission denied to remove directory '{directory_path}'.")

    def pull_helper(wildcard, force):
      path_to_zip = mflowgen_libs_path + "/zip"
      
      if not os.path.exists(mflowgen_libs_path):
        os.system(f'mkdir {mflowgen_libs_path}')
      if not os.path.exists(path_to_zip):
        os.system(f'mkdir {path_to_zip}')
      
      if force:
        for node in os.popen(f"find {mflowgen_libs_path} -type d -iname {wildcard}"):
          os.system(f"rm -rf {node}")
    
      if len(os.popen(f"find {mflowgen_libs_path} -type d -iname {wildcard}").read()):
        print(bold("Relevant Nodes found in the local repository!\n"))
        os.system(f"find {mflowgen_libs_path} -type d -iname {wildcard}")
        print(bold("------------------------------------------------------"))
        print("If the Node you are looking for is not in the above list, please update the wildcard and try again!")
      else:
        fileName = zip_file.split('/')[-1]
        dest_file_path = path_to_zip + "/" + fileName
        wget.download(zip_file, dest_file_path, bar=None)
        shutil.unpack_archive(dest_file_path, path_to_zip)
        print(bold("Relevant Nodes if found in the remote repository are as follows:"))
        valid_nodes = []
        for node in os.popen(f"find {path_to_zip} -type d -iname {wildcard}"):
          node = node.strip().split('\n')
          valid_nodes.append(node[0])
          print(node[0])
          if len(valid_nodes):
            for node in valid_nodes:
              shutil.copytree(node, mflowgen_libs_path + '/' + node.split('/')[-1], dirs_exist_ok=True)
          else: print('No Valid nodes found.')
      remove_directory(path_to_zip)

    if help_ or not wildcard:
      print_help()
      return
    else: pull_helper(wildcard, force)


  def launch_help( p ):
    print()
    print( bold( 'Package Commands' ) )
    print()
    print( bold( ' foo :' ), 'Prints', bold('Hello World!')   )
    print()
    print( bold( ' find :'), 'Finds the directories specified by the entered wildcard.')
    print()
    print(bold( ' pull :'), 'Pulls and links the directories specified by the entered wildcard.')
