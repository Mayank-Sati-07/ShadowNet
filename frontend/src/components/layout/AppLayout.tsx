import { Outlet, useNavigate, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";

import Sidebar from "./Sidebar";
import Header from "./Header";

export default function AppLayout() {
  const navigate = useNavigate();
  const location = useLocation();

  function handleSearch(value: string) {
    const query = value.trim();
    if (!query) return;
    navigate(`/persons/${encodeURIComponent(query)}`);
  }

  return (
    <div className="min-h-screen bg-[var(--color-background)] text-[var(--color-foreground)] selection:bg-[var(--color-primary)] selection:text-white overflow-hidden">
      <Sidebar />
      <Header onSearch={handleSearch} />
      <main className="ml-64 pt-20 min-h-screen overflow-y-auto">
        <AnimatePresence mode="wait">
          <motion.div
            key={location.pathname}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -15 }}
            transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
            className="p-8 h-full"
          >
            <Outlet />
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  );
}