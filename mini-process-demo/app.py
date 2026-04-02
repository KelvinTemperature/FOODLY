import os
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory


def create_app():
    app = Flask(__name__)
    frontend_dir = Path(__file__).resolve().parent / "frontend"

    tasks = [
        {"id": 1, "title": "Learn the stack", "done": False},
        {"id": 2, "title": "Run the tests", "done": False},
    ]
    next_id = {"value": 3}

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/tasks")
    def list_tasks():
        return jsonify(tasks)

    @app.post("/tasks")
    def create_task():
        payload = request.get_json(silent=True) or {}
        title = str(payload.get("title", "")).strip()
        if not title:
            return jsonify({"message": "title is required"}), 400

        task = {"id": next_id["value"], "title": title, "done": False}
        tasks.append(task)
        next_id["value"] += 1
        return jsonify(task), 201

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id):
        for index, task in enumerate(tasks):
            if task["id"] == task_id:
                deleted = tasks.pop(index)
                return jsonify(deleted)
        return jsonify({"message": "task not found"}), 404

    @app.get("/")
    def frontend_index():
        return send_from_directory(frontend_dir, "index.html")

    @app.get("/<path:filename>")
    def frontend_assets(filename):
        return send_from_directory(frontend_dir, filename)

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, port=port)
