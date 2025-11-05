const BASE_URL = "http://127.0.0.1:5000";

async function startGame() {
  const res = await fetch(`${BASE_URL}/start`, { method: "POST" });
  return res.json();
}

async function getProbabilities() {
  const res = await fetch(`${BASE_URL}/probabilities`);
  return res.json();
}
