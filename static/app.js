async function submitForm() {
    const form = document.getElementById('predictionForm');
    const formData = new FormData(form);

    try {
        console.log("Fetching...")
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: formData
        });
        console.log("Fetched")
        const data = await response.json();
        console.log(data)
        if (data.diabetes) {
            document.getElementById('result').innerHTML = `Diabetes Prediction: <span>${data.diabetes}</span>`;
        } else {
            document.getElementById('result').innerHTML = '1Error: Unable to get pred' +
                'iction';
        }
    } catch (error) {
        document.getElementById('result').innerHTML = '2Error: Unable to get prediction';
        console.error(error);
    }
}
