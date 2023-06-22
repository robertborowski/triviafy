$(document).ready(function() {
  var chartContentColor = "rgb(0, 0, 0, 0.60)";
  // ----------------------------- chart start -----------------------------
  new Chart("id-chartAnswerDistribution", {
    type: "bar",
    data: {
      labels: chartAnswerDistributionLabels,
      datasets: [{
        backgroundColor: chartContentColor,
        data: chartAnswerDistributionValues
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
        data: chartGenerationDistributionValues
      }]
    },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: chartGenerationDistributionTitle
      }
    }
  });
  // ----------------------------- chart end -----------------------------
});