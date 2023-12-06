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


