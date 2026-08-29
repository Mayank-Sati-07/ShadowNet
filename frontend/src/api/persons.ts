import { api } from "./client";

import type {
  Person,
  PersonListResponse,
  PersonNetwork,
  PersonAnomaly,
} from "../types/person";


export async function getPersons(
  limit = 100
): Promise<PersonListResponse> {

  const response = await api.get<PersonListResponse>(
    `/persons?limit=${limit}`
  );

  return response.data;
}


export async function getPerson(
  personId: string
): Promise<Person> {

  const response = await api.get<Person>(
    `/persons/${encodeURIComponent(personId)}`
  );

  return response.data;
}


export async function getPersonNetwork(
  personId: string
): Promise<PersonNetwork> {

  const response = await api.get<PersonNetwork>(
    `/persons/${encodeURIComponent(personId)}/network`
  );

  return response.data;
}


export async function getPersonAnomalies(
  personId: string
): Promise<{
  person_id: string;
  count: number;
  anomalies: PersonAnomaly[];
}> {

  const response = await api.get(
    `/persons/${encodeURIComponent(personId)}/anomalies`
  );

  return response.data;
}