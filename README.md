Dependencies of Python3, Flask, Flask-RESTful, requests, radon

Dependencies can be installed through the installDependencies.sh script

Rowan Sutton
13330793

Repository used: https://github.com/python/bedevere

This project computes the cyclomatic complexity for a given Python Github repository. A manager node distributes commit SHAs from a Github repository to worker nodes. These worker nodes use the work stealing method, where they request the SHA for a commit whenever they are free to do work and pull the commit themselves for Github.

To start the system, the manager node (manager.py) must be started first either directly ("python3 manager.py") or via the startManager.sh script (which does the same thing). Once the manager is started, it will request the number of nodes that it will use. After this is inputted, the workers can be started (either directly or by the startWorker.sh script). Each worker must be located in a separate directory location to the other workers. In addition, the workerData folder, workerGetCommit.sh and workerInitScript.sh must be in the same directory as the worker.py file for each worker.

When the workers are started, they will poll the manager until the required number of workers are ready. When all workers are ready, the manager starts a timer and the workers will request commits, compute the average cyclomatic complexity for that commit and respond to the manager node with the results. After all commits have been computed, the manager will stop the timer and average the overall cyclomatic complexity across all commits. The manager prints this average cyclomatic complexity and the time taken to compute it.

Measurements for the number of workers against the computation time are available in "Worker numbers vs Time graph.pdf". These measurements were taken for workers on a local machine to the manager. As can be seen, increasing the number of workers reduces the computation time until more than six workers are used. Adding more workers initially gives large benefits, but give diminishing returns for higher worker numbers. Past six workers, the overhead in the worker setup outweighs the benefits from parallelisation and the computation time starts to increase.

On a distributed system, the benefits from using multiple workers would be much larger since computing resources would not be shared across nodes, as is the case with running all nodes locally. In addition, the overhead from node setup would be higher since each worker is located separately. Hence, running this system on a distributed network for different numbers of workers would yield a similarly shaped graph with a sharper drop in computing time initially from independent computing resources and a larger rise in computing time for higher worker numbers due to the increased overhead.
