document.getElementById('profileForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const form = this;
    const formData = {
        first_name: document.getElementById('first_name').value,
        last_name: document.getElementById('last_name').value,
        birth_date: document.getElementById('birth_date').value,
        gender: document.querySelector('input[name="gender"]:checked').value
    };
    const actionUrl = form.getAttribute('data-action-url');

    fetch(actionUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}' // Include this if you're using CSRF protection
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Handle response here. For example, show a success message
        if (data.success) {
            // alert('Profile updated successfully');
            closeProfileModal(); // Function to close the panel
        } else {
            alert('Error updating profile');
        }
    })
    .catch(error => console.error('Error:', error));
});

function showProfileModal() {
    document.getElementById('profileModal').style.display = 'block';
}

function closeProfileModal() {
    document.getElementById('profileModal').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
        const empNo = document.getElementById("currEmpNo").value; // Replace with the actual emp_no you want to fetch

        fetch(`/get_manager_requests/${empNo}`)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    // There are tasks, render them
                    const taskContainer = document.querySelector('.task-container');
                    const taskList = document.querySelector('.task-list');
                    const noTasks = document.querySelector('.no-tasks');

                    data.forEach(task => {
                        const taskCard = document.createElement('div');
                        taskCard.classList.add('task-card');
                        taskCard.innerHTML = `
                            <input type="hidden" id="taskId" value="${task.id}">
                            <h4>${task.title}</h4>
                            <p>${task.description}</p>
                            <p>Assignee: ${task.assignee}</p>
                            <p>Deadline: ${task.deadline}</p>
                            <button id="doneButton">Done</button>
                        `;
                        const doneButton = taskCard.querySelector('#doneButton');
                        doneButton.addEventListener('click', function() {
                            updateTaskStatus(task.id);
                });
                        taskList.appendChild(taskCard);
                    });

                    taskContainer.style.display = 'block';
                    noTasks.style.display = 'none';
                } else {
                    // No tasks, display "No pending items" message
                    const taskContainer = document.querySelector('.task-container');
                    const noTasks = document.querySelector('.no-tasks');

                    taskContainer.style.display = 'none';
                    noTasks.style.display = 'block';
                }
            })
            .catch(error => console.error('Error fetching data:', error));
    });

function updateTaskStatus(taskId) {
    fetch(`/update_manager_request/${taskId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: 1 }) // Assuming status 1 means "Done"
    })
    .then(response => {
        if (response.ok) {
            console.log('Task status updated successfully');
            reloadTasks(); // Function to reload the tasks
        } else {
            console.error('Failed to update task status');
        }
    })
    .catch(error => console.error('Error:', error));
}

function reloadTasks() {
    const empNo = document.getElementById("currEmpNo").value;
    const taskContainer = document.querySelector('.task-container');
    const taskList = document.querySelector('.task-list');
    const noTasks = document.querySelector('.no-tasks');

    // Clear existing tasks
    taskList.innerHTML = '';

    fetch(`/get_manager_requests/${empNo}`)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                data.forEach(task => {
                    const taskCard = document.createElement('div');
                    taskCard.classList.add('task-card');
                    taskCard.innerHTML = `
                        <h4>${task.title}</h4>
                        <p>${task.description}</p>
                        <p>Assignee: ${task.assignee}</p>
                        <p>Deadline: ${task.deadline}</p>
                        <button id="doneButton">Done</button>
                    `;
                    taskList.appendChild(taskCard);

                    // Add event listener to the "Done" button
                    const doneButton = taskCard.querySelector('#doneButton');
                    doneButton.addEventListener('click', function() {
                        updateTaskStatus(task.id);
                    });
                });

                taskContainer.style.display = 'block';
                noTasks.style.display = 'none';
            } else {
                taskContainer.style.display = 'none';
                noTasks.style.display = 'block';
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}



