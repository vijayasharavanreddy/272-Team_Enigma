document.addEventListener('DOMContentLoaded', function() {
    const empNo = window.location.pathname.split('/').pop();
    document.getElementById('dashboard-button').onclick = function() {
        window.location.href = `/dashboard_emp`;
    };
    showLoader();
    fetch(`/employee_history/${empNo}`)
        .then(response => response.json())
        .then(data => {
            renderChart('salaryChart', 'Salary History', data.salary_history, 'salary');
            renderTimeline('titleTimeline', 'Title History', data.title_history);
            renderTimeline('deptTimeline', 'Department History', data.dept_history);
        })
        .finally(() => hideLoader());
});

function showLoader() {
    document.getElementById('loader').style.display = 'flex';
}

function hideLoader() {
    document.getElementById('loader').style.display = 'none';
}

function renderChart(canvasId, title, data, key) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    const labels = data.map(item => {
        const fromDate = new Date(item.from_date).getFullYear();
        const toDate = new Date(item.to_date).getFullYear();
        return `${fromDate} - ${toDate}`;
    });
    const values = data.map(item => item[key]);

    new Chart(ctx, {
        type: 'line', // or 'bar', depending on your preference
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: values,
                // Other chart configurations...
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
}

function renderTimeline(containerId, title, data) {
    const container = document.getElementById(containerId);
    const timeline = document.createElement('div');
    timeline.className = 'timeline';

    const titleElement = document.createElement('h2');
    titleElement.textContent = title;
    timeline.appendChild(titleElement);

    data.forEach(item => {
        const fromDate = new Date(item.from_date).getFullYear();
        const toDate = new Date(item.to_date).getFullYear();
        const dateRangeText = `${fromDate} - ${toDate}`;

        const entry = document.createElement('div');
        entry.className = 'timeline-entry';

        const dateRange = document.createElement('div');
        dateRange.className = 'timeline-date';
        dateRange.textContent = dateRangeText;
        entry.appendChild(dateRange);

        const content = document.createElement('div');
        content.className = 'timeline-content';
        content.textContent = item.title || item.dept_no;
        entry.appendChild(content);

        timeline.appendChild(entry);
    });

    container.appendChild(timeline);
}
