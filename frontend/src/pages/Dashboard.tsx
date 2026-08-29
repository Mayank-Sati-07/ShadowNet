import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  getNetworkStats,
  getTopPersons,
  type NetworkPerson,
  type NetworkStatsResponse,
} from "../api/network";

export default function Dashboard() {
  const navigate = useNavigate();

  const [stats, setStats] = useState<NetworkStatsResponse | null>(null);
  const [topPersons, setTopPersons] = useState<NetworkPerson[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const network = await getNetworkStats();
        const top = await getTopPersons("pagerank", 10);

        setStats(network);
        setTopPersons(top.persons ?? []);
      } catch (err) {
        console.error("Dashboard error:", err);
        setError("Unable to load CNAS backend");
      }
    }

    void loadDashboard();
  }, []);

if (error) {
    return (
        <div className="p-10">
            <div className="rounded-xl border border-red-300 bg-red-50 p-6 text-red-700">
                <h2 className="text-xl font-bold">
                    CNAS Backend Error
                </h2>

                <p className="mt-2">
                    {error}
                </p>

                <p className="mt-2 text-sm">
                    Make sure the FastAPI backend is running.
                </p>
            </div>
        </div>
    );
}

if (!stats) {
    return (
        <div className="flex min-h-screen items-center justify-center">
            <div className="text-xl font-semibold">
                Loading CNAS...
            </div>
        </div>
    );
}

return (
    <div className="min-h-screen bg-gray-50 p-6">

        {/* Header */}

        <div>
            <h1 className="text-3xl font-bold text-gray-900">
                CNAS Command Center
            </h1>

            <p className="mt-2 text-gray-500">
                Criminal Network Intelligence Platform
            </p>
        </div>


        {/* Statistics */}

        <div className="mt-8 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">

            <StatCard
                title="Total Nodes"
                value={stats.total_nodes}
            />

            <StatCard
                title="Persons"
                value={stats.entities?.Person}
            />

            <StatCard
                title="FIRs"
                value={stats.entities?.FIR}
            />

            <StatCard
                title="Transactions"
                value={stats.entities?.Transaction}
            />

        </div>


        {/* Top Actors */}

        <div className="mt-10">

            <div className="mb-4 flex items-center justify-between">

                <div>
                    <h2 className="text-xl font-bold text-gray-900">
                        Top Network Actors
                    </h2>

                    <p className="text-sm text-gray-500">
                        Ranked by PageRank
                    </p>
                </div>

                <button
                    onClick={() => navigate("/network")}
                    className="rounded-lg bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
                >
                    Open Network
                </button>

            </div>


            <div className="overflow-hidden rounded-xl border bg-white">

                <table className="w-full">

                    <thead className="bg-gray-100">

                        <tr className="border-b">

                            <th className="p-3 text-left">
                                Person
                            </th>

                            <th className="p-3 text-left">
                                Degree
                            </th>

                            <th className="p-3 text-left">
                                PageRank
                            </th>

                            <th className="p-3 text-left">
                                Community
                            </th>

                        </tr>

                    </thead>


                    <tbody>

                        {topPersons.length === 0 ? (

                            <tr>

                                <td
                                    colSpan={4}
                                    className="p-6 text-center text-gray-500"
                                >
                                    No persons found.
                                </td>

                            </tr>

                        ) : (

                            topPersons.map((person) => (

                                <tr
                                    key={person.person_id}
                                    onClick={() =>
                                        navigate(
                                            `/persons/${person.person_id}`
                                        )
                                    }
                                    className="cursor-pointer border-b transition hover:bg-gray-50"
                                >

                                    <td className="p-3 font-medium">
                                        {person.person_id}
                                    </td>

                                    <td className="p-3">
                                        {person.degree ?? 0}
                                    </td>

                                    <td className="p-3">
                                        {typeof person.pagerank === "number"
                                            ? person.pagerank.toFixed(6)
                                            : "0.000000"}
                                    </td>

                                    <td className="p-3">
                                        {person.community_id ?? "N/A"}
                                    </td>

                                </tr>

                            ))

                        )}

                    </tbody>

                </table>

            </div>

        </div>

    </div>
);
}

function StatCard({ title, value }: { title: string; value?: number | string | null }) {
  return (
    <div className="rounded-xl border bg-white p-5 shadow-sm">
      <p className="text-sm text-gray-500">{title}</p>

      <h2 className="mt-2 text-3xl font-bold text-gray-900">{value ?? 0}</h2>
    </div>
  );
}
