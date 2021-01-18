import sys
import subprocess
import os
import inspect

def start_manager(script_loc):

    job_manager_loc = os.path.abspath(inspect.getfile(main))
    job_manager_loc.replace('xbatch.py', 'job_manager.py')

    pid =\
        subprocess.Popen(['python',
                          os.path.realpath(job_manager_loc),
                          script_loc], close_fds=True).pid

    return pid

def main():
    
    # Extract script name
    script_name = list(sys.argv)[0]
    script_loc = os.path.abspath(script_name)
    
    # Start manager
    manager_pid = start_manager(script_loc)
    
    print('Started Job Manager with pid:', manager_pid)

if __name__ == "__main__":
    main()