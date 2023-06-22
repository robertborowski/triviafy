$(document).ready(function() {
  // ----------------------------- multipl progress bars start -----------------------------
  var chartContentColor = "rgb(0, 0, 0, 0.60)";

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
  // ----------------------------- multipl progress bars start -----------------------------
});