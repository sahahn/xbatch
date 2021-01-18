import inspect
import os
from config import (USER_DESC, INTERVAL_DESC, MAX_JOB_LIMIT_DESC,
                    SINGLE_JOB_LIMIT_DESC, MIN_SUBMIT_DESC, RESUBMIT_ON_FAIL_DESC)

def get_config_loc():

    config_loc = os.path.abspath(inspect.getfile(main))
    config_loc = config_loc.replace('config_setup.py', 'config.py')
    return config_loc

def main():

    config_loc = get_config_loc()

    with open(config_loc, 'r') as f:
        lines = f.readlines()

    for i in range(len(lines)):

        line = lines[i]
        
        if line.startswith('USER = '):
            print(USER_DESC)
            USER = input('USER (str): ')
            if len(USER) == 0:
                raise RuntimeError('USER cannot be empty!')

            print()

            lines[i] = 'USER = "' + USER + '"\n'

        elif line.startswith('INTERVAL = '):
            print(INTERVAL_DESC)
            INTERVAL = input('INTERVAL (int, default=21600): ')
            print()
            
            if INTERVAL == '':
                INTERVAL = '21600'
            else:
                INTERVAL = str(int(INTERVAL))

            lines[i] = 'INTERVAL = ' + INTERVAL + '\n'
      
        elif line.startswith('MAX_JOB_LIMIT = '):
            print(MAX_JOB_LIMIT_DESC)
            MAX_JOB_LIMIT = input('MAX_JOB_LIMIT (int, default=1000): ')
            print()

            if MAX_JOB_LIMIT == '':
                MAX_JOB_LIMIT = '1000'
            else:
                MAX_JOB_LIMIT = str(int(MAX_JOB_LIMIT))

            lines[i] = 'MAX_JOB_LIMIT = ' + MAX_JOB_LIMIT + '\n'

        elif line.startswith('SINGLE_JOB_LIMIT = '):
            print(SINGLE_JOB_LIMIT_DESC)
            SINGLE_JOB_LIMIT = input('SINGLE_JOB_LIMIT (int, default=1000): ')
            print()

            if SINGLE_JOB_LIMIT == '':
                SINGLE_JOB_LIMIT = '1000'
            else:
                SINGLE_JOB_LIMIT = str(int(SINGLE_JOB_LIMIT))

            lines[i] = 'SINGLE_JOB_LIMIT = ' + SINGLE_JOB_LIMIT + '\n'

        elif line.startswith('MIN_SUBMIT = '):
            print(MIN_SUBMIT_DESC)
            MIN_SUBMIT = input('MIN_SUBMIT (int, default=5): ')
            print()

            if MIN_SUBMIT == '':
                MIN_SUBMIT = '5'
            else:
                MIN_SUBMIT = str(int(MIN_SUBMIT))

            lines[i] = 'MIN_SUBMIT = ' + MIN_SUBMIT + '\n'

        elif line.startswith('RESUBMIT_ON_FAIL = '):
            print(RESUBMIT_ON_FAIL_DESC)
            RESUBMIT_ON_FAIL = input('RESUBMIT_ON_FAIL (bool, default=True): ')
            print()

            if RESUBMIT_ON_FAIL == '':
                RESUBMIT_ON_FAIL = 'True'
            else:

                RESUBMIT_ON_FAIL = RESUBMIT_ON_FAIL.lower()

                if RESUBMIT_ON_FAIL == 'true' or RESUBMIT_ON_FAIL == '1':
                    RESUBMIT_ON_FAIL = 'True'
                else:
                    RESUBMIT_ON_FAIL = 'False'

            lines[i] = 'RESUBMIT_ON_FAIL = ' + RESUBMIT_ON_FAIL + '\n'

    with open(config_loc, 'w') as f:
        for line in lines:
            f.write(line)

    print('Parameters saved! Note: in the future to change any of these configuration settings, either manually edit config.py or call python config_setup.py')
    print()

if __name__ == "__main__":
    main()
