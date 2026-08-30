import { api } from "./client";

export async function getNetworkStats() {
  const response = await api.get("/network/stats");
  return response.data;
}

export async function getTopPersons(metric = "pagerank", limit = 10) {
  const response = await api.get("/network/top-persons", {
    params: {
      metric,
      limit,
    },
  });

  return response.data;
}