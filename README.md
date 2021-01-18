# eXtra batching (xbatch) for SLURM

Need to submit a large number of SLURM jobs? Tired of logging on at odd hours to fill the queue? Tried of seeing

    sbatch: error: QOSMaxSubmitJobPerUserLimit
    sbatch: error: Batch job submission failed: Job violates accounting/QOS policy (job submit limit, user's size and/or time limits)


Then xbatch is for you.

--- 

xbatch is simple utility designed to be a drop in replacement for some of the functionality of the SLURM sbatch command (in the future, more complete support may be added if their is interest). Simply put, xbatch allows submitting job arrays beyond the maximum size enforced by the QOSMaxSubmitJobPerUserLimit.

To use xbatch, simply modify an existing sbatch scripts array arguments, for example let's assume the maximum limit on the cluster is 1000, but you need to run 5000 jobs. First change the array header to:

    #SBATCH --array=1-5000

Assuming that the limit of jobs per one script is also limited to 1000, this would normally prompt an error when submitting with:

    sbatch script.sh

By just replacing sbatch with xbatch though, and it should now submit!

    xbatch script.sh

Instead of a job id, xbatch will return to you a pid (process id). You may want to keep track of this id, as if you want to cancel the xbatch job manager, you will need to call:

    kill pid_returned_by_xbatch

Which will kill the job manager created by xbatch.

On the backend what sbatch will do is create a job manager that runs in the background (w/ the process id mentioned above). This job manager will handle keeping your queue of jobs up to the limit. E.g., you should see by calling squeue in the example referenced above that to start only 1000 jobs were submitted to the queue as jobid_[1-1000]. What will then happen is that after an interval of time (set by INTERVAL in config.py) Any open spots in the queue (lets say 200 jobs finished) will be submitted, so you will see another array job submitted to the queue as jobid_[1001-1200]. This process will repeat every INTERVAL until all the requested jobs have been completed!

## Setup

Convinced? Want to give it a try? To setup xbatch, first clone this repository on your
SLURM cluster account (anywhere you have permissions is fine.) This can be done with:

    git clone https://github.com/sahahn/xbatch

Next, navigate into the xbatch directory and run setup.sh

    cd xbatch
    bash setup.sh

This will guide you through setting some key configuration parameters and then add
an xbatch alias to your .bashrc file. After this is done xbatch is ready to go!

## Requiriments

xbatch has only been tested with python3+, and does not rely on any external python packages. The only other requiriment is an account on a SLURM cluster to use xbatch with.