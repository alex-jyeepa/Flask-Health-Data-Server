from queue import Queue
from threading import Thread, Event
import json
import os


class ThreadPool:
    def __init__(self):
        self.threads = []
        self.jobs = Queue()
        self.job_status = {}
        self.ingestor = None
        self.calls = {}
        self.shutdown = 0
        self.event = Event()

        #verificam variabila de mediu pentru numar de thread-uri,
        #daca este nula luam numarul maxim cu os.cpu_count()
        TP_NUM_OF_THREADS = os.getenv("TP_NUM_OF_THREADS")
        if TP_NUM_OF_THREADS:
            self.num_of_threads = TP_NUM_OF_THREADS
        else:
            self.num_of_threads = os.cpu_count()

        #fiecare thread are acces la task_runner pentru
        #a avea acces la coada de job-uri
        for _ in range(self.num_of_threads):
            self.threads.append(TaskRunner(self))

    def start(self):
        for thread in self.threads:
            thread.start()

    def join(self):
        self.event.set()
        for thread in self.threads:
            thread.join()


class TaskRunner(Thread):
    def __init__(self, tpool: ThreadPool):
        super().__init__()
        self.tpool = tpool

    def run(self):
        while 1:
            #thread-urile verifica mereu coada
            if not self.tpool.jobs.empty():
                job = self.tpool.jobs.get()
                self.tpool.job_status[job["job_id"]] = "running"
                if job["job_type"] == "states_mean":
                    job["result"] = self.tpool.ingestor.mean_best_worst(
                        job["data"]["question"], "mean"
                    )
                elif job["job_type"] == "state_mean":
                    job["result"] = self.tpool.ingestor.state_mean(
                        job["data"]["state"], job["data"]["question"]
                    )
                elif job["job_type"] == "best5":
                    job["result"] = self.tpool.ingestor.mean_best_worst(
                        job["data"]["question"], "best"
                    )
                elif job["job_type"] == "worst5":
                    job["result"] = self.tpool.ingestor.mean_best_worst(
                        job["data"]["question"], "worst"
                    )
                elif job["job_type"] == "global_mean":
                    job["result"] = self.tpool.ingestor.global_mean(
                        job["data"]["question"], "dictionary"
                    )
                elif job["job_type"] == "diff_from_mean":
                    job["result"] = self.tpool.ingestor.diff_from_mean(
                        job["data"]["question"]
                    )
                elif job["job_type"] == "state_diff_from_mean":
                    job["result"] = self.tpool.ingestor.state_diff_from_mean(
                        job["data"]["state"], job["data"]["question"]
                    )
                elif job["job_type"] == "mean_by_category":
                    job["result"] = self.tpool.ingestor.mean_by_category(
                        job["data"]["question"]
                    )
                elif job["job_type"] == "state_mean_by_category":
                    job["result"] = self.tpool.ingestor.state_mean_by_category(
                        job["data"]["state"], job["data"]["question"]
                    )
                result_file_path = f"results/{job['job_id']}"
                with open(result_file_path, 'w') as result_file:
                    json.dump(job['result'], result_file)
                self.tpool.job_status[job["job_id"]] = result_file_path
            else:
                if self.tpool.event.is_set():
                    break
