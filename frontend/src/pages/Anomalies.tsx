import { useEffect, useState } from "react";
import { AlertTriangle, Activity } from "lucide-react";
import { motion, type Variants } from "framer-motion";
import { api } from "../api/client";

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.1 } }
};

const itemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 24 } }
};

export default function Anomalies() {
  const [anomalies, setAnomalies] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/anomalies?limit=200")
      .then((response) => {
        setAnomalies(response.data.anomalies);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="space-y-8 pb-10">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-[var(--color-foreground)]">Anomaly Detection</h1>
        <p className="mt-2 text-[var(--color-muted-foreground)]">Suspicious financial activity detected by ML models</p>
      </div>

      {loading ? (
        <div className="flex min-h-[40vh] items-center justify-center">
          <div className="flex justify-center items-center gap-3 text-[var(--color-muted-foreground)]">
            <div className="h-5 w-5 rounded-full border-2 border-[var(--color-destructive)] border-t-transparent animate-spin" />
            Scanning for anomalies...
          </div>
        </div>
      ) : anomalies.length === 0 ? (
        <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-card)] p-10 text-center text-[var(--color-muted-foreground)] shadow-sm">
          No anomalies detected in the current dataset.
        </div>
      ) : (
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          animate="show"
          className="grid gap-4"
        >
          {anomalies.map((anomaly) => (
            <motion.div
              variants={itemVariants}
              key={anomaly.transaction_id}
              className="rounded-xl border border-[var(--color-destructive)]/30 bg-[var(--color-card)] p-5 shadow-sm transition-all hover:border-[var(--color-destructive)]/60 hover:shadow-md"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-center gap-4">
                  <div className="rounded-lg border border-[var(--color-destructive)]/20 bg-[var(--color-destructive)]/10 p-3 text-[var(--color-destructive)]">
                    <AlertTriangle size={20} />
                  </div>
                  <div>
                    <p className="font-mono text-sm font-semibold text-[var(--color-foreground)]">{anomaly.transaction_id}</p>
                    <p className="mt-1 text-xs text-[var(--color-muted-foreground)]">{anomaly.timestamp}</p>
                  </div>
                </div>

                <div className="text-left sm:text-right">
                  <p className="text-xl font-bold tracking-tight text-[var(--color-foreground)]">₹{anomaly.amount}</p>
                  <div className="mt-1 flex items-center sm:justify-end gap-1.5 text-xs font-medium text-[var(--color-destructive)]">
                    <Activity size={13} />
                    Risk Score: {anomaly.anomaly_score?.toFixed(4)}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}
    </div>
  );
}