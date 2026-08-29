import { useState } from "react";
import { Search, Brain, Network, FileText, ShieldCheck } from "lucide-react";
import { motion } from "framer-motion";
import { api } from "../api/client";

const containerVariants = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.1 } }
};

const itemVariants = {
  hidden: { opacity: 0, y: 15 },
  show: { opacity: 1, y: 0, transition: { duration: 0.3 } }
};

export default function Investigation() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  async function investigate() {
    if (!question.trim()) return;

    try {
      setLoading(true);
      const response = await api.post("/graph-rag/investigate", { question });
      setResult(response.data);
    } catch (error) {
      console.error(error);
      setResult({
        status: "error",
        answer: "The investigation service is unavailable right now.",
        graph_evidence: [],
        document_evidence: [],
        investigation_evidence: {},
      });
    } finally {
      setLoading(false);
    }
  }

  const graphEvidence = Array.isArray(result?.graph_evidence) ? result.graph_evidence : [];
  const documentEvidence = Array.isArray(result?.document_evidence) ? result.document_evidence : [];
  const investigationEvidence = result?.investigation_evidence ?? {};

  return (
    <div className="mx-auto max-w-6xl space-y-8 pb-10">
      <motion.div initial="hidden" animate="show" variants={itemVariants}>
        <h1 className="text-3xl font-bold tracking-tight text-[var(--color-foreground)]">AI Investigation</h1>
        <p className="mt-2 text-[var(--color-muted-foreground)]">
          Ask CNAS questions about the criminal network and trace the evidence behind the answer.
        </p>
      </motion.div>

      <motion.div 
        variants={itemVariants} 
        initial="hidden" 
        animate="show"
        className="rounded-xl border border-[var(--color-border)] bg-[var(--color-card)] p-6 shadow-sm"
      >
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder={
            "Ask something like:\n'Show connections of SYN_P_0001'\n'Which persons are connected through suspicious transactions?'\n'Find important people in this network'"
          }
          rows={5}
          className="w-full resize-none rounded-xl border border-[var(--color-border)] bg-[var(--color-muted)] p-4 text-sm text-[var(--color-foreground)] outline-none placeholder:text-[var(--color-muted-foreground)] focus:border-[var(--color-primary)] focus:bg-[var(--color-card)] transition-colors duration-300 shadow-inner"
        />

        <button
          onClick={investigate}
          disabled={loading || !question.trim()}
          className="mt-4 flex items-center gap-2 rounded-xl bg-[var(--color-primary)] px-6 py-3 text-sm font-medium text-white transition-all duration-300 hover:bg-blue-600 hover:shadow-[0_4px_14px_rgba(59,130,246,0.3)] disabled:opacity-50 disabled:hover:bg-[var(--color-primary)] disabled:hover:shadow-none shadow-sm"
        >
          {loading ? (
            <div className="h-4 w-4 rounded-full border-2 border-white border-t-transparent animate-spin" />
          ) : (
            <Search size={17} />
          )}
          {loading ? "Investigating network..." : "Run Investigation"}
        </button>
      </motion.div>

      {result && (
        <motion.div 
          variants={containerVariants} 
          initial="hidden" 
          animate="show" 
          className="space-y-6"
        >
          <motion.div variants={itemVariants} className="rounded-xl border border-[var(--color-border)] bg-[var(--color-card)] p-6 shadow-md">
            <div className="flex items-center gap-3 border-b border-[var(--color-border)] pb-4">
              <div className="rounded-lg bg-[var(--color-primary)]/10 p-2 text-[var(--color-primary)] border border-[var(--color-primary)]/20">
                <Brain size={20} />
              </div>
              <h2 className="text-lg font-semibold text-[var(--color-foreground)]">AI Analysis</h2>
            </div>

            <div className="mt-5 flex flex-wrap gap-2">
              <span className={`rounded-lg border px-3 py-1.5 text-xs font-medium uppercase tracking-wide ${result.status === "success" ? "border-emerald-500/30 bg-emerald-50/50 text-emerald-600" : "border-[var(--color-destructive)]/30 bg-[var(--color-destructive)]/10 text-[var(--color-destructive)]"}`}>
                {result.status === "success" ? "Grounded report" : "System warning"}
              </span>
              <span className="rounded-lg border border-[var(--color-border)] bg-[var(--color-muted)] px-3 py-1.5 text-xs font-medium uppercase tracking-wide text-[var(--color-primary)]">
                {graphEvidence.length} graph signals
              </span>
              <span className="rounded-lg border border-[var(--color-border)] bg-[var(--color-muted)] px-3 py-1.5 text-xs font-medium uppercase tracking-wide text-[var(--color-primary)]">
                {documentEvidence.length} document matches
              </span>
            </div>

            <div className="mt-6 rounded-xl border border-[var(--color-border)] bg-[var(--color-muted)] p-5 shadow-sm">
              <p className="whitespace-pre-wrap text-sm leading-relaxed text-[var(--color-foreground)]">{result.answer}</p>
            </div>
          </motion.div>

          <div className="grid gap-6 lg:grid-cols-3">
            <motion.div variants={itemVariants} className="rounded-xl border border-[var(--color-border)] bg-[var(--color-card)] p-6 shadow-sm lg:col-span-2">
              <div className="flex items-center gap-3 border-b border-[var(--color-border)] pb-4 mb-5">
                <Network size={18} className="text-[var(--color-primary)]" />
                <h2 className="text-lg font-semibold text-[var(--color-foreground)]">Graph Evidence</h2>
              </div>

              {graphEvidence.length ? (
                <div className="space-y-4">
                  {graphEvidence.map((item: any, index: number) => (
                    <div key={`${item.type ?? "edge"}-${index}`} className="rounded-xl border border-[var(--color-border)] bg-[var(--color-muted)] p-5 shadow-sm">
                      <div className="flex items-center justify-between gap-3">
                        <p className="text-sm font-medium text-[var(--color-foreground)]">{item.type ?? "Relationship"}</p>
                        {item.data && item.data.length ? (
                          <span className="rounded-lg border border-[var(--color-primary)]/30 bg-[var(--color-primary)]/10 px-2.5 py-1 text-[10px] font-medium text-[var(--color-primary)]">
                            {item.data.length} matches
                          </span>
                        ) : null}
                      </div>
                      <pre className="mt-4 max-h-60 overflow-auto rounded-lg bg-white border border-[var(--color-border)] p-4 text-[11px] leading-relaxed text-[var(--color-muted-foreground)]">
                        {JSON.stringify(item, null, 2)}
                      </pre>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="rounded-xl border border-dashed border-[var(--color-border)] p-8 text-center text-sm text-[var(--color-muted-foreground)]">
                  No graph evidence returned for this query.
                </div>
              )}
            </motion.div>

            <motion.div variants={itemVariants} className="rounded-xl border border-[var(--color-border)] bg-[var(--color-card)] p-6 shadow-sm h-fit sticky top-28">
              <div className="flex items-center gap-3 border-b border-[var(--color-border)] pb-4 mb-5">
                <FileText size={18} className="text-amber-500" />
                <h2 className="text-lg font-semibold text-[var(--color-foreground)]">Document Evidence</h2>
              </div>

              {documentEvidence.length ? (
                <div className="space-y-4">
                  {documentEvidence.map((item: any, index: number) => (
                    <div key={`${item.title ?? "doc"}-${index}`} className="rounded-xl border border-[var(--color-border)] bg-[var(--color-muted)] p-4 shadow-sm">
                      <p className="text-sm font-medium text-[var(--color-foreground)]">{item.title ?? "Document match"}</p>
                      <p className="mt-3 text-xs leading-relaxed text-[var(--color-muted-foreground)]">
                        {item.content ?? item.summary ?? JSON.stringify(item)}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="rounded-xl border border-dashed border-[var(--color-border)] p-6 text-center text-sm text-[var(--color-muted-foreground)]">
                  No document evidence retrieved.
                </div>
              )}
            </motion.div>
          </div>

          {Object.keys(investigationEvidence).length > 0 && (
            <motion.div variants={itemVariants} className="rounded-xl border border-[var(--color-border)] bg-[var(--color-card)] p-6 shadow-sm">
              <div className="flex items-center gap-3 border-b border-[var(--color-border)] pb-4 mb-5">
                <ShieldCheck size={18} className="text-emerald-500" />
                <h2 className="text-lg font-semibold text-[var(--color-foreground)]">Investigation Summary</h2>
              </div>
              <div className="rounded-xl bg-[var(--color-muted)] border border-[var(--color-border)] p-5 text-sm">
                <pre className="overflow-auto whitespace-pre-wrap text-xs leading-relaxed text-[var(--color-muted-foreground)]">
                  {JSON.stringify(investigationEvidence, null, 2)}
                </pre>
              </div>
            </motion.div>
          )}
        </motion.div>
      )}
    </div>
  );
}