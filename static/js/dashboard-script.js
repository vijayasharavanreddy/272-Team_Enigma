
document.addEventListener('DOMContentLoaded', () => {
   showLoader(); // Show loader before starting the fetch
    fetch('/department_histogram')
        .then(response => response.json())
        .then(data => {
            createBarChart('departmentHistogram', data);
        })
        .catch(error => console.error('Error loading department histogram:', error))
    //     .finally(() => hideLoader()); // Hide loader after fetch is done
    //
    // showLoader(); // Show loader again for the next fetch
    fetch('/salary_ranges_pie_chart')
        .then(response => response.json())
        .then(data => {
            createPieChart('salaryRangesPieChart', data);
        })
        .catch(error => console.error('Error loading salary ranges pie chart:', error))
        .finally(() => hideLoader());
});

function createBarChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.department_names,
                        datasets: [{
                            label: 'Number of Employees',
                            data: data.employee_counts,
                            backgroundColor: 'rgba(0, 123, 255, 0.5)',
                            borderColor: 'rgba(0, 123, 255, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            // })
            // .catch(error => console.error('Error loading department histogram:', error));
}

function createPieChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            data: data.data,
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.5)',
                                'rgba(54, 162, 235, 0.5)',
                                'rgba(255, 206, 86, 0.5)'
                            ],
                            borderColor: [
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(255, 206, 86, 1)'
                            ],
                            borderWidth: 1
                        }]
                    }
                });
           // .catch(error => console.error('Error loading salary ranges pie chart:', error));
}

function openApprovalsPanel() {
    var panel = document.getElementById('approvalsPanel');
    panel.style.animation = "slideIn 0.5s forwards";
    // var panel = document.getElementById('approvalsPanel');
    var content = document.getElementById('approvalsContent');
    panel.style.animation = "slideIn 0.5s forwards";

    fetch('/pending_approvals')
    .then(response => response.json())
    .then(data => {
        content.innerHTML = '';
        data.forEach(req => {
            var card = document.createElement('div');
            card.className = 'approval-card ' + req.req_type;
            card.innerHTML = `
                <div class="badge ${req.req_type}">${req.req_type.toUpperCase()}</div>
                <h4>${req.title}</h4>
                <p>Manager No: ${req.manager_no}</p>
                <p>Department: ${req.dept_no}</p>
            `;
            card.onclick = () => openApprovalsModal(req);
            content.appendChild(card);
        });
    })
    .catch(error => console.error('Error loading approvals:', error));
}

function closeApprovalsPanel() {
    var panel = document.getElementById('approvalsPanel');
    panel.style.animation = "slideOut 0.5s forwards";
}


document.querySelector('.navbar #approvalsLink').addEventListener('click', function(e) {
    e.preventDefault();
    openApprovalsPanel();
});

// function openModal(req) {
//     var modal = document.getElementById('approvalModal');
//     var modalContent = document.getElementById('modalContent');
//     modalContent.innerHTML = `<h3>Request Details: ${req.req_type.toUpperCase()}</h3>
//         <p>Manager No: ${req.manager_no}</p>
//         <p>Department: ${req.dept_name}</p>
//         <p>First Name: ${req.first_name}</p>
//         <p>Last Name: ${req.last_name}</p>
//         <p>Title: ${req.title}</p>
//         <div class="form-group">
//             <label for="salary">Salary:</label>
//             <input type="number" id="salary" name="salary">
//         </div>
//         <button class="modal-btn approve" onclick="approveRequest(${req.id})">Approve</button>
//         <button class="modal-btn decline" onclick="declineRequest(${req.id})">Decline</button>
//     `;
//     modal.style.display = 'block';
// }

function openApprovalsModal(req) {
    document.querySelector(".overlay").style.display = "block";
    var modal = document.getElementById('approvalModal');
    var modalDetails = document.getElementById('modalDetails');

    // Populate modal with request details
    modalDetails.innerHTML = `
        <h3>Request Details: ${req.req_type.toUpperCase()}</h3>
        <p>Manager No: ${req.manager_no}</p>
        <p>Department: ${req.dept_no}</p>
        <p>First Name: ${req.first_name}</p>
        <p>Last Name: ${req.last_name}</p>
        <p>Title: ${req.title}</p>
        <input type="hidden" id="approvalReqType" value="${req.req_type}">
        ${req.req_type !== 'terminate' ? `
            <div class="form-group">
                <label for="salary">Salary:</label>
                <input type="number" id="salary" name="salary">
            </div>` : ''
        }
    `;

    modal.style.display = "block";
    modal.style.animation = 'fadeIn 0.5s';
}


