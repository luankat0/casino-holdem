const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const btnStart = document.getElementById('btnStart');

btnStart.addEventListener('click', async () => {
  const game = await startGame();
  drawGame(game);
  updateProbabilities();
});

function drawCard(x, y, text) {
  ctx.fillStyle = "#fff";
  ctx.fillRect(x, y, 60, 90);
  ctx.fillStyle = "#000";
  ctx.font = "20px Arial";
  ctx.fillText(text, x + 10, y + 50);
}

function drawGame(game) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#006400";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Player
  game.player_cards.forEach((c, i) => drawCard(100 + i * 80, 250, c));

  // Dealer
  game.dealer_cards.forEach((c, i) => drawCard(100 + i * 80, 50, c));

  // Mesa
  game.table_cards.forEach((c, i) => drawCard(300 + i * 80, 150, c));
}
