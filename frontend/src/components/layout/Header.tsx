import { Search, Bell } from "lucide-react";

interface HeaderProps {
  onSearch: (value: string) => void;
}


export default function Header({
  onSearch,
}: HeaderProps) {

  return (
    <header className="fixed left-64 right-0 top-0 z-30 h-20 border-b border-slate-800 bg-[#070b14]/95 px-8 backdrop-blur">

      <div className="flex h-full items-center justify-between">

        <div>
          <h2 className="text-lg font-semibold text-white">
            Criminal Network Analysis System
          </h2>

          <p className="text-xs text-slate-500">
            Intelligence & Investigation Platform
          </p>
        </div>


        <div className="flex items-center gap-4">

          <div className="relative">

            <Search
              size={17}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
            />

            <input
              onChange={(e) => onSearch(e.target.value)}
              placeholder="Search person ID..."
              className="
                w-72 rounded-lg border border-slate-800
                bg-slate-900/70 py-2.5 pl-10 pr-4
                text-sm text-white outline-none
                placeholder:text-slate-600
                focus:border-blue-500
              "
            />

          </div>

          <button className="rounded-lg border border-slate-800 p-2.5 text-slate-400 hover:text-white">
            <Bell size={18} />
          </button>

        </div>

      </div>

    </header>
  );
}