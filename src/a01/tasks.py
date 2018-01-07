import requests
import tabulate

import a01.cli
from a01.common import get_store_uri, LOG_FILE


@a01.cli.cmd(name='get task', desc='Retrieve tasks information.')
@a01.cli.arg('ids', help='The task id. Support multiple IDs.', positional=True)
@a01.cli.arg('log', help='Retrieve the log of the task.', option=('-l', '--log'))
def get_task(ids: [str], log: bool = False):
    for task_id in ids:
        resp = requests.get(f'{get_store_uri()}/task/{task_id}')
        resp.raise_for_status()
        task = resp.json()
        view = [
            ('id', task['id']),
            ('result', task['result']),
            ('test', task['settings']['path']),
            ('duration(ms)', task['result_details']['duration'])
        ]

        print(tabulate.tabulate(view, tablefmt='plain'))
        if log:
            log_path = LOG_FILE.format(f'{task["run_id"]}/task_{task_id}.log')
            print()
            for index, line in enumerate(requests.get(log_path).content.decode('utf-8').split('\n')):
                print(f' {index}\t{line}')

        print()
        print()