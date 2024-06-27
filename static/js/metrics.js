document.getElementById('assessment-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const datasetURL = document.getElementById('datasetURL').value;
    const datasetURL2 = document.getElementById('datasetURL2').value;
    const loadingDiv = document.getElementById('loading');
    const wrapperResults = document.getElementById('wrapper-results');
    const secondResult = document.getElementById('second-result');

    loadingDiv.style.display = 'flex'; // Show loading spinner
    fetch('/run_metrics', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: datasetURL }),
    })
    .then(response => response.json())
    .then(data => {

        

        displayResults(data);
        
    })
    .catch(error => {
        console.error('Error:', error);
    })
    .finally(() => {
        loadingDiv.style.display = 'none'; // Hide loading spinner
    });

    
    if(datasetURL2){
        loadingDiv.style.display = 'flex'; // Show loading spinner
        fetch('/run_metrics', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: datasetURL2 }),
        })
        .then(response => response.json())
        .then(data => {

            displayResultsSecond(data);

            wrapperResults.style.display = 'flex';
            secondResult.hidden = false;
        })
        .catch(error => {
            console.error('Error:', error);
        })
        .finally(() => {
            loadingDiv.style.display = 'none'; // Hide loading spinner
        });
    }
    
});

function displayResults(results) {

    for (const [metric, result] of Object.entries(results)) {
        if(metric === 'summary_grade'){
            console.log(result)
            document.getElementById('summary_grade').textContent = `Overall Score: ${result.text} (${result.number})`;
            continue;
        }
        if(metric === 'additional_info'){
            console.log(result)
            document.getElementById('provided_url').textContent = `${result.provided_url}`;
            document.getElementById('metadata_preview').textContent = `Metadata: ${result.metadata}`;
            document.getElementById('metadata_preview').hidden = false;
            continue;
        }
        console.log(metric, result);
        let grade_id = `grade_${result.subfix_element}`;
        console.log(grade_id)
        let message_id = `message_${result.subfix_element}`;
        console.log(message_id)
        document.getElementById(grade_id).textContent = `Score: ${result.grade}`;
        document.getElementById(message_id).textContent = `Additional Info: ${result.message}`;
    }


}

function displayResultsSecond(results) {

    for (const [metric, result] of Object.entries(results)) {
        if(metric === 'summary_grade'){
            console.log(result)
            document.getElementById('summary_grade_2').textContent = `Overall Score: ${result.text} (${result.number})`;
            continue;
        }
        if(metric === 'additional_info'){
            console.log(result)
            document.getElementById('provided_url_2').textContent = `${result.provided_url}`;
            document.getElementById('metadata_preview_2').textContent = `Metadata: ${result.metadata}`;
            document.getElementById('metadata_preview_2').hidden = false;
            continue;
        }
        console.log(metric, result);
        let grade_id = `grade_2_${result.subfix_element}`;
        console.log(grade_id)
        let message_id = `message_2_${result.subfix_element}`;
        console.log(message_id)
        document.getElementById(grade_id).textContent = `Score: ${result.grade}`;
        document.getElementById(message_id).textContent = `Additional Info: ${result.message}`;
    }


}