# Config info needed

USER = "sahahn"
USER_DESC = 'The name of the SLURM user using xbatch, e.g., your login name'

INTERVAL = 21600
INTERVAL_DESC = 'How often xbatch should check to add new jobs in seconds. ' \
                'e.g., 1 hour == 3600, and new jobs will attempt to be added every hour.' \
                '. 21600 == 6 hours.'

MAX_JOB_LIMIT = 1000
MAX_JOB_LIMIT_DESC = 'The number of jobs a user can submit / have running as ' \
                     'enforced by the cluster.'

SINGLE_JOB_LIMIT = 1000
SINGLE_JOB_LIMIT_DESC = 'The max number of jobs that can ' \
                        'be submitted in one array as enforced by the cluster. ' \
                        'This is also the maximum number of jobs ' \
                        'that will be submitted in one INTERVAL'
                        
MIN_SUBMIT = 5
MIN_SUBMIT_DESC = 'Minimum number of jobs to submit at once ' \
                  'with the exception of the last submission. ' \
                  'e.g., if only 20 left and MIN_SUBMIT = 100 ' \
                  'will submit just 20.'

RESUBMIT_ON_FAIL = True
RESUBMIT_ON_FAIL_DESC =\
    'In the case that a job does not submit ' \
    'this optional parameter if set to True ' \
    'will try to submit the same job with 1 less ' \
    'in the array. Note: this may cause the ' \
    'number of jobs in the array to be less than ' \
    'the min submit limit. ' \
    'If False: Then no jobs will be submitted this interval, ' \
    'but the manager will try again next interval. ' \
