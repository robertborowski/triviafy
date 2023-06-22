$(document).ready(function() {
  // var chartContentColor = "rgb(0, 0, 0, 0.50)";
  var chartContentColor = "rgb(255, 193, 7, 0.50)";
  var chartBorderWidth = 3;
  // ----------------------------- chart start -----------------------------
  new Chart("id-chartAnswerDistribution", {
    type: "bar",
    data: {
      labels: chartAnswerDistributionLabels,
      datasets: [{
        backgroundColor: chartContentColor,
        data: chartAnswerDistributionValues,
        borderWidth: chartBorderWidth
      }]
    },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: chartAnswerDistributionTitle
      }
    }
  });
  // ----------------------------- chart end -----------------------------
  // ----------------------------- chart start -----------------------------
  new Chart("id-chartGenerationDistribution", {
    type: "bar",
    data: {
      labels: chartGenerationDistributionLabels,
      datasets: [{
        backgroundColor: chartContentColor,
        data: chartGenerationDistributionValues,
        borderWidth: chartBorderWidth
      }]
    },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: chartGenerationDistributionTitle,
      }
    }
  });
  // ----------------------------- chart end -----------------------------
  // ----------------------------- chart start -----------------------------
  new Chart("id-chartAgeGroupDistribution", {
    type: "bar",
    data: {
      labels: chartAgeGroupDistributionLabels,
      datasets: [{
        backgroundColor: chartContentColor,
        data: chartAgeGroupDistributionValues,
        borderWidth: chartBorderWidth
      }]
    },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: chartAgeGroupDistributionTitle
      }
    }
  });
  // ----------------------------- chart end -----------------------------
});