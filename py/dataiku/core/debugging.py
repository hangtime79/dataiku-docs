import traceback, signal, sys

def debug_sighandler(sig, frame):
   """Interrupt running process, and provide a python prompt for
   interactive debugging."""
   d={'_frame':frame}         # Allow access to frame object.
   d.update(frame.f_globals)  # Unless shadowed by global
   d.update(frame.f_locals)

   print "-------------------\n"
   print "Signal received : traceback for main thread:\n"
   print ''.join(traceback.format_stack(frame))
   print "Additional threads\n"
   for f2 in sys._current_frames().values():
       print "STACK:"
       print ''.join(traceback.format_stack(f2))
       print "\n"
   print "-------------------\n"
   sys.stdout.flush()
   sys.stderr.flush()

def install_handler():
   print "Installing debugging signal handler"
   signal.signal(signal.SIGUSR1, debug_sighandler)  # Register handler