// company.js

// Function to fetch revenue data and plot the chart
async function fetchAndPlotRevenue(companyId) {
    try {
        // Fetch data from API
        const response = await fetch(`/companies/${companyId}/revenue`);
        if (!response.ok) {
            throw new Error('Failed to fetch revenue data');
        }
        const data = await response.json();

        // Process data: group by date and sum values to handle duplicates
        const revenueMap = new Map();
        data.forEach(item => {
            const dateStr = item.date;
            const value = item.value;
            if (revenueMap.has(dateStr)) {
                revenueMap.set(dateStr, revenueMap.get(dateStr) + value);
            } else {
                revenueMap.set(dateStr, value);
            }
        });

        // Extract sorted dates and values
        const sortedEntries = Array.from(revenueMap.entries()).sort((a, b) => new Date(a[0]) - new Date(b[0]));
        const dates = sortedEntries.map(entry => entry[0]);
        const values = sortedEntries.map(entry => entry[1]);

        // Plotly chart configuration
        const trace = {
            x: dates,
            y: values,
            type: 'scatter',
            mode: 'lines+markers',
            marker: { color: '#667eea' },
            line: { color: '#667eea' }
        };

        const layout = {
            title: 'Company Revenue Over Time',
            xaxis: {
                title: 'Date',
                type: 'date'
            },
            yaxis: {
                title: 'Revenue Value'
            },
            height: 500,
            margin: { t: 50, b: 50, l: 50, r: 50 }
        };

        Plotly.newPlot('revenueChart', [trace], layout);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('revenueChart').innerHTML = '<p class="text-danger text-center">Error loading revenue chart.</p>';
    }
}

// Extract company_id from URL path (assuming URL like /company/<tax_id>)
const pathParts = window.location.pathname.split('/');
const companyId = pathParts[pathParts.length - 1];

// Call the function with companyId
fetchAndPlotRevenue(companyId);
