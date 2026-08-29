import { api } from "./client";

import type {
  Person,
  PersonListResponse,
  PersonNetwork,
  PersonAnomaly,
} from "../types/person";

function normalizePerson(raw: Partial<Person> & { person_id?: string }): Person {
  const resolvedId = raw.id ?? raw.person_id ?? "unknown";

  return {
    ...raw,
    id: resolvedId,
    name: raw.name ?? raw.person_id ?? "Unknown entity",
  } as Person;
}

export async function getPersons(
  limit = 100
): Promise<PersonListResponse> {
  const response = await api.get<PersonListResponse>(`/persons?limit=${limit}`);
  const persons = (response.data.persons ?? []).map(normalizePerson);

  return {
    ...response.data,
    persons,
  };
}

export async function getPerson(
  personId: string
): Promise<Person> {
  const response = await api.get<Person>(`/persons/${encodeURIComponent(personId)}`);
  return normalizePerson(response.data);
}

export async function getPersonNetwork(
  personId: string
): Promise<PersonNetwork> {
  const response = await api.get<PersonNetwork>(`/persons/${encodeURIComponent(personId)}/network`);
  const network = response.data ?? {
    person_id: personId,
    name: personId,
    degree: 0,
    degree_centrality: null,
    betweenness: null,
    pagerank: null,
    community: null,
    community_size: null,
    connections: [],
  };

  return {
    ...network,
    person_id: network.person_id ?? personId,
    name: network.name ?? personId,
    connections: network.connections ?? [],
  };
}

export async function getPersonAnomalies(
  personId: string
): Promise<{
  person_id: string;
  count: number;
  anomalies: PersonAnomaly[];
}> {
  const response = await api.get<{ person_id: string; count: number; anomalies: PersonAnomaly[] }>(
    `/persons/${encodeURIComponent(personId)}/anomalies`
  );

  return {
    person_id: response.data.person_id ?? personId,
    count: response.data.count ?? 0,
    anomalies: response.data.anomalies ?? [],
  };
}