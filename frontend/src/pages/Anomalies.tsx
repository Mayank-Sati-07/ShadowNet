import {
  useEffect,
  useState,
} from "react";

import {
  AlertTriangle,
  Activity,
} from "lucide-react";

import { api } from "../api/client";


export default function Anomalies() {

  const [
    anomalies,
    setAnomalies,
  ] = useState<any[]>([]);


  useEffect(() => {

    api
      .get("/anomalies?limit=200")
      .then((response) => {
        setAnomalies(
          response.data.anomalies
        );
      })
      .catch(console.error);

  }, []);


  return (
    <div className="space-y-6">

      <div>

        <h1 className="text-2xl font-bold text-white">
          Anomaly Detection
        </h1>

        <p className="text-sm text-slate-500">
          Suspicious financial activity detected by ML
        </p>

      </div>


      <div className="grid gap-4">

        {anomalies.map((anomaly) => (

          <div
            key={anomaly.transaction_id}
            className="
              rounded-xl
              border border-red-900/40
              bg-red-950/10
              p-5
            "
          >

            <div className="flex items-center justify-between">

              <div className="flex items-center gap-4">

                <div className="rounded-lg bg-red-500/10 p-3 text-red-400">
                  <AlertTriangle size={20} />
                </div>

                <div>

                  <p className="font-mono text-sm text-white">
                    {anomaly.transaction_id}
                  </p>

                  <p className="mt-1 text-xs text-slate-500">
                    {anomaly.timestamp}
                  </p>

                </div>

              </div>


              <div className="text-right">

                <p className="text-lg font-bold text-white">
                  ₹{anomaly.amount}
                </p>

                <p className="mt-1 flex items-center gap-1 text-xs text-red-400">

                  <Activity size={13} />

                  Score:
                  {anomaly.anomaly_score?.toFixed(4)}

                </p>

              </div>

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}