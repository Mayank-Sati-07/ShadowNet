import {
  useEffect,
  useState,
} from "react";

import { api } from "../api/client";


interface Transaction {
  transaction_id: string;
  amount: number;
  timestamp: string;
  is_anomaly: boolean;
  anomaly_score: number | null;
}


export default function Transactions() {

  const [
    transactions,
    setTransactions,
  ] = useState<Transaction[]>([]);


  useEffect(() => {

    api
      .get("/transactions?limit=200")
      .then((response) => {
        setTransactions(
          response.data.transactions
        );
      })
      .catch(console.error);

  }, []);


  return (
    <div className="space-y-6">

      <div>

        <h1 className="text-2xl font-bold text-white">
          Transactions
        </h1>

        <p className="text-sm text-slate-500">
          Financial activity across the network
        </p>

      </div>


      <div className="
        overflow-hidden
        rounded-xl
        border border-slate-800
        bg-[#0c1220]
      ">

        <table className="w-full">

          <thead className="border-b border-slate-800">

            <tr className="text-left text-xs uppercase text-slate-600">

              <th className="px-6 py-4">
                Transaction
              </th>

              <th className="px-6 py-4">
                Amount
              </th>

              <th className="px-6 py-4">
                Timestamp
              </th>

              <th className="px-6 py-4">
                Status
              </th>

              <th className="px-6 py-4">
                Score
              </th>

            </tr>

          </thead>


          <tbody>

            {transactions.map((tx) => (

              <tr
                key={tx.transaction_id}
                className="border-b border-slate-800"
              >

                <td className="px-6 py-4 font-mono text-xs text-slate-300">
                  {tx.transaction_id}
                </td>

                <td className="px-6 py-4 text-sm text-white">
                  ₹{tx.amount}
                </td>

                <td className="px-6 py-4 text-xs text-slate-500">
                  {tx.timestamp}
                </td>

                <td className="px-6 py-4">

                  {tx.is_anomaly ? (

                    <span className="rounded-full bg-red-500/10 px-3 py-1 text-xs text-red-400">
                      Suspicious
                    </span>

                  ) : (

                    <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs text-emerald-400">
                      Normal
                    </span>

                  )}

                </td>

                <td className="px-6 py-4 font-mono text-xs text-slate-400">
                  {tx.anomaly_score?.toFixed(4) || "—"}
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}