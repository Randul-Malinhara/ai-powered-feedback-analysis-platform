window.addEventListener('load', async () => {
    try {
        // Fetch feedback data from API endpoint
        const response = await fetch('/api/feedbacks');
        const data = await response.json();
        
        // Populate the feedback table
        const tbody = document.getElementById('feedbackTableBody');
        data.forEach(fb => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${fb.id}</td>
                <td>${fb.name}</td>
                <td>${fb.email}</td>
                <td>${fb.feedback_text}</td>
                <td>${fb.sentiment}</td>
                <td>${fb.created_at}</td>
            `;
            tbody.appendChild(row);
        });
        
        // Prepare sentiment trend data
        let sentimentCount = { Positive: 0, Neutral: 0, Negative: 0 };
        data.forEach(fb => {
            if (fb.sentiment in sentimentCount) {
                sentimentCount[fb.sentiment] += 1;
            }
        });
        const labels = Object.keys(sentimentCount);
        const counts = Object.values(sentimentCount);
        
        const ctx = document.getElementById('sentimentChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Feedback Count',
                    data: counts,
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    } catch (err) {
        console.error('Error fetching feedback data:', err);
    }
});
