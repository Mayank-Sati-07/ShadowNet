import {
  Activity,
  GitBranch,
  Users,
  TrendingUp,
} from "lucide-react";

import type { PersonNetwork } from "../../types/person";


interface Props {
  network: PersonNetwork;
}


export default function PersonMetrics({
  network,
}: Props) {

  const metrics = [
    {
      label: "Degree",
      value: network.degree ?? "—",
      icon: <GitBranch size={18} />,
    },

    {
      label: "Betweenness",
      value:
        network.betweenness !== null
          ? network.betweenness.toFixed(4)
          : "—",
      icon: <Activity size={18} />,
    },

    {
      label: "PageRank",
      value:
        network.pagerank !== null
          ? network.pagerank.toFixed(6)
          : "—",
      icon: <TrendingUp size={18} />,
    },

    {
      label: "Community",
      value:
        network.community !== null
          ? network.community
          : "—",
      icon: <Users size={18} />,
    },
  ];


  return (
    <div className="grid grid-cols-2 gap-4 xl:grid-cols-4">

      {metrics.map((metric) => (

        <div
          key={metric.label}
          className="
            rounded-xl
            border border-slate-800
            bg-[#0c1220]
            p-5
          "
        >

          <div className="flex items-center gap-2 text-slate-500">

            {metric.icon}

            <span className="text-xs uppercase tracking-wider">
              {metric.label}
            </span>

          </div>

          <p className="mt-3 text-2xl font-bold text-white">
            {metric.value}
          </p>

        </div>

      ))}

    </div>
  );
}