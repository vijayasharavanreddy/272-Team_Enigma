document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.querySelector('.search-container form');

    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const searchText = searchForm.querySelector('input[name="search"]').value;
        performSearch(searchText);
    });

function performSearch(query) {
    const deptNo = document.getElementById('deptNo').value; // Replace this with the actual department number
    fetch(`/employees_mgr?dept_no=${deptNo}&search=${query}`)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newTableBody = doc.querySelector('tbody');
            const newPagination = doc.querySelector('.pagination');
            document.querySelector('tbody').replaceWith(newTableBody);
            document.querySelector('.pagination').replaceWith(newPagination);
        })
        .catch(error => console.error('Error:', error));
}
});

// Get the modal
var modal = document.getElementById('hireEmployeeModal');

// Function to open the modal
function showModal() {
    modal.style.display = 'block';
}

// Function to close the modal
function closeModal() {
    modal.style.display = 'none';
}

// Close the modal if the user clicks anywhere outside of it
window.onclick = function(event) {
    if (event.target == modal) {
        closeModal();
    }
}

// Add an event listener to the Hire Employee button
document.getElementById('hireEmployeeBtn').addEventListener('click', showModal);

// Handle form submission
document.getElementById('hireEmployeeForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const deptNo = document.getElementById('deptNo').value;
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const hireDate = document.getElementById('hireDate').value;
    const managerNo = document.getElementById('managerId').value;
    const title = document.getElementById('title').value;
    const hireStatus = 0;
    const reqType = "newhire";

    const data = {
        dept_no: deptNo,
        first_name: firstName,
        last_name: lastName,
        hire_date: hireDate,
        manager_no: managerNo,
        title: title,
        hire_status: hireStatus,
        req_type: reqType
    };

    console.log(data);

    fetch('/add_hr_request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Handle success (e.g., close the modal and display a success message)
        alert("Succesfully posted")
        closeModal()
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle errors (e.g., display an error message)
    });
});

function openPromoteModal(empNo, firstName, lastName, hiredate) {
    document.getElementById('promoteEmpNo').value = empNo;
    document.getElementById('promoteFirstName').value = firstName;
    document.getElementById('promoteLastName').value = lastName;
    document.getElementById('promoteHireDate').value = hiredate;
    document.getElementById('promoteEmployeeModal').style.display = 'block';
}

function closePromoteModal() {
    document.getElementById('promoteEmployeeModal').style.display = 'none';
}

function sendPromotionToHR() {
    const empNo = document.getElementById('promoteEmpNo').value;
    var newTitle = document.getElementById('promoteTitle').value;
    const deptNo = document.getElementById('deptNo').value;
    const firstName = document.getElementById('promoteFirstName').value;
    const lastName = document.getElementById('promoteFirstName').value;
    const hireDate = document.getElementById('promoteHireDate').value;
    const managerNo = document.getElementById('promoteManagerId').value;
    const newSalary = document.getElementById('promoteSalary').value;

    const data = {
        dept_no: deptNo,
        first_name: firstName,
        last_name: lastName,
        hire_date: hireDate,
        manager_no: managerNo,
        title: newTitle,
        salary: newSalary,
        req_type: "promote"
    };

    console.log(data);

    // AJAX request to the backend
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/promote_employee", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            if(response.status === 'success') {
                alert("Promotion request sent successfully!");
                // Additional logic to update UI or redirect
            } else {
                alert("Error: " + response.message);
            }
        }
    };
    xhr.send(JSON.stringify(data));

    closePromoteModal();
}

function handleTerminate(firstName, lastName, dept_no) {
    // Confirmation dialog
    if (!confirm(`Are you sure you want to terminate ${firstName} ${lastName}?`)) {
        return; // Stop if the user cancels the action
    }

    const mgr_no = document.getElementById('mgrNo').value;
    // AJAX request to the backend
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/terminate_employee", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            if(response.status === 'success') {
                alert("Termination request sent successfully!");
                // Additional logic to update UI or redirect
            } else {
                alert("Error: " + response.message);
            }
        }
    };
    xhr.send(JSON.stringify({ firstName: firstName, lastName: lastName, dept_no: dept_no, mgr_no: mgr_no }));
}



