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
import { motion } from "framer-motion";

const navigation = [
  { name: "Dashboard", path: "/", icon: LayoutDashboard },
  { name: "Network Explorer", path: "/network", icon: Network },
  { name: "Cases", path: "/cases", icon: Search },
  { name: "Persons", path: "/persons", icon: Users },
  { name: "Transactions", path: "/transactions", icon: ArrowLeftRight },
  { name: "Anomalies", path: "/anomalies", icon: TriangleAlert },
  { name: "Investigation", path: "/investigation", icon: Search },
  { name: "Documents", path: "/documents", icon: FileText },
];

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 bg-[#0E0417]">
      <div className="flex h-20 items-center gap-3 px-6">
        <div>
          <h1 className="text-2xl font-bold tracking-wide text-[var(--color-primary)]">ShadowNet</h1>
        </div>
      </div>

      <nav className="space-y-1 p-4">
        {navigation.map((item, index) => {
          const Icon = item.icon;
          return (
            <motion.div
              key={item.path}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 + 0.1, duration: 0.3 }}
            >
              <NavLink
                to={item.path}
                end={item.path === "/"}
                className={({ isActive }) =>
                  `
                    flex items-center gap-3 px-4 py-3 
                    text-sm font-medium transition-all duration-300 rounded-none font-sans
                    ${
                      isActive
                        ? "bg-[#160424] text-[var(--color-primary)]"
                        : "text-[var(--color-muted-foreground)] hover:bg-[#160424]/50 hover:text-[var(--color-primary)]"
                    }
                  `
                }
              >
                <Icon size={18} />
                <span>{item.name}</span>
              </NavLink>
            </motion.div>
          );
        })}
      </nav>
    </aside>
  );
}