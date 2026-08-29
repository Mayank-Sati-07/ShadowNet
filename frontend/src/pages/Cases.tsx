import { useEffect, useMemo, useState } from "react";

import { getCaseEvidence, getCases, type CaseEvidenceItem, type CaseItem } from "../api/cases";

const FILTERS = ["All", "High", "Medium", "Active", "Monitoring"];

export default function Cases() {
  const [cases, setCases] = useState<CaseItem[]>([]);
  const [filter, setFilter] = useState("All");
  const [selectedCaseId, setSelectedCaseId] = useState<string | null>(null);
  const [caseEvidence, setCaseEvidence] = useState<CaseEvidenceItem[]>([]);
  const [loadingEvidence, setLoadingEvidence] = useState(false);

  useEffect(() => {
    getCases()
      .then((data) => {
        setCases(data.cases);
        if (!selectedCaseId && data.cases.length) {
          setSelectedCaseId(data.cases[0].id);
        }
      })
      .catch((error) => console.error("Cases error:", error));
  }, []);

  const visibleCases = useMemo(
    () =>
      filter === "All"
        ? cases
        : cases.filter((item) => item.priority === filter || item.status === filter),
    [cases, filter]
  );

  useEffect(() => {
    if (!selectedCaseId) {
      setCaseEvidence([]);
      return;
    }

    setLoadingEvidence(true);
    getCaseEvidence(selectedCaseId)
      .then((data) => setCaseEvidence(data.evidence))
      .catch((error) => {
        console.error("Case evidence error:", error);
        setCaseEvidence([]);
      })
      .finally(() => setLoadingEvidence(false));
  }, [selectedCaseId]);

  const selectedCase =
    cases.find((item) => item.id === selectedCaseId) ?? visibleCases[0] ?? null;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Cases</h1>
        <p className="text-sm text-slate-500">Active investigations and case tracking.</p>
      </div>

      <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-4">
        <div className="flex flex-wrap gap-2">
          {FILTERS.map((item) => (
            <button
              key={item}
              onClick={() => setFilter(item)}
              className={`rounded-full px-3 py-1.5 text-xs transition ${
                filter === item
                  ? "bg-blue-600 text-white"
                  : "border border-slate-700 bg-slate-950 text-slate-300 hover:border-slate-500"
              }`}
            >
              {item}
            </button>
          ))}
        </div>
      </div>

      <div className="grid gap-5 xl:grid-cols-[1.25fr_0.75fr]">
        <div className="grid gap-5 md:grid-cols-2">
          {visibleCases.map((item) => {
            const isSelected = selectedCase?.id === item.id;

            return (
              <button
                key={item.id}
                type="button"
                onClick={() => setSelectedCaseId(item.id)}
                className={`rounded-xl border p-5 text-left transition ${
                  isSelected
                    ? "border-blue-500 bg-[#111a2d] shadow-lg shadow-blue-950/20"
                    : "border-slate-800 bg-[#0c1220] hover:border-slate-700"
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-500">{item.id}</p>
                    <h3 className="mt-2 text-lg font-semibold text-white">{item.title}</h3>
                  </div>
                  <span
                    className={`rounded-full px-2 py-1 text-[10px] font-medium ${
                      item.priority === "High"
                        ? "bg-red-500/10 text-red-400"
                        : item.priority === "Medium"
                          ? "bg-yellow-500/10 text-yellow-300"
                          : "bg-slate-700 text-slate-300"
                    }`}
                  >
                    {item.priority}
                  </span>
                </div>

                <div className="mt-4 flex items-center justify-between text-sm text-slate-400">
                  <span>{item.status}</span>
                  <span>Risk {item.risk_score}</span>
                </div>

                <div className="mt-5 grid grid-cols-2 gap-3 text-sm">
                  <Metric label="Evidence" value={String(item.evidence_count)} />
                  <Metric label="Owner" value={item.owner.split(" ")[0]} />
                </div>
              </button>
            );
          })}
        </div>

        <aside className="rounded-xl border border-slate-800 bg-[#0c1220] p-5">
          {selectedCase ? (
            <>
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-xs uppercase tracking-wide text-slate-500">Case report</p>
                  <h2 className="mt-2 text-xl font-semibold text-white">{selectedCase.title}</h2>
                </div>
                <span
                  className={`rounded-full px-2 py-1 text-[10px] font-medium ${
                    selectedCase.priority === "High"
                      ? "bg-red-500/10 text-red-400"
                      : selectedCase.priority === "Medium"
                        ? "bg-yellow-500/10 text-yellow-300"
                        : "bg-slate-700 text-slate-300"
                  }`}
                >
                  {selectedCase.priority}
                </span>
              </div>

              <div className="mt-5 grid grid-cols-3 gap-3 text-sm">
                <Metric label="Status" value={selectedCase.status} />
                <Metric label="Risk" value={String(selectedCase.risk_score)} />
                <Metric label="Links" value={String(selectedCase.evidence_count)} />
              </div>

              <div className="mt-6">
                <h3 className="text-sm font-medium uppercase tracking-wide text-slate-400">
                  Evidence trail
                </h3>

                {loadingEvidence ? (
                  <div className="mt-3 rounded-lg border border-slate-800 bg-slate-950/50 p-4 text-sm text-slate-400">
                    Loading evidence...
                  </div>
                ) : caseEvidence.length ? (
                  <div className="mt-3 space-y-3">
                    {caseEvidence.map((item, index) => (
                      <div
                        key={`${item.title}-${index}`}
                        className="rounded-lg border border-slate-800 bg-slate-950/40 p-3"
                      >
                        <div className="flex items-center justify-between gap-3">
                          <p className="text-sm font-medium text-white">{item.title}</p>
                          <span className="rounded-full bg-blue-500/10 px-2 py-1 text-[10px] text-blue-300">
                            {item.type}
                          </span>
                        </div>
                        <p className="mt-2 text-xs text-slate-400">
                          {item.summary ?? "Linked network activity"}
                        </p>
                        <div className="mt-3 flex items-center justify-between text-[10px] uppercase tracking-wide text-slate-500">
                          <span>Confidence</span>
                          <span>{Math.round((item.confidence ?? 0) * 100)}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="mt-3 rounded-lg border border-dashed border-slate-700 bg-slate-950/40 p-4 text-sm text-slate-400">
                    No direct evidence found for this case.
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="rounded-lg border border-dashed border-slate-700 bg-slate-950/40 p-6 text-sm text-slate-400">
              Select a case to inspect the live evidence trail.
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-950/40 p-3">
      <p className="text-[10px] uppercase tracking-wide text-slate-500">{label}</p>
      <p className="mt-2 text-sm font-medium text-white">{value}</p>
    </div>
  );
}
