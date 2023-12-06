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
            alert('Profile updated successfully');
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

function toggleTaskForm() {
    const taskFormContainer = document.getElementById("taskFormContainer");
    const isExpanded = taskFormContainer.style.maxHeight;

    if (isExpanded) {
        taskFormContainer.style.maxHeight = null;
        clearForm();
    } else {
        taskFormContainer.style.maxHeight = taskFormContainer.scrollHeight + "px";
    }
}

function fetchEmployees(deptNo) {
    fetch(`/get_employees?dept_no=${deptNo}`)
        .then(response => response.json())
        .then(employees => {
            const assigneeSelect = document.getElementById('assignee');
            assigneeSelect.innerHTML = ''; // Clear existing options
            employees.forEach(emp => {
                let option = new Option(`${emp.name}`, emp.id);
                assigneeSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    const taskForm = document.getElementById('taskAssignmentForm');

    taskForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(taskForm);
        const data = {
            taskName: formData.get('taskName'),
            description: formData.get('taskDescription'),
            assignee: formData.get('assignee'),
            deadline: formData.get('deadline'),
            managerNo: document.getElementById("currMgrNo").value,  // Assuming you have manager number available in template
            employeeNo: document.getElementById('assignee').value
        };

        fetch('/add_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            alert("added task successfully");
            console.log('Success:', data);
            toggleTaskForm(); // Hide the form after submission
            // You might want to add code here to update the UI with the new task
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});


// Example usage
const curr_dept = document.getElementById("currDeptNo").value;
fetchEmployees(curr_dept); // Replace 'your_dept_no' with the actual department number


function clearForm() {
    document.getElementById("taskAssignmentForm").reset();
}


