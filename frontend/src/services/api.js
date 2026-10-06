const API_BASE_URL = "http://127.0.0.1:5000/api";

export async function predictNews(newsText) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ news_text: newsText })
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Failed to classify news article.");
  }
  return data;
}

export async function getDashboardStats() {
  const response = await fetch(`${API_BASE_URL}/dashboard`);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Failed to load dashboard stats.");
  }
  return data;
}

export async function getPredictionHistory(search = "", filter = "all", sort = "newest") {
  const params = new URLSearchParams({ search, filter, sort });
  const response = await fetch(`${API_BASE_URL}/history?${params}`);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Failed to load history.");
  }
  return data;
}

export async function deleteHistoryRecord(id) {
  const response = await fetch(`${API_BASE_URL}/history/${id}`, {
    method: "DELETE"
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Failed to delete record.");
  }
  return data;
}

export async function clearAllHistory() {
  const response = await fetch(`${API_BASE_URL}/history`, {
    method: "DELETE"
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Failed to clear history.");
  }
  return data;
}

export async function getDatasetStats() {
  const response = await fetch(`${API_BASE_URL}/dataset-stats`);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Failed to load dataset statistics.");
  }
  return data;
}

export async function getModelPerformance() {
  const response = await fetch(`${API_BASE_URL}/model-performance`);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Failed to load model performance stats.");
  }
  return data;
}
