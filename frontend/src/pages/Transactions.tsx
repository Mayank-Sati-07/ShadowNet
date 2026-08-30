import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { api } from "../api/client";

interface Transaction {
  transaction_id: string | null;
  amount: number | string | null;
  timestamp: string | Record<string, unknown> | null;
  is_anomaly: boolean;
  anomaly_score: number | null;
}

const containerVariants = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.05 } },
};

const rowVariants = {
  hidden: { opacity: 0, y: 10 },
  show: { opacity: 1, y: 0 },
};

const formatTimestamp = (value: string | Record<string, unknown> | null): string => {
  if (!value) return "N/A";
  if (typeof value === "string") return value;
  if (typeof value === "object") {
    const candidate = value as Record<string, unknown>;
    const date = candidate["_DateTime__date"] as Record<string, unknown> | undefined;
    const time = candidate["_DateTime__time"] as Record<string, unknown> | undefined;

    const year = date?.["_Date__year"] ?? 0;
    const month = date?.["_Date__month"] ?? 1;
    const day = date?.["_Date__day"] ?? 1;
    const hour = time?.["_Time__hour"] ?? 0;
    const minute = time?.["_Time__minute"] ?? 0;
    const second = time?.["_Time__second"] ?? 0;

    const safeYear = Number(year);
    const safeMonth = Number(month);
    const safeDay = Number(day);
    const safeHour = Number(hour);
    const safeMinute = Number(minute);
    const safeSecond = Number(second);

    const dt = new Date(safeYear, safeMonth - 1, safeDay, safeHour, safeMinute, safeSecond);
    return Number.isNaN(dt.getTime()) ? "N/A" : dt.toISOString();
  }
  return String(value);
};

export default function Transactions() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/transactions?limit=200")
      .then((response) => {
        setTransactions(Array.isArray(response.data.transactions) ? response.data.transactions : []);
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
        <h1 className="text-3xl font-bold tracking-tight text-[var(--color-foreground)]">Transactions</h1>
        <p className="mt-2 text-[var(--color-muted-foreground)]">Financial activity across the network</p>
      </div>

      <div className="overflow-hidden rounded-xl border border-[var(--color-border)] bg-[var(--color-card)] shadow-sm">
        <table className="w-full text-left text-sm">
          <thead className="bg-[var(--color-muted)] text-[var(--color-muted-foreground)] border-b border-[var(--color-border)]">
            <tr className="uppercase tracking-wider text-xs">
              <th className="px-6 py-4 font-medium">Transaction</th>
              <th className="px-6 py-4 font-medium">Amount</th>
              <th className="px-6 py-4 font-medium">Timestamp</th>
              <th className="px-6 py-4 font-medium">Status</th>
              <th className="px-6 py-4 font-medium">Score</th>
            </tr>
          </thead>

          <motion.tbody
            variants={containerVariants}
            initial="hidden"
            animate="show"
            className="divide-y divide-[var(--color-border)]"
          >
            {loading ? (
              <tr>
                <td colSpan={5} className="p-8 text-center text-[var(--color-muted-foreground)]">
                  <div className="flex justify-center items-center gap-3">
                    <div className="h-4 w-4 rounded-full border-2 border-[var(--color-primary)] border-t-transparent animate-spin" />
                    Loading transactions...
                  </div>
                </td>
              </tr>
            ) : transactions.length === 0 ? (
              <tr>
                <td colSpan={5} className="p-8 text-center text-[var(--color-muted-foreground)]">
                  No transactions found.
                </td>
              </tr>
            ) : (
              transactions.map((tx) => {
                const amount = typeof tx.amount === "number" ? tx.amount : Number(tx.amount ?? 0);
                const transactionId = tx.transaction_id || "UNKNOWN_TRANSACTION";
                const score = typeof tx.anomaly_score === "number" ? tx.anomaly_score : null;
                const timestamp = formatTimestamp(tx.timestamp);

                return (
                  <motion.tr
                    variants={rowVariants}
                    key={transactionId}
                    className="transition-colors hover:bg-[var(--color-muted)]"
                  >
                    <td className="px-6 py-4 font-mono text-xs text-[var(--color-foreground)]">{transactionId}</td>
                    <td className="px-6 py-4 text-sm font-medium text-[var(--color-foreground)]">₹{Number.isFinite(amount) ? amount.toLocaleString() : "0"}</td>
                    <td className="px-6 py-4 text-xs text-[var(--color-muted-foreground)]">{timestamp}</td>
                    <td className="px-6 py-4">
                      {tx.is_anomaly ? (
                        <span className="rounded-lg border border-[var(--color-destructive)]/30 bg-[var(--color-destructive)]/10 px-3 py-1 text-xs font-medium text-[var(--color-destructive)]">
                          Suspicious
                        </span>
                      ) : (
                        <span className="rounded-lg border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-600">
                          Normal
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 font-mono text-xs text-[var(--color-muted-foreground)]">
                      {score !== null && score !== undefined ? score.toFixed(4) : "—"}
                    </td>
                  </motion.tr>
                );
              })
            )}
          </motion.tbody>
        </table>
      </div>
    </div>
  );
}