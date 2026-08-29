import {
  useEffect,
  useState,
} from "react";

import {
  Search,
  User,
} from "lucide-react";

import {
  useNavigate,
} from "react-router-dom";

import {
  getPersons,
} from "../api/persons";

import type {
  Person,
} from "../types/person";


export default function Persons() {

  const navigate = useNavigate();

  const [persons, setPersons] =
    useState<Person[]>([]);

  const [search, setSearch] =
    useState("");

  useEffect(() => {

    getPersons(200)
      .then((data) => {
        setPersons(data.persons);
      })
      .catch(console.error);

  }, []);


  const filtered = persons.filter((person) => {

    const value =
      `${person.id} ${person.name || ""}`
        .toLowerCase();

    return value.includes(
      search.toLowerCase()
    );

  });


  return (
    <div className="space-y-6">

      <div>

        <h1 className="text-2xl font-bold text-white">
          Persons
        </h1>

        <p className="text-sm text-slate-500">
          Search and investigate graph entities
        </p>

      </div>


      <div className="relative">

        <Search
          size={18}
          className="
            absolute
            left-4
            top-1/2
            -translate-y-1/2
            text-slate-500
          "
        />

        <input
          value={search}
          onChange={(e) =>
            setSearch(e.target.value)
          }
          placeholder="Search by person ID or name..."
          className="
            w-full
            rounded-xl
            border border-slate-800
            bg-[#0c1220]
            py-3
            pl-11
            pr-4
            text-sm
            text-white
            outline-none
            focus:border-blue-500
          "
        />

      </div>


      <div className="
        overflow-hidden
        rounded-xl
        border border-slate-800
        bg-[#0c1220]
      ">

        <table className="w-full">

          <thead className="border-b border-slate-800">

            <tr className="text-left text-xs uppercase tracking-wider text-slate-600">

              <th className="px-6 py-4">
                Person
              </th>

              <th className="px-6 py-4">
                Source
              </th>

              <th className="px-6 py-4">
                Degree
              </th>

              <th className="px-6 py-4">
                PageRank
              </th>

              <th className="px-6 py-4">
                Community
              </th>

            </tr>

          </thead>


          <tbody>

            {filtered.map((person) => (

              <tr
                key={person.id}
                onClick={() =>
                  navigate(
                    `/persons/${encodeURIComponent(person.id)}`
                  )
                }
                className="
                  cursor-pointer
                  border-b border-slate-800
                  transition
                  hover:bg-slate-800/40
                "
              >

                <td className="px-6 py-4">

                  <div className="flex items-center gap-3">

                    <div className="rounded-lg bg-blue-500/10 p-2 text-blue-400">
                      <User size={16} />
                    </div>

                    <div>

                      <p className="text-sm font-medium text-white">
                        {person.name ||
                          "Unknown entity"}
                      </p>

                      <p className="font-mono text-xs text-slate-600">
                        {person.id}
                      </p>

                    </div>

                  </div>

                </td>


                <td className="px-6 py-4 text-xs text-slate-400">
                  {person.source || "—"}
                </td>


                <td className="px-6 py-4 text-sm text-slate-300">
                  {person.degree ?? "—"}
                </td>


                <td className="px-6 py-4 font-mono text-xs text-slate-400">
                  {person.pagerank?.toFixed(6) || "—"}
                </td>


                <td className="px-6 py-4">

                  <span className="
                    rounded-full
                    bg-blue-500/10
                    px-3
                    py-1
                    text-xs
                    text-blue-400
                  ">

                    {person.community_id ?? "—"}

                  </span>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}