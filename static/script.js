async function uploadImage() {
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select an image first.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        displayResults(result);
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while uploading the image.');
    }
}

function displayResults(result) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <h2>Results</h2>
        <p>Skin Tone: ${result.skin_tone}</p>
        <h3>Suggested Colors:</h3>
        <ul>
            ${result.color_suggestions.map(color => `<li>${color}</li>`).join('')}
        </ul>
    `;
}

async function changeSkinTone() {
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select an image first.');
        return;
    }

    const newTone = document.getElementById('newTone').value;
    const formData = new FormData();
    formData.append('file', file);
    formData.append('new_tone', newTone);

    try {
        const response = await fetch('/change-skin-tone', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.blob();
        displayChangedImage(result);
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while changing the skin tone.');
    }
}

function displayChangedImage(imageBlob) {
    const changedImageDiv = document.getElementById('changedImage');
    const img = document.createElement('img');
    img.src = URL.createObjectURL(imageBlob);
    changedImageDiv.innerHTML = '<h2>Changed Image</h2>';
    changedImageDiv.appendChild(img);
}