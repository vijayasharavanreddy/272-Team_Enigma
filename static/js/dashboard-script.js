
document.addEventListener('DOMContentLoaded', () => {
    fetch('/department_histogram')
        .then(response => response.json())
        .then(data => createBarChart('departmentHistogram', data))
        .catch(error => console.error('Error loading department histogram:', error));

    fetch('/salary_ranges_pie_chart')
        .then(response => response.json())
        .then(data => createPieChart('salaryRangesPieChart', data))
        .catch(error => console.error('Error loading salary ranges pie chart:', error));
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
