import { useState } from "react";

import { Search, Brain, Network, FileText, ShieldCheck } from "lucide-react";

import { api } from "../api/client";

export default function Investigation() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  async function investigate() {
    if (!question.trim()) {
      return;
    }

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
    <div className="mx-auto max-w-6xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">AI Investigation</h1>
        <p className="text-sm text-slate-500">
          Ask CNAS questions about the criminal network and trace the evidence behind the answer.
        </p>
      </div>

      <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-6">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder={
            "Ask something like:\n'Show connections of SYN_P_0001'\n'Which persons are connected through suspicious transactions?'\n'Find important people in this network'"
          }
          rows={6}
          className="w-full resize-none rounded-lg border border-slate-800 bg-slate-950 p-4 text-sm text-white outline-none placeholder:text-slate-600 focus:border-blue-500"
        />

        <button
          onClick={investigate}
          disabled={loading}
          className="mt-4 flex items-center gap-2 rounded-lg bg-blue-600 px-5 py-3 text-sm font-medium text-white transition hover:bg-blue-500 disabled:opacity-50"
        >
          <Search size={17} />
          {loading ? "Investigating..." : "Run Investigation"}
        </button>
      </div>

      {result && (
        <div className="space-y-5">
          <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-6">
            <div className="flex items-center gap-2">
              <Brain size={19} className="text-blue-400" />
              <h2 className="font-semibold text-white">AI Analysis</h2>
            </div>

            <div className="mt-4 flex flex-wrap gap-2">
              <span className="rounded-full border border-slate-700 bg-slate-950 px-2 py-1 text-[10px] uppercase tracking-wide text-slate-300">
                {result.status === "success" ? "Grounded report" : "System warning"}
              </span>
              <span className="rounded-full border border-slate-700 bg-slate-950 px-2 py-1 text-[10px] uppercase tracking-wide text-slate-300">
                {graphEvidence.length} graph signals
              </span>
              <span className="rounded-full border border-slate-700 bg-slate-950 px-2 py-1 text-[10px] uppercase tracking-wide text-slate-300">
                {documentEvidence.length} document matches
              </span>
            </div>

            <p className="mt-4 whitespace-pre-wrap text-sm leading-7 text-slate-300">{result.answer}</p>
          </div>

          <div className="grid gap-5 lg:grid-cols-3">
            <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-5 lg:col-span-2">
              <div className="flex items-center gap-2">
                <Network size={18} className="text-blue-400" />
                <h2 className="font-semibold text-white">Graph Evidence</h2>
              </div>

              {graphEvidence.length ? (
                <div className="mt-4 space-y-3">
                  {graphEvidence.map((item: any, index: number) => (
                    <div key={`${item.type ?? "edge"}-${index}`} className="rounded-lg border border-slate-800 bg-slate-950/40 p-4">
                      <div className="flex items-center justify-between gap-3">
                        <p className="text-sm font-medium text-white">{item.type ?? "Relationship"}</p>
                        {item.data && item.data.length ? (
                          <span className="rounded-full bg-blue-500/10 px-2 py-1 text-[10px] text-blue-300">
                            {item.data.length} matches
                          </span>
                        ) : null}
                      </div>
                      <pre className="mt-3 max-h-60 overflow-auto rounded-md bg-slate-950 p-3 text-[11px] leading-5 text-slate-400">
                        {JSON.stringify(item, null, 2)}
                      </pre>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="mt-4 rounded-lg border border-dashed border-slate-700 bg-slate-950/40 p-5 text-sm text-slate-400">
                  No graph evidence returned for this query.
                </div>
              )}
            </div>

            <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-5">
              <div className="flex items-center gap-2">
                <FileText size={18} className="text-blue-400" />
                <h2 className="font-semibold text-white">Document Evidence</h2>
              </div>

              {documentEvidence.length ? (
                <div className="mt-4 space-y-3">
                  {documentEvidence.map((item: any, index: number) => (
                    <div key={`${item.title ?? "doc"}-${index}`} className="rounded-lg border border-slate-800 bg-slate-950/40 p-3">
                      <p className="text-sm font-medium text-white">{item.title ?? "Document match"}</p>
                      <p className="mt-2 text-xs leading-5 text-slate-400">
                        {item.content ?? item.summary ?? JSON.stringify(item)}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="mt-4 rounded-lg border border-dashed border-slate-700 bg-slate-950/40 p-5 text-sm text-slate-400">
                  No document evidence retrieved.
                </div>
              )}
            </div>
          </div>

          {Object.keys(investigationEvidence).length > 0 && (
            <div className="rounded-xl border border-slate-800 bg-[#0c1220] p-5">
              <div className="flex items-center gap-2">
                <ShieldCheck size={18} className="text-emerald-400" />
                <h2 className="font-semibold text-white">Investigation Summary</h2>
              </div>

              <div className="mt-4 rounded-lg bg-slate-950 p-4 text-sm text-slate-300">
                <pre className="overflow-auto whitespace-pre-wrap text-xs leading-6 text-slate-300">
                  {JSON.stringify(investigationEvidence, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}