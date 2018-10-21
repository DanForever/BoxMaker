#Author-Daniel Neve
#Description-

from .box import command

_cmd = command.Box()

def run( context ):
	try:
		global _app

		global _cmd
		_cmd.Start()

	except:
		import traceback
		print( 'run() Exception:\n{}'.format( traceback.format_exc() ) )

def stop( context ):
	try:
		global _cmd
		_cmd.Stop()

	except:
		import traceback
		print( 'stop() Exception:\n{}'.format( traceback.format_exc() ) )
