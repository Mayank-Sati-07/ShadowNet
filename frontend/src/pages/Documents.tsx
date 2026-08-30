import { useState } from "react";
import { Upload, CheckCircle, XCircle } from "lucide-react";
import { motion } from "framer-motion";
import { api } from "../api/client";

export default function Documents() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
  const [message, setMessage] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setStatus("idle");
      setMessage("");
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setStatus("uploading");
    setMessage("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post("/documents/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setStatus("success");
      setMessage(`Document "${response.data.filename}" ingested successfully.`);
    } catch (error: any) {
      console.error(error);
      setStatus("error");
      setMessage(error.response?.data?.detail || "Upload failed. Check backend connection.");
    }
  };

  return (
    <div className="mx-auto max-w-3xl space-y-8 pb-10">
      <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
        <h1 className="text-3xl font-bold tracking-tight text-[var(--color-foreground)]">Document Ingestion</h1>
        <p className="mt-2 text-[var(--color-muted-foreground)]">
          Upload unstructured evidence (PDFs, TXT, CSV) to enrich the graph network automatically.
        </p>
      </motion.div>

      <motion.div 
        initial={{ opacity: 0, y: 15 }} 
        animate={{ opacity: 1, y: 0 }} 
        transition={{ delay: 0.1, duration: 0.3 }}
        className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] p-8 shadow-sm"
      >
        <div className="relative flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-[var(--color-border)] bg-[var(--color-muted)] py-16 transition-colors hover:border-[var(--color-primary)]/50 hover:bg-slate-50 group">
          <input
            type="file"
            onChange={handleFileChange}
            className="absolute inset-0 z-50 h-full w-full cursor-pointer opacity-0"
            accept=".txt,.csv,.pdf,.json"
          />

          <div className="rounded-full bg-[var(--color-card)] p-4 shadow-sm border border-[var(--color-border)] group-hover:bg-[var(--color-primary)]/10 group-hover:border-[var(--color-primary)]/30 group-hover:text-[var(--color-primary)] transition-all duration-300">
             <Upload size={32} className="text-[var(--color-muted-foreground)] group-hover:text-[var(--color-primary)]" />
          </div>

          <h3 className="mt-6 text-lg font-semibold text-[var(--color-foreground)]">
            {file ? file.name : "Drag & drop evidence files here"}
          </h3>
          <p className="mt-2 text-sm text-[var(--color-muted-foreground)]">
            {file ? `${(file.size / 1024).toFixed(2)} KB` : "Supports PDF, TXT, CSV, JSON"}
          </p>
        </div>

        <div className="mt-8 flex justify-end">
          <button
            onClick={handleUpload}
            disabled={!file || status === "uploading"}
            className="flex items-center gap-2 rounded-xl bg-[var(--color-primary)] px-8 py-3 text-sm font-semibold text-white transition-all duration-300 hover:opacity-90 disabled:opacity-50 disabled:hover:opacity-100 shadow-sm hover:shadow-md"
          >
            {status === "uploading" ? (
              <>
                <div className="h-4 w-4 rounded-full border-2 border-white border-t-transparent animate-spin" />
                Ingesting...
              </>
            ) : (
              "Ingest to Graph"
            )}
          </button>
        </div>

        {status === "success" && (
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 flex items-center gap-3 rounded-xl border border-[var(--color-accent)]/30 bg-[var(--color-accent)]/10 text-[var(--color-accent)] p-4 shadow-sm">
            <CheckCircle size={20} />
            <p className="text-sm font-medium">{message}</p>
          </motion.div>
        )}

        {status === "error" && (
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mt-6 flex items-center gap-3 rounded-xl border border-[var(--color-destructive)]/30 bg-[var(--color-destructive)]/10 text-[var(--color-destructive)] p-4 shadow-sm">
            <XCircle size={20} />
            <p className="text-sm font-medium">{message}</p>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}