// google_form_onSubmit.gs - v3
// Automatically sends responses to AI backend and writes predictions back into Google Sheets
function onFormSubmit(e) {
  try {
    var sheet = e.source.getActiveSheet();
    var row = e.range.getRow();
    var responses = e.values;

    // Map your form fields
    var payload = {
      Age: responses[2],
      HeightCm: responses[4],
      WeightKg: responses[5],
      SystolicBP: responses[6],
      DiastolicBP: responses[7],
      Smoking: responses[8] === 'Yes' ? 1 : 0,
      PastClaims: responses[13] || 0
    };

    // Backend URL
    var backendUrl = 'https://script.google.com/macros/s/AKfycby7W8fkEraUCLCqZYrYkEA_TtyNOuhbtO_0OuGGpxNeBgDqzNlYxpwJz2CjGGEFd31M/exec';
    var options = {
      'method': 'post',
      'contentType': 'application/json',
      'payload': JSON.stringify(payload),
      'muteHttpExceptions': true
    };

    // Send to backend
    var response = UrlFetchApp.fetch(backendUrl, options);
    var result = JSON.parse(response.getContentText());

    // Extract prediction results
    var healthPrediction = result.prediction || '';
    var probability = result.probability || '';
    var insurancePremium = result.estimated_premium || '';

    // Write results to same row (add headers manually if not present)
    var lastCol = sheet.getLastColumn();
    sheet.getRange(row, lastCol + 1).setValue(healthPrediction);
    sheet.getRange(row, lastCol + 2).setValue(probability);
    sheet.getRange(row, lastCol + 3).setValue(insurancePremium);

    Logger.log('✅ Prediction saved for row ' + row);
  } catch (err) {
    Logger.log('❌ Error: ' + err);
  }
}
