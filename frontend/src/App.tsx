import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import AppLayout from "./components/layout/AppLayout";

import Dashboard from "./pages/Dashboard";
import NetworkExplorer from "./pages/NetworkExplorer";
import Cases from "./pages/Cases";
import Persons from "./pages/Persons";
import PersonInvestigation from "./pages/PersonInvestigation";
import Transactions from "./pages/Transactions";
import Anomalies from "./pages/Anomalies";
import Investigation from "./pages/Investigation";
import Documents from "./pages/Documents";


function PersonRoute() {
  return <PersonInvestigation />;
}


export default function App() {

  return (
    <BrowserRouter>

      <Routes>

        <Route
          element={<AppLayout />}
        >

          <Route
            path="/"
            element={<Dashboard />}
          />

          <Route
            path="/persons"
            element={<Persons />}
          />

          <Route
            path="/persons/:personId"
            element={<PersonRoute />}
          />

          <Route
            path="/network"
            element={<NetworkExplorer />}
          />

          <Route
            path="/cases"
            element={<Cases />}
          />

          <Route
            path="/transactions"
            element={<Transactions />}
          />

          <Route
            path="/anomalies"
            element={<Anomalies />}
          />

          <Route
            path="/investigation"
            element={<Investigation />}
          />

          <Route
            path="/documents"
            element={<Documents />}
          />

        </Route>

      </Routes>

    </BrowserRouter>
  );
}