import os
import re
import shutil
import subprocess
import sys

from mflowgen.utils import bold, yellow
from mflowgen.utils import read_yaml, write_yaml


class PkgHandler:

  def __init__( p ):
    p.commands = [
      'foo',
      'help',
      'find',
      'pull',
    ]
 
  
  def launch( p, args, help_, wildcard ):

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
    elif command == 'pull': p.launch_pull( help_, path )
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
   
    if help_ or not wildcard:
      print_help()
      return
    else: os.system(f"find $HOME -type d -iname {wildcard}")


  def launch_help( p ):
    print()
    print( bold( 'Package Commands' ) )
    print()
    print( bold( ' foo :' ), 'Prints', bold('Hello World!')   )
    print()
    print( bold( ' find :'), 'Finds the directories specified by the entered wildcard')
    print()  
