const ctxChart = document.getElementById('probChart').getContext('2d');
let chart = new Chart(ctxChart, {
  type: 'bar',
  data: {
    labels: ['Player', 'Dealer'],
    datasets: [{
      label: 'Probabilidade de Vitória',
      data: [0.5, 0.5]
    }]
  }
});

async function updateProbabilities() {
  const probs = await getProbabilities();
  chart.data.datasets[0].data = [probs.player_win, probs.dealer_win];
  chart.update();
}
