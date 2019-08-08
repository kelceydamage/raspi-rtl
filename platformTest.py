from common.transform import Transform

DSDSL = {
    0: {
        'tasks': {
            'task_null': {}
        }
    }
}

if __name__ == '__main__':
    Job = Transform().execute(DSDSL).result()