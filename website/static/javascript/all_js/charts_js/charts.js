$(document).ready(function() {
  // var chartContentColor = "rgb(0, 0, 0, 0.50)";
  var chartContentColor = "rgb(255, 193, 7, 0.50)";
  var chartBorderWidth = 3;
  // ----------------------------- chart start -----------------------------
  try {
    new Chart("id-chartAnswerChoiceDistribution", {
      type: "bar",
      data: {
        labels: chartAnswerChoiceDistributionLabels,
        datasets: [{
          backgroundColor: chartContentColor,
          data: chartAnswerChoiceDistributionValues,
          borderWidth: chartBorderWidth
        }]
      },
      options: {
        legend: {display: false},
        title: {
          display: true,
          text: chartAnswerChoiceDistributionTitle
        }
      }
    }); 
  } catch (error) {
    // catch_nothing
  }
  // ----------------------------- chart end -----------------------------
  // ----------------------------- chart start -----------------------------
  try {
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
  } catch (error) {
    // catch_nothing
  }
  // ----------------------------- chart end -----------------------------
  // ----------------------------- chart start -----------------------------
  try {
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
  } catch (error) {
    // catch_nothing
  }
  // ----------------------------- chart end -----------------------------
  // ----------------------------- chart start -----------------------------
  try {
    new Chart("id-chartGenderDistribution", {
      type: "bar",
      data: {
        labels: chartGenderDistributionLabels,
        datasets: [{
          backgroundColor: chartContentColor,
          data: chartGenderDistributionValues,
          borderWidth: chartBorderWidth
        }]
      },
      options: {
        legend: {display: false},
        title: {
          display: true,
          text: chartGenderDistributionTitle
        }
      }
    });
  } catch (error) {
    // catch_nothing
  }
  // ----------------------------- chart end -----------------------------
  // ----------------------------- chart start -----------------------------
  try {
    new Chart("id-chartAnnualIncomeDistribution", {
      type: "bar",
      data: {
        labels: chartAnnualIncomeDistributionLabels,
        datasets: [{
          backgroundColor: chartContentColor,
          data: chartAnnualIncomeDistributionValues,
          borderWidth: chartBorderWidth
        }]
      },
      options: {
        legend: {display: false},
        title: {
          display: true,
          text: chartAnnualIncomeDistributionTitle
        }
      }
    });
  } catch (error) {
    // catch_nothing
  }
  // ----------------------------- chart end -----------------------------
});