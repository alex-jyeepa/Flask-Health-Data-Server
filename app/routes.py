import json
from flask import request, jsonify
from app import webserver


@webserver.route("/api/post_endpoint", methods=["POST"])
def post_endpoint():
    if request.method == "POST":
        data = request.json
        response = {"message": "Received data successfully", "data": data}
        return jsonify(response)
    else:
        return jsonify({"error": "Method not allowed"}), 405

#fiecare apel de metoda pentru rute este retinut in log
#in functie de job_status aflam daca un job este valid, in rulare sau gata.
#pentru raspuns accesam fisierul cu ruta din job_status
@webserver.route("/api/get_results/<job_id>", methods=["GET"])
def get_response(job_id):
    webserver.logger.info("Received GET for job_id: %s", job_id)
    if int(job_id) in webserver.tasks_runner.job_status:
        if webserver.tasks_runner.job_status[int(job_id)] == "running":
            return jsonify({"status": "running"})
        else:
            result_file_path = f"results/{job_id}"
            with open(result_file_path, "r") as result_file:
                result = json.load(result_file)
            return jsonify({"status": "done", "data": result})
    else:
        return jsonify({"status": "invalid job_id"})

#compunem o lista job_list in functie de job_status
@webserver.route("/api/jobs", methods=["GET"])
def get_jobs():
    webserver.logger.info("Received GET for job list")
    job_list = []
    for job_id in webserver.tasks_runner.job_status:
        job_status = {}
        if webserver.tasks_runner.job_status[job_id] == "running":
            job_status["job_id_" + str(job_id)] = "running"
        else:
            job_status["job_id_" + str(job_id)] = "done"
        job_list.append(job_status)
    return jsonify({"status": "done", "data": job_list})


@webserver.route("/api/num_jobs", methods=["GET"])
def num_jobs():
    webserver.logger.info("Received GET for number of jobs")
    remaining_jobs = 0
    for job_id in webserver.tasks_runner.job_status:
        if webserver.tasks_runner.job_status[job_id] == "running":
            remaining_jobs += 1
    return jsonify({"data": remaining_jobs})

#request-urile au corp aproape identic,
#ele construiesc structura job si o pun in coada de job-uri
#pentru a fi procesata de thread-uri
@webserver.route("/api/states_mean", methods=["POST"])
def states_mean_request():
    webserver.logger.info("Received POST for states_mean")
    if webserver.tasks_runner.event.is_set():
        return jsonify({"job_id": -1, "status": "shutdown"})
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.jobs.put(
        {"job_type": "states_mean", "job_id": webserver.job_counter, "data": data}
    )
    return jsonify({"job_id": webserver.job_counter})


@webserver.route("/api/state_mean", methods=["POST"])
def state_mean_request():
    webserver.logger.info("Received POST for state_mean")
    if webserver.tasks_runner.event.is_set():
        return jsonify({"job_id": -1, "status": "shutdown"})
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.jobs.put(
        {"job_type": "state_mean", "job_id": webserver.job_counter, "data": data}
    )
    return jsonify({"job_id": webserver.job_counter})


@webserver.route("/api/best5", methods=["POST"])
def best5_request():
    webserver.logger.info("Received POST for best5")
    if webserver.tasks_runner.event.is_set():
        return jsonify({"job_id": -1, "status": "shutdown"})
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.jobs.put(
        {"job_type": "best5", "job_id": webserver.job_counter, "data": data}
    )
    return jsonify({"job_id": webserver.job_counter})


@webserver.route("/api/worst5", methods=["POST"])
def worst5_request():
    webserver.logger.info("Received POST for worst5")
    if webserver.tasks_runner.event.is_set():
        return jsonify({"job_id": -1, "status": "shutdown"})
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.jobs.put(
        {"job_type": "worst5", "job_id": webserver.job_counter, "data": data}
    )
    return jsonify({"job_id": webserver.job_counter})


@webserver.route("/api/global_mean", methods=["POST"])
def global_mean_request():
    webserver.logger.info("Received POST for global_mean")
    if webserver.tasks_runner.event.is_set():
        return jsonify({"job_id": -1, "status": "shutdown"})
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.jobs.put(
        {"job_type": "global_mean", "job_id": webserver.job_counter, "data": data}
    )
    return jsonify({"job_id": webserver.job_counter})


@webserver.route("/api/diff_from_mean", methods=["POST"])
def diff_from_mean_request():
    webserver.logger.info("Received POST for diff_from_mean")
    if webserver.tasks_runner.event.is_set():
        return jsonify({"job_id": -1, "status": "shutdown"})
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.jobs.put(
        {"job_type": "diff_from_mean", "job_id": webserver.job_counter, "data": data}
    )
    return jsonify({"job_id": webserver.job_counter})


@webserver.route("/api/state_diff_from_mean", methods=["POST"])
def state_diff_from_mean_request():
    webserver.logger.info("Received POST for state_diff_from_mean")
    if webserver.tasks_runner.event.is_set():
        return jsonify({"job_id": -1, "status": "shutdown"})
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.jobs.put(
        {
            "job_type": "state_diff_from_mean",
            "job_id": webserver.job_counter,
            "data": data,
        }
    )
    return jsonify({"job_id": webserver.job_counter})


@webserver.route("/api/mean_by_category", methods=["POST"])
def mean_by_category_request():
    webserver.logger.info("Received POST for mean_by_category")
    if webserver.tasks_runner.event.is_set():
        return jsonify({"job_id": -1, "status": "shutdown"})
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.jobs.put(
        {"job_type": "mean_by_category", "job_id": webserver.job_counter, "data": data}
    )
    return jsonify({"job_id": webserver.job_counter})


@webserver.route("/api/state_mean_by_category", methods=["POST"])
def state_mean_by_category_request():
    webserver.logger.info("Received POST for state_mean_by_category")
    if webserver.tasks_runner.event.is_set():
        return jsonify({"job_id": -1, "status": "shutdown"})
    data = request.json
    webserver.job_counter += 1
    webserver.tasks_runner.jobs.put(
        {
            "job_type": "state_mean_by_category",
            "job_id": webserver.job_counter,
            "data": data,
        }
    )
    return jsonify({"job_id": webserver.job_counter})

#pentru shutdown apelam join din task_runner, ce 
#foloseste un event ce atentioneaza thread-urile sa se opreasca
#dupa ce s-a golit coada de task-uri
@webserver.route("/api/graceful_shutdown", methods=["POST"])
def graceful_shutdown():
    webserver.logger.info("Received shutdown request")
    webserver.tasks_runner.join()
    return jsonify({"status": "shutdown"})


@webserver.route("/")
@webserver.route("/index")
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg


def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ", ".join(rule.methods)
        routes.append(f'Endpoint: "{rule}" Methods: "{methods}"')
    return routes
