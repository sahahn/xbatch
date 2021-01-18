import time
import sys
import subprocess
import os
from config import (INTERVAL, USER, MIN_SUBMIT, MAX_JOB_LIMIT,
                    SINGLE_JOB_LIMIT, RESUBMIT_ON_FAIL)


def sbatch(loc):

    output =\
        subprocess.run(['sbatch', loc],
                        stdout=subprocess.PIPE).stdout.decode('utf-8')
    return output


def get_current_n_jobs():

    output = subprocess.run(['squeue', '-u', USER], 
                            stdout=subprocess.PIPE).stdout.decode('utf-8')
    lines = output.split('\n')

    cnt = 0
    for line in lines:

        try:
            job_id = [l for l in line.split(' ') if len(l) > 0][0]
             
            # If a range
            if '[' in job_id and ']' in job_id and '-' in job_id:

                rng = job_id.split('_')[-1]
                s = int(rng.split('-')[0].strip('['))
                e = int(rng.split('-')[1].strip(']'))
                cnt += e + 1 - s
            
            # Otherwise, single job, add 1
            else:
                cnt += 1

        except IndexError:
            pass

    return cnt


def get_x_loc(script_loc):
    
    # Get x script loc from base script location
    base = script_loc.split('.')[0]
    end = '.' + script_loc.split('.')[1]
    
    # In case of existing file...
    cnt = 0
    x_loc = base + '_temp' + str(cnt) + end
    while os.path.exists(x_loc):
        x_loc = base + '_temp' + str(cnt) + end

    return x_loc


def save_x_script(info, x_loc, start, end):

    # Add start and end to lines
    lines = info['lines'].copy()
    lines[info['array_ind']] += str(start) + '-' + str(end)

    # Save file - okay to overwrite existing
    with open(x_loc, 'w') as f:
        for line in lines:
            f.write(line)


def submit(info, start, end):

    # Get loc
    x_loc = get_x_loc(info['script_loc'])
    
    # Save script w/ start and end
    save_x_script(info, x_loc, start, end)

    # Call sbatch on saved script
    output = sbatch(x_loc)

    # Delete temp submit x script
    os.remove(x_loc)
    
    # Return if worked or not
    if 'Submitted batch job' in output:
        return True
    return False


def submit_new(info):
    
    # Get number of already queued or running
    # jobs.
    n_current_jobs = get_current_n_jobs()

    # Compute number of avaliable jobs
    avaliable = MAX_JOB_LIMIT - n_current_jobs

    # Compute remaining number of jobs to run
    remaining = info['end'] + 1 - info['start']
    
    # Start at the last place left off
    start = info['start']

    # If more avaliable than the single job
    # limit, treat the job limit as the number of avaliable.
    avaliable = min(avaliable, SINGLE_JOB_LIMIT)
    
    # Case 1: The number of remaining jobs
    # can all be submitted at once
    if remaining <= avaliable:
        
        # Set end to saved last end
        end = info['end']
    
    # Case 2: Regular submit,
    # make sure avaliable is greater
    # than the min submit threshold
    elif avaliable >= MIN_SUBMIT:

        # -1 as the range is inclusive
        end = start + avaliable - 1
    
    # Case 3: Min submit is less than
    # the number of avaliable, don't submit anything
    else:
        return

    # Try to submit the job.
    worked = submit(info, start, end)
    
    # If failed
    if not worked:
        # Either keep trying with submitting smaller
        # numbers of jobs, if RESUBMIT_ON_FAIL is True
        if RESUBMIT_ON_FAIL:
            while not worked:
                
                # Try with one less each time
                end -= 1

                # If gets to where end is less than start,
                # cancel and skip this round
                if end < start:
                    return
                
                # Try to re-submit with the new end
                worked = submit(info, start, end)
        
        # Otherwise just skip this round
        else:
            return

    # Update saved start
    info['start'] = end + 1

    return
    

def init_script_parse(script_loc):
    
    # Extract needed info from base script
    with open(script_loc, 'r') as f:
        lines = f.readlines()

    # Save parsed in info
    info = {'script_loc': script_loc}

    # Parse script file
    for ind in range(len(lines)):

        # Fine line with array info
        if lines[ind].startswith('#SBATCH --array='):
            
            # Extract range
            rng = lines[ind].split('#SBATCH --array=')[1]
            info['start'] = int(rng.split('-')[0].strip())
            info['end'] = int(rng.split('-')[1].strip())

            # Save ind of array
            info['array_ind'] = ind

            # Re-save line with just stub
            lines[ind] = '#SBATCH --array='

    # Save lines to info
    info['lines'] = lines

    return info


def main():

    # Extract the script_loc
    args = list(sys.argv)
    script_loc = args[1]
    
    # Create info dict from passed script
    info = init_script_parse(script_loc)

    # Submit initial jobs
    # Note: this is outside of
    # the loop s.t., the task manager doesn't
    # have to wait a full interval after submitting
    # the last jobs to close the program
    submit_new(info)

    # Enter job submission loop,
    # which will continue while
    # start is less than or equal to end,
    # note they can be equal as the range is inclusive,
    # so when equal just means 1 job remaining.
    while info['start'] <= info['end']:

        # Wait one interval
        time.sleep(INTERVAL)

        # Try to submit more jobs based on
        # avaliable jobs and remaining jobs
        submit_new(info)

    # Done
    return


if __name__ == "__main__":
    main()