import random
from core.tasks import get_simulated_total_for_qcr_core_set
from celery.result import allow_join_result

def simulate_multiple_boxes(qcr_core_set_list, num_iterations):
    # results = []
    # chunk_size = 10
    # chunks = [num_iterations/chunk_size for _ in range(chunk_size)]
    # tasks = []
    # for chunk in chunks:
    #     task = [tasks.append(get_simulated_total_for_qcr_core_set.delay(qcr_core_set)) for _ in range(chunk)]
    #     with allow_join_result():
    #         results.extend([task.get() for task in tasks])
    # return results

    results = []
    chunk_size = 10
    chunks = [num_iterations // chunk_size for _ in range(chunk_size)]
    tasks = []
    # Create and execute Celery tasks for each chunk
    for chunk in chunks:
        for _ in range(chunk):
            
            task = get_simulated_total_for_qcr_core_set.delay(qcr_core_set_list)
            tasks.append(task)
    
    # Gather results from Celery tasks
    with allow_join_result():
        for task in tasks:
            print(task.get())
            results.append(task.get())

    return results