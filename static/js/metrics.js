document.getElementById('uidForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const datasetUID = document.getElementById('datasetUID').value;
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');

    // Show loading spinner and hide results
    loadingDiv.style.display = 'flex';
    resultsDiv.style.display = 'none';

    fetch('/run_metrics', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ uid: datasetUID }),
    })
    .then(response => response.json())
    .then(data => {
        displayResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
    })
    .finally(() => {
        // Hide loading spinner
        loadingDiv.style.display = 'none';
    });
});

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    for (const [metric, result] of Object.entries(results)) {
        const resultItem = document.createElement('div');
        resultItem.className = 'result-item';

        const metricName = document.createElement('h3');
        metricName.className = 'metric-name';
        metricName.textContent = formatMetricName(metric);
        resultItem.appendChild(metricName);

        const grade = document.createElement('div');
        grade.className = 'grade';
        grade.textContent = `Grade: ${result.grade}`;
        resultItem.appendChild(grade);

        if (metric === 'financial_standards_applicable') {
            const possibleStandards = document.createElement('div');
            possibleStandards.className = 'possible-standards';
            possibleStandards.textContent = `Possible Standards: ${result.possible_standards}`;
            resultItem.appendChild(possibleStandards);

            const adherence = document.createElement('div');
            adherence.className = 'adherence';
            adherence.textContent = `Adherence: ${result.adherence}`;
            resultItem.appendChild(adherence);
        }else if (metric === 'summary'){
            continue;
        } else {
            const message = document.createElement('div');
            message.className = 'message';
            message.textContent = `Reason: ${result.message}`;
            
            const source = document.createElement('div');
            source.className = 'message';
            source.textContent = `Evaluated based on: ${result.source_data}`;
            resultItem.appendChild(message);
            resultItem.appendChild(source);
        }

        resultsDiv.appendChild(resultItem);
    }

    resultsDiv.style.display = 'block';
}

function formatMetricName(metric) {
    return metric.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
}
