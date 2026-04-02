const API_BASE = "http://127.0.0.1:5001";

const taskList = document.getElementById("taskList");
const taskForm = document.getElementById("taskForm");
const taskTitle = document.getElementById("taskTitle");
const statusEl = document.getElementById("status");

async function loadTasks() {
  const response = await fetch(`${API_BASE}/tasks`);
  const tasks = await response.json();
  taskList.innerHTML = "";

  tasks.forEach((task) => {
    const item = document.createElement("li");
    item.innerHTML = `
      <span>${task.title}</span>
      <button data-id="${task.id}">Delete</button>
    `;
    item.querySelector("button").addEventListener("click", async () => {
      await fetch(`${API_BASE}/tasks/${task.id}`, { method: "DELETE" });
      statusEl.textContent = `Deleted task ${task.id}`;
      loadTasks();
    });
    taskList.appendChild(item);
  });
}

taskForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const title = taskTitle.value.trim();
  if (!title) {
    statusEl.textContent = "Enter a task title.";
    return;
  }

  const response = await fetch(`${API_BASE}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });

  if (!response.ok) {
    statusEl.textContent = "Could not add task.";
    return;
  }

  taskTitle.value = "";
  statusEl.textContent = "Task added.";
  loadTasks();
});

loadTasks();
