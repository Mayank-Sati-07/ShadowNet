import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { api } from "../api/client";

interface Transaction {
  transaction_id: string;
  amount: number;
  timestamp: string;
  is_anomaly: boolean;
  anomaly_score: number | null;
}

const containerVariants = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.05 } }
};

const rowVariants = {
  hidden: { opacity: 0, y: 10 },
  show: { opacity: 1, y: 0 }
};

export default function Transactions() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get("/transactions?limit=200")
      .then((response) => {
        setTransactions(response.data.transactions);
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
              transactions.map((tx) => (
                <motion.tr
                  variants={rowVariants}
                  key={tx.transaction_id}
                  className="transition-colors hover:bg-[var(--color-muted)]"
                >
                  <td className="px-6 py-4 font-mono text-xs text-[var(--color-foreground)]">{tx.transaction_id}</td>
                  <td className="px-6 py-4 text-sm font-medium text-[var(--color-foreground)]">₹{tx.amount.toLocaleString()}</td>
                  <td className="px-6 py-4 text-xs text-[var(--color-muted-foreground)]">{tx.timestamp}</td>
                  <td className="px-6 py-4">
                    {tx.is_anomaly ? (
                      <span className="rounded-lg border border-[var(--color-destructive)]/30 bg-[var(--color-destructive)]/10 px-3 py-1 text-xs font-medium text-[var(--color-destructive)]">
                        Suspicious
                      </span>
                    ) : (
                      <span className="rounded-lg border border-[var(--color-accent)]/30 bg-[var(--color-accent)]/10 px-3 py-1 text-xs font-medium text-[var(--color-accent)]">
                        Normal
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 font-mono text-xs text-[var(--color-muted-foreground)]">
                    {tx.anomaly_score?.toFixed(4) || "—"}
                  </td>
                </motion.tr>
              ))
            )}
          </motion.tbody>
        </table>
      </div>
    </div>
  );
}