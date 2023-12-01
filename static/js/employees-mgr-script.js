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
    // Add your AJAX call here to submit the form data
    // On successful submission, call closeModal()
});

