async function fetchDataAndUpdateChart(chart) {
    const response = await fetch('/data');
    const data = await response.json();

    const labels = data.map(d => new Date(d.timestamp).toLocaleTimeString());
    const temps = data.map(d => d.temperature);
    const hums = data.map(d => d.humidity);

    chart.data.labels = labels;
    chart.data.datasets[0].data = temps;
    chart.data.datasets[1].data = hums;
    chart.update();
}

const ctx = document.getElementById('sensorChart').getContext('2d');
const sensorChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Temperature (°C)',
                borderColor: 'red',
                data: [],
            },
            {
                label: 'Humidity (%)',
                borderColor: 'blue',
                data: [],
            }
        ]
    },
    options: {
        scales: {
            y: { beginAtZero: true }
        }
    }
});

setInterval(() => fetchDataAndUpdateChart(sensorChart), 60000); // Update every 1 min
fetchDataAndUpdateChart(sensorChart); // Initial call
