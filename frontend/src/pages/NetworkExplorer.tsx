import { useEffect, useState } from "react";

import { getLiveGraphStats } from "../api/intelligence";

interface GraphStats {
  graph_name: string;
  node_count: number;
  relationship_count: number;
  community_count: number;
  top_risk_areas: string[];
}

export default function NetworkExplorer() {
  const [stats, setStats] = useState<GraphStats | null>(null);

  useEffect(() => {
    getLiveGraphStats()
      .then((data) => setStats(data))
      .catch((error) => console.error("Graph stats error:", error));
  }, []);

  if (!stats) {
    return <div className="text-slate-400">Loading network intelligence...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Network Explorer</h1>
        <p className="text-sm text-slate-500">{stats.graph_name}</p>
      </div>

      <div className="grid gap-6 md:grid-cols-4">
        <Panel title="Nodes" value={String(stats.node_count)} detail="Graph entities" />
        <Panel title="Links" value={String(stats.relationship_count)} detail="Relationships" />
        <Panel title="Communities" value={String(stats.community_count)} detail="Active clusters" />
        <Panel title="Risk Areas" value={String(stats.top_risk_areas.length)} detail="Priority domains" />
      </div>

      <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-6">
        <h2 className="text-lg font-semibold text-white">Top risk areas</h2>
        <div className="mt-4 flex flex-wrap gap-3">
          {stats.top_risk_areas.map((area) => (
            <span key={area} className="rounded-full bg-blue-500/10 px-3 py-1 text-xs text-blue-400">
              {area}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

function Panel({ title, value, detail }: { title: string; value: string; detail: string }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-6">
      <p className="text-xs uppercase tracking-wide text-slate-500">{title}</p>
      <h2 className="mt-4 text-3xl font-bold text-white">{value}</h2>
      <p className="mt-2 text-sm text-slate-400">{detail}</p>
    </div>
  );
}
