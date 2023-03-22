from test2 import worker
import multiprocessing
if __name__ == '__main__':
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    temp=[1,2]
    for i in temp:
            p = multiprocessing.Process(target=worker, args=(i,return_dict))
            jobs.append(p)
            p.start()
    for proc in jobs:
      proc.join()
    print(return_dict.values())