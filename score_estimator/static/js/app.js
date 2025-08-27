async function makePrediction() {
  const student = studentSelect.value;
  const assessment = assessmentSelect.value;
  const model = document.getElementById('modelSelect').value; // NEW

  if (!student || !assessment) {
    showAlert('Please select both a student and an assessment.', 'error');
    return;
  }
  showLoading('Calculating prediction...');

  try {
    const resp = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student, assessment, model }) // include model
    });
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || 'Prediction failed');

    predictions[student] = predictions[student] || {};
    predictions[student][assessment] = data.predictedScore;

    displayPredictionResults(data);
    resultsSection.style.display = 'block';
    exportSection.style.display = 'block';
  } catch (err) {
    showAlert('Prediction failed: ' + err.message, 'error');
  } finally {
    hideLoading();
  }
}
