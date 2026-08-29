import {
  useEffect,
  useState,
} from "react";

import {
  AlertTriangle,
  User,
  ShieldCheck,
} from "lucide-react";

import {
  getPersonNetwork,
  getPersonAnomalies,
} from "../api/persons";

import type {
  PersonNetwork,
  PersonAnomaly,
} from "../types/person";

import NetworkGraph from "../components/network/NetworkGraph";
import PersonMetrics from "../components/person/PersonMetrics";


interface Props {
  personId?: string;
}


export default function PersonInvestigation({
  personId,
}: Props) {

  const [network, setNetwork] =
    useState<PersonNetwork | null>(null);

  const [anomalies, setAnomalies] =
    useState<PersonAnomaly[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);


  useEffect(() => {
  if (!personId) {
    setLoading(false);
    setError("No person selected.");
    return;
  }

  const id = personId;

  async function load() {
    try {
      setLoading(true);
      setError(null);

      const [networkData, anomalyData] = await Promise.all([
        getPersonNetwork(id),
        getPersonAnomalies(id),
      ]);

      setNetwork(networkData);
      setAnomalies(anomalyData.anomalies);
    } catch (err) {
      console.error("Person investigation error:", err);
      setError("Unable to load person investigation.");
    } finally {
      setLoading(false);
    }
  }

  load();
}, [personId]);


  if (loading) {

    return (
      <div className="flex h-96 items-center justify-center text-slate-500">
        Loading investigation...
      </div>
    );

  }


  if (error || !network) {

    return (
      <div className="
        rounded-xl
        border border-red-900/50
        bg-red-950/20
        p-8
        text-center
      ">

        <AlertTriangle
          className="mx-auto text-red-400"
          size={32}
        />

        <p className="mt-4 text-red-300">
          {error || "Person not found"}
        </p>

      </div>
    );

  }


  return (
    <div className="space-y-6">

      {/* Person header */}

      <div className="
        rounded-xl
        border border-slate-800
        bg-[#0c1220]
        p-6
      ">

        <div className="flex items-center justify-between">

          <div className="flex items-center gap-4">

            <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">

              <User size={26} />

            </div>

            <div>

              <h1 className="text-xl font-bold text-white">

                {network.name ||
                  network.person_id}

              </h1>

              <p className="mt-1 font-mono text-xs text-slate-500">

                {network.person_id}

              </p>

            </div>

          </div>


          <div className="flex items-center gap-2 rounded-full bg-emerald-500/10 px-4 py-2 text-xs text-emerald-400">

            <ShieldCheck size={15} />

            Entity identified

          </div>

        </div>

      </div>


      {/* Metrics */}

      <PersonMetrics
        network={network}
      />


      {/* Graph */}

      <div>

        <div className="mb-4">

          <h2 className="text-lg font-semibold text-white">
            Network Analysis
          </h2>

          <p className="text-sm text-slate-500">
            Direct connections and relationship intelligence
          </p>

        </div>

        <NetworkGraph
          network={network}
        />

      </div>


      {/* Anomalies */}

      <div className="
        rounded-xl
        border border-slate-800
        bg-[#0c1220]
        p-6
      ">

        <div className="flex items-center justify-between">

          <div>

            <h2 className="font-semibold text-white">
              Suspicious Activity
            </h2>

            <p className="text-xs text-slate-500">
              Transactions flagged by anomaly detection
            </p>

          </div>

          <div className="
            rounded-full
            bg-red-500/10
            px-3
            py-1
            text-xs
            text-red-400
          ">

            {anomalies.length} alerts

          </div>

        </div>


        <div className="mt-5 space-y-3">

          {anomalies.length === 0 ? (

            <p className="py-6 text-center text-sm text-slate-600">
              No anomalies detected.
            </p>

          ) : (

            anomalies.map((anomaly) => (

              <div
                key={anomaly.transaction_id}
                className="
                  flex
                  items-center
                  justify-between
                  rounded-lg
                  border border-slate-800
                  bg-slate-900/50
                  p-4
                "
              >

                <div className="flex items-center gap-3">

                  <AlertTriangle
                    size={18}
                    className="text-red-400"
                  />

                  <div>

                    <p className="font-mono text-sm text-white">
                      {anomaly.transaction_id}
                    </p>

                    <p className="text-xs text-slate-500">
                      {anomaly.timestamp || "Unknown time"}
                    </p>

                  </div>

                </div>


                <div className="text-right">

                  <p className="font-semibold text-white">
                    ₹{anomaly.amount ?? "—"}
                  </p>

                  <p className="text-xs text-red-400">
                    Score:{" "}
                    {anomaly.anomaly_score?.toFixed(3) ??
                      "—"}
                  </p>

                </div>

              </div>

            ))

          )}

        </div>

      </div>

    </div>
  );
}