import { Outlet, useNavigate } from "react-router-dom";

import Sidebar from "./Sidebar";
import Header from "./Header";


export default function AppLayout() {

  const navigate = useNavigate();

  function handleSearch(value: string) {

    const query = value.trim();

    if (!query) {
      return;
    }

    navigate(`/persons/${encodeURIComponent(query)}`);
  }


  return (
    <div className="min-h-screen bg-[#070b14]">

      <Sidebar />

      <Header
        onSearch={handleSearch}
      />

      <main className="ml-64 pt-20">

        <div className="p-8">

          <Outlet />

        </div>

      </main>

    </div>
  );
}