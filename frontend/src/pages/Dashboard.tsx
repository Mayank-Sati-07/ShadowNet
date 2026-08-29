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
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);
        setError(null);

        const network = await getNetworkStats();
        const top = await getTopPersons("pagerank", 10);

        setStats(network);
        setTopPersons(top.persons ?? []);
      } catch (err) {
        console.error("Dashboard error:", err);
        setError("Unable to load CNAS backend data.");
      } finally {
        setLoading(false);
      }
    }

    void loadDashboard();
  }, []);

  if (error) {
    return (
      <div className="min-h-screen bg-slate-950 p-6 text-slate-100">
        <div className="mx-auto max-w-2xl rounded-2xl border border-red-500/40 bg-red-950/30 p-8 shadow-xl">
          <h2 className="text-2xl font-bold text-red-300">CNAS Backend Error</h2>
          <p className="mt-3 text-red-100">{error}</p>
          <p className="mt-3 text-sm text-red-200/80">
            Make sure the FastAPI backend is running and the Neo4j data layer is available.
          </p>
        </div>
      </div>
    );
  }

  if (loading || !stats) {
    return (
      <div className="min-h-screen bg-slate-950 p-6 text-slate-100">
        <div className="mx-auto max-w-3xl rounded-2xl border border-slate-800 bg-slate-900/60 p-8">
          <div className="h-3 w-32 animate-pulse rounded-full bg-slate-700" />
          <div className="mt-6 grid gap-4 md:grid-cols-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-28 animate-pulse rounded-xl bg-slate-800" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 p-6 text-slate-100">
      <div className="mx-auto max-w-7xl">
        <div className="flex items-end justify-between gap-4">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-blue-400">Intelligence overview</p>
            <h1 className="mt-2 text-3xl font-bold text-white">CNAS Command Center</h1>
            <p className="mt-2 text-sm text-slate-400">Criminal Network Intelligence Platform</p>
          </div>

          <button
            onClick={() => navigate("/network")}
            className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-500"
          >
            Open Network
          </button>
        </div>

        <div className="mt-8 grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
          <StatCard title="Total Nodes" value={stats.total_nodes} accent="blue" />
          <StatCard title="Persons" value={stats.entities?.Person ?? 0} accent="cyan" />
          <StatCard title="FIRs" value={stats.entities?.FIR ?? 0} accent="violet" />
          <StatCard title="Transactions" value={stats.entities?.Transaction ?? 0} accent="emerald" />
        </div>

        <div className="mt-10 rounded-2xl border border-slate-800 bg-slate-900/60 p-4 shadow-lg shadow-slate-950/30">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-white">Top Network Actors</h2>
              <p className="text-sm text-slate-400">Ranked by PageRank</p>
            </div>
          </div>

          <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-950/40">
            <table className="w-full">
              <thead className="bg-slate-800/80 text-left text-xs uppercase tracking-wider text-slate-400">
                <tr>
                  <th className="p-3">Person</th>
                  <th className="p-3">Degree</th>
                  <th className="p-3">PageRank</th>
                  <th className="p-3">Community</th>
                </tr>
              </thead>

              <tbody>
                {topPersons.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="p-6 text-center text-slate-400">
                      No persons found.
                    </td>
                  </tr>
                ) : (
                  topPersons.map((person, index) => (
                    <tr
                      key={`${person.person_id ?? "person"}-${index}`}
                      onClick={() => navigate(`/persons/${encodeURIComponent(person.person_id ?? "")}`)}
                      className="cursor-pointer border-t border-slate-800 transition hover:bg-slate-800/50"
                    >
                      <td className="p-3 font-medium text-white">
                        {person.name || person.person_id || "Unknown entity"}
                      </td>
                      <td className="p-3 text-slate-300">{person.degree ?? 0}</td>
                      <td className="p-3 text-slate-300">
                        {typeof person.pagerank === "number" ? person.pagerank.toFixed(6) : "0.000000"}
                      </td>
                      <td className="p-3 text-slate-300">{person.community_id ?? "N/A"}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({
  title,
  value,
  accent,
}: {
  title: string;
  value?: number | string | null;
  accent: "blue" | "cyan" | "violet" | "emerald";
}) {
  const accentClasses = {
    blue: "border-blue-500/30 bg-blue-500/10 text-blue-300",
    cyan: "border-cyan-500/30 bg-cyan-500/10 text-cyan-300",
    violet: "border-violet-500/30 bg-violet-500/10 text-violet-300",
    emerald: "border-emerald-500/30 bg-emerald-500/10 text-emerald-300",
  };

  return (
    <div className={`rounded-2xl border p-5 shadow-lg shadow-slate-950/20 ${accentClasses[accent]}`}>
      <p className="text-sm text-slate-300">{title}</p>
      <h2 className="mt-3 text-3xl font-bold text-white">{value ?? 0}</h2>
    </div>
  );
}
