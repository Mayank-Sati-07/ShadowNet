import {
  useState,
} from "react";

import {
  Upload,
  FileText,
} from "lucide-react";

import { api } from "../api/client";


export default function Documents() {

  const [file, setFile] =
    useState<File | null>(null);

  const [result, setResult] =
    useState<any>(null);

  const [loading, setLoading] =
    useState(false);


  async function upload() {

    if (!file) {
      return;
    }

    const formData =
      new FormData();

    formData.append(
      "file",
      file
    );


    try {

      setLoading(true);

      const response =
        await api.post(
          "/documents/search",
          formData,
          {
            headers: {
              "Content-Type":
                "multipart/form-data",
            },
          }
        );

      setResult(
        response.data
      );

    } finally {

      setLoading(false);

    }

  }


  return (
    <div className="mx-auto max-w-4xl space-y-6">

      <div>

        <h1 className="text-2xl font-bold text-white">
          Evidence & Documents
        </h1>

        <p className="text-sm text-slate-500">
          Upload FIR and investigation documents
        </p>

      </div>


      <div className="
        rounded-xl
        border border-dashed
        border-slate-700
        bg-[#0c1220]
        p-12
        text-center
      ">

        <div className="
          mx-auto
          flex
          h-16
          w-16
          items-center
          justify-center
          rounded-xl
          bg-blue-500/10
          text-blue-400
        ">

          <Upload size={28} />

        </div>


        <h2 className="mt-5 font-semibold text-white">
          Upload investigation document
        </h2>


        <p className="mt-2 text-sm text-slate-500">
          PDF, TXT and supported evidence files
        </p>


        <input
          type="file"
          onChange={(e) =>
            setFile(
              e.target.files?.[0] || null
            )
          }
          className="mx-auto mt-6 block text-sm text-slate-400"
        />


        {file && (

          <div className="
            mx-auto
            mt-5
            flex
            max-w-md
            items-center
            gap-3
            rounded-lg
            bg-slate-900
            p-3
            text-left
          ">

            <FileText
              size={18}
              className="text-blue-400"
            />

            <span className="text-sm text-slate-300">
              {file.name}
            </span>

          </div>

        )}


        <button
          onClick={upload}
          disabled={!file || loading}
          className="
            mt-6
            rounded-lg
            bg-blue-600
            px-6
            py-3
            text-sm
            font-medium
            text-white
            disabled:opacity-40
          "
        >

          {loading
            ? "Uploading..."
            : "Upload Document"}

        </button>

      </div>


      {result && (

        <pre className="
          rounded-xl
          border border-slate-800
          bg-slate-950
          p-5
          text-xs
          text-slate-400
        ">

          {JSON.stringify(
            result,
            null,
            2
          )}

        </pre>

      )}

    </div>
  );
}