function closeModal() {
    var modal = document.getElementById('approvalModal');
    modal.style.display = "none";
    document.querySelector(".overlay").style.display = "none";
}

function showLoader() {
    document.getElementById('loader').style.display = 'flex';
}

function hideLoader() {
    document.getElementById('loader').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    fetch('/approvals_count')
        .then(response => response.json())
        .then(data => {
            const count = data.count; // assuming the server returns a JSON object with a 'count' property
            if (count > 0) {
                document.getElementById('approvalCount').textContent = count;
            } else {
                // Hide the badge if there are no entries
                document.getElementById('approvalCount').style.display = 'none';
            }
        })
        .catch(error => console.error('Error:', error));
});


function approveRequest() {
    // Implement approve logic
    const managerNo = document.querySelector("#modalDetails p:nth-child(2)").textContent.split(": ")[1];
    const deptNo = document.querySelector("#modalDetails p:nth-child(3)").textContent.split(": ")[1];
    const firstName = document.querySelector("#modalDetails p:nth-child(4)").textContent.split(": ")[1];
    const lastName = document.querySelector("#modalDetails p:nth-child(5)").textContent.split(": ")[1];
    const title = document.querySelector("#modalDetails p:nth-child(6)").textContent.split(": ")[1];
    const salary = !!document.getElementById("salary") ? document.getElementById("salary").value : '';
    const req_type = document.getElementById("approvalReqType").value;

    const data = {
        manager_no: managerNo,
        dept_no: deptNo,
        first_name: firstName,
        last_name: lastName,
        title: title,
        salary: salary,
        req_type: req_type
    };

    console.log(data);
    showLoader();
    fetch('/approve_employee', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if(data.message) {
            alert(data.message);
            closeModal();
            openApprovalsPanel();
            fetch('/approvals_count')
            .then(response => response.json())
            .then(data => {
                const count = data.count; // assuming the server returns a JSON object with a 'count' property
                if (count > 0) {
                    document.getElementById('approvalCount').textContent = count;
                } else {
                    // Hide the badge if there are no entries
                    document.getElementById('approvalCount').style.display = 'none';
                }
            }).catch(error => console.error('Error:', error));
            // Additional logic to update the UI
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error))
    .finally(() => hideLoader());
    closeModal();
}

function declineRequest() {
    // Capture necessary data from the modal
    const managerNo = document.querySelector("#modalDetails p:nth-child(2)").textContent.split(": ")[1];
    const deptNo = document.querySelector("#modalDetails p:nth-child(3)").textContent.split(": ")[1];
    const firstName = document.querySelector("#modalDetails p:nth-child(4)").textContent.split(": ")[1];
    const lastName = document.querySelector("#modalDetails p:nth-child(5)").textContent.split(": ")[1];
    const title = document.querySelector("#modalDetails p:nth-child(6)").textContent.split(": ")[1];

    const data = {
        manager_no: managerNo,
        dept_no: deptNo,
        first_name: firstName,
        last_name: lastName,
        title: title,
        hire_status: 2  // Indicating decline
    };

    fetch('/decline_employee', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if(data.message) {
            alert(data.message);
            closeModal();
            openApprovalsPanel(); // Optionally, refresh the approvals panel
             fetch('/approvals_count')
            .then(response => response.json())
            .then(data => {
                const count = data.count; // assuming the server returns a JSON object with a 'count' property
                if (count > 0) {
                    document.getElementById('approvalCount').textContent = count;
                } else {
                    // Hide the badge if there are no entries
                    document.getElementById('approvalCount').style.display = 'none';
                }
            }).catch(error => console.error('Error:', error));
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}


// Close modal when clicking outside of it
window.onclick = function(event) {
    var modal = document.getElementById('approvalModal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
}