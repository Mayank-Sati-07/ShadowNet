import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { getLiveGraphStats } from "../api/intelligence";

interface GraphStats {
  graph_name: string;
  node_count: number;
  relationship_count: number;
  community_count: number;
  top_risk_areas: string[];
}

const containerVariants = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.1 } }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 24 } }
};

export default function NetworkExplorer() {
  const [stats, setStats] = useState<GraphStats | null>(null);

  useEffect(() => {
    getLiveGraphStats()
      .then((data) => setStats(data))
      .catch((error) => console.error("Graph stats error:", error));
  }, []);

  if (!stats) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="text-xl font-semibold text-[var(--color-muted-foreground)] flex items-center gap-3">
          <div className="h-5 w-5 rounded-full border-2 border-[var(--color-primary)] border-t-transparent animate-spin" />
          Loading network intelligence...
        </div>
      </div>
    );
  }

  return (
    <div className="pb-10 space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-[var(--color-foreground)]">Network Explorer</h1>
        <p className="mt-2 text-[var(--color-muted-foreground)]">{stats.graph_name}</p>
      </div>

      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="show"
        className="grid gap-6 md:grid-cols-4"
      >
        <Panel title="Nodes" value={String(stats.node_count)} detail="Graph entities"/>
        <Panel title="Links" value={String(stats.relationship_count)} detail="Relationships"/>
        <Panel title="Communities" value={String(stats.community_count)} detail="Active clusters"/>
        <Panel title="Risk Areas" value={String(stats.top_risk_areas.length)} detail="Priority domains"/>
      </motion.div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.4 }}
        className="rounded-xl border border-[var(--color-border)] bg-[var(--color-card)] p-6 shadow-sm"
      >
        <h2 className="text-lg font-semibold text-[var(--color-foreground)]">Top Risk Areas</h2>
        <div className="mt-6 flex flex-wrap gap-3">
          {stats.top_risk_areas.map((area) => (
            <span key={area} className="border border-[var(--color-destructive)]/30 bg-[var(--color-destructive)]/10 px-4 py-1.5 text-sm font-medium text-[var(--color-destructive)] rounded-lg shadow-sm">
              {area}
            </span>
          ))}
        </div>
      </motion.div>
    </div>
  );
}

function Panel({ title, value, detail }: { title: string; value: string; detail: string }) {
  return (
    <motion.div 
      variants={itemVariants}
      className="rounded-xl border border-[var(--color-border)] bg-[var(--color-card)] p-6 hover:border-[var(--color-primary)]/50 transition-all duration-300 relative overflow-hidden group shadow-sm hover:shadow-md"
    >
      <div className="absolute -right-10 -top-10 h-32 w-32 rounded-full bg-[var(--color-primary)]/5 blur-3xl group-hover:bg-[var(--color-primary)]/15 transition-colors duration-500" />
      <p className="text-xs font-medium uppercase tracking-wider text-[var(--color-muted-foreground)]">{title}</p>
      <h2 className="mt-4 text-3xl font-bold text-[var(--color-foreground)]">{value}</h2>
      <p className="mt-2 text-sm text-[var(--color-muted-foreground)]">{detail}</p>
    </motion.div>
  );
}
