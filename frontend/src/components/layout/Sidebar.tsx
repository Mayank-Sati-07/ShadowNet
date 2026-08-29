import {
  LayoutDashboard,
  Users,
  Network,
  ArrowLeftRight,
  TriangleAlert,
  Search,
  FileText,
  Shield,
} from "lucide-react";

import { NavLink } from "react-router-dom";


const navigation = [
  {
    name: "Dashboard",
    path: "/",
    icon: LayoutDashboard,
  },
  {
    name: "Network Explorer",
    path: "/network",
    icon: Network,
  },
  {
    name: "Cases",
    path: "/cases",
    icon: Search,
  },
  {
    name: "Persons",
    path: "/persons",
    icon: Users,
  },
  {
    name: "Transactions",
    path: "/transactions",
    icon: ArrowLeftRight,
  },
  {
    name: "Anomalies",
    path: "/anomalies",
    icon: TriangleAlert,
  },
  {
    name: "Investigation",
    path: "/investigation",
    icon: Search,
  },
  {
    name: "Documents",
    path: "/documents",
    icon: FileText,
  },
];


export default function Sidebar() {

  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r border-slate-800 bg-[#0a0f1c]">

      <div className="flex h-20 items-center gap-3 border-b border-slate-800 px-6">

        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600/20">
          <Shield className="text-blue-400" size={22} />
        </div>

        <div>
          <h1 className="font-bold tracking-wide text-white">
            CNAS
          </h1>

          <p className="text-xs text-slate-500">
            Investigation System
          </p>
        </div>

      </div>


      <nav className="space-y-1 p-4">

        {navigation.map((item) => {

          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === "/"}
              className={({ isActive }) =>
                `
                flex items-center gap-3 rounded-lg px-4 py-3
                text-sm transition
                ${
                  isActive
                    ? "bg-blue-600/15 text-blue-400"
                    : "text-slate-400 hover:bg-slate-800/60 hover:text-white"
                }
                `
              }
            >
              <Icon size={18} />

              <span>
                {item.name}
              </span>

            </NavLink>
          );
        })}

      </nav>

    </aside>
  );
}