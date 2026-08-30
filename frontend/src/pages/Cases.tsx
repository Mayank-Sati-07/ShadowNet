import { useEffect, useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
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
    () => filter === "All" ? cases : cases.filter((item) => item.priority === filter || item.status === filter),
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

  const selectedCase = cases.find((item) => item.id === selectedCaseId) ?? visibleCases[0] ?? null;

  return (
    <div className="space-y-8 pb-10">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-[var(--color-foreground)]">Cases</h1>
        <p className="mt-2 text-[var(--color-muted-foreground)]">Active investigations and case tracking.</p>
      </div>

      <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-card)] p-4 shadow-sm">
        <div className="flex flex-wrap gap-2">
          {FILTERS.map((item) => (
            <button
              key={item}
              onClick={() => setFilter(item)}
              className={`rounded-lg px-4 py-2 text-xs font-medium transition-colors duration-300 shadow-sm ${
                filter === item
                  ? "bg-[var(--color-primary)] text-white"
                  : "border border-[var(--color-border)] bg-transparent text-[var(--color-muted-foreground)] hover:border-[var(--color-primary)] hover:text-[var(--color-primary)]"
              }`}
            >
              {item}
            </button>
          ))}
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.3fr_0.7fr]">
        <motion.div className="grid gap-4 md:grid-cols-2 content-start">
          <AnimatePresence mode="popLayout">
            {visibleCases.map((item) => {
              const isSelected = selectedCase?.id === item.id;
              return (
                <motion.button
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.2 }}
                  key={item.id}
                  onClick={() => setSelectedCaseId(item.id)}
                  className={`flex flex-col text-left rounded-xl p-5 transition-all duration-300 border shadow-sm ${
                    isSelected
                      ? "border-[var(--color-primary)] bg-[var(--color-primary)]/5"
                      : "border-[var(--color-border)] bg-[var(--color-card)] hover:border-[var(--color-primary)]/50 hover:shadow-md"
                  }`}
                >
                  <div className="w-full flex items-start justify-between gap-3">
                    <div>
                      <p className="text-xs uppercase tracking-wide text-[var(--color-muted-foreground)]">{item.id}</p>
                      <h3 className="mt-2 text-lg font-semibold text-[var(--color-foreground)]">{item.title}</h3>
                    </div>
                    <span
                      className={`rounded-lg px-2.5 py-1 text-[10px] font-medium border ${
                        item.priority === "High"
                          ? "border-[var(--color-destructive)]/30 bg-[var(--color-destructive)]/10 text-[var(--color-destructive)]"
                          : item.priority === "Medium"
                          ? "border-amber-500/30 bg-amber-500/10 text-amber-600"
                          : "border-[var(--color-border)] bg-[var(--color-muted)] text-[var(--color-muted-foreground)]"
                      }`}
                    >
                      {item.priority}
                    </span>
                  </div>

                  <div className="mt-5 w-full flex items-center justify-between text-sm text-[var(--color-muted-foreground)] border-t border-[var(--color-border)] pt-4">
                    <span>{item.status}</span>
                    <span>Risk: {item.risk_score}</span>
                  </div>

                  <div className="mt-4 grid grid-cols-2 gap-3 text-sm w-full">
                    <Metric label="Evidence" value={String(item.evidence_count)} />
                    <Metric label="Owner" value={String(item.owner).charAt(0)} />
                  </div>
                </motion.button>
              );
            })}
          </AnimatePresence>
        </motion.div>

        <aside className="rounded-xl border border-[var(--color-border)] bg-[var(--color-card)] p-6 shadow-sm h-fit sticky top-28">
          {selectedCase ? (
            <motion.div
              key={selectedCase.id}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-xs uppercase tracking-wide text-[var(--color-muted-foreground)]">Case Report</p>
                  <h2 className="mt-2 text-2xl font-bold tracking-tight text-[var(--color-foreground)]">{selectedCase.title}</h2>
                </div>
                <span
                  className={`rounded-lg px-2.5 py-1 text-[10px] font-medium border ${
                    selectedCase.priority === "High"
                      ? "border-[var(--color-destructive)]/30 bg-[var(--color-destructive)]/10 text-[var(--color-destructive)]"
                      : selectedCase.priority === "Medium"
                      ? "border-amber-500/30 bg-amber-500/10 text-amber-600"
                      : "border-[var(--color-border)] bg-[var(--color-muted)] text-[var(--color-muted-foreground)]"
                  }`}
                >
                  {selectedCase.priority}
                </span>
              </div>

              <div className="mt-8 grid grid-cols-3 gap-3 text-sm">
                <Metric label="Status" value={selectedCase.status} />
                <Metric label="Risk" value={String(selectedCase.risk_score)} />
                <Metric label="Links" value={String(selectedCase.evidence_count)} />
              </div>

              <div className="mt-10">
                <h3 className="text-sm font-semibold uppercase tracking-wide text-[var(--color-muted-foreground)] border-b border-[var(--color-border)] pb-2 mb-4">
                  Evidence Trail
                </h3>

                {loadingEvidence ? (
                  <div className="flex justify-center items-center py-10 gap-3 text-[var(--color-muted-foreground)]">
                    <div className="h-4 w-4 rounded-full border-2 border-[var(--color-primary)] border-t-transparent animate-spin" />
                    Loading evidence...
                  </div>
                ) : caseEvidence.length ? (
                  <div className="space-y-4">
                    {caseEvidence.map((item, index) => (
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        key={`${item.title}-${index}`}
                        className="rounded-xl border border-[var(--color-border)] bg-[var(--color-muted)] p-4 shadow-sm"
                      >
                        <div className="flex items-center justify-between gap-3">
                          <p className="text-sm font-medium text-[var(--color-foreground)]">{item.title}</p>
                          <span className="rounded-lg border border-[var(--color-primary)]/30 bg-[var(--color-primary)]/10 px-2 py-1 text-[10px] font-medium text-[var(--color-primary)]">
                            {item.type}
                          </span>
                        </div>
                        <p className="mt-3 text-xs text-[var(--color-muted-foreground)] leading-relaxed">
                          {item.summary ?? "Linked network activity"}
                        </p>
                        <div className="mt-4 flex items-center justify-between text-[10px] uppercase tracking-wide text-[var(--color-muted-foreground)] border-t border-[var(--color-border)] pt-3">
                          <span>Confidence</span>
                          <span className="text-[var(--color-foreground)] font-medium">{Math.round((item.confidence ?? 0) * 100)}%</span>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                ) : (
                  <div className="rounded-xl border border-dashed border-[var(--color-border)] p-8 text-center text-sm text-[var(--color-muted-foreground)]">
                    No direct evidence found for this case.
                  </div>
                )}
              </div>
            </motion.div>
          ) : (
            <div className="flex h-64 items-center justify-center rounded-xl border border-dashed border-[var(--color-border)] p-6 text-sm text-[var(--color-muted-foreground)]">
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
    <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-muted)] p-3 shadow-sm">
      <p className="text-[10px] uppercase tracking-wide text-[var(--color-muted-foreground)]">{label}</p>
      <p className="mt-2 text-sm font-semibold text-[var(--color-foreground)]">{value}</p>
    </div>
  );
}
