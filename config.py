# Name of the SLURM user
USER = 'sahahn'

# How often xbatch should check to
# add new jobs, note: 3600 == 1 Hour
INTERVAL = 3600

# Minimum number of jobs to submit at once
# with the exception of the last submission,
# e.g., if only 20 left and MIN_SUBMIT = 100,
# will still submit 
MIN_SUBMIT = 100

# Number of jobs a user can submit as
# enforced by the cluster.
MAX_JOB_LIMIT = 1000

# The max number of jobs that can
# be submitted in one array as
# enforced by the cluster.
# This is also the maximum number of jobs
# that will be queue'ed in one INTERVAL.
SINGLE_JOB_LIMIT = 1000

# In the case that a job does not submit
# this optional parameter if set to True
# will try to submit the same job with 1 less
# in the array. Note: this may cause the
# number of jobs in the array to be less than
# the min submit limit.
# If False: Then no jobs will be submitted this interval,
# but the manager will try again next interval.
RESUBMIT_ON_FAIL = True

