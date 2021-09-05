import { useState, useEffect } from "react";

import { updateData } from "./api";
import { AssaysList } from "./AssaysList";
import { AssayForm } from "./AssayForm";

import "./peptidesHome.css";

export function PeptidesHome() {
  const [data, setData] = useState({ assays: [], peptides: {}, users: {} });

  const refreshData = () => {
    updateData().then(setData);
  };

  useEffect(() => {
    refreshData();
  }, []);

  const totPeptides = Object.values(data.peptides).length;

  return (
    <div className="peptides-home">
      <h2>Peptides manager - {totPeptides} peptides in the system</h2>
      <div className="peptides-home__content">
        <AssaysList data={data} />
        <AssayForm data={data} refreshData={refreshData} />
      </div>
    </div>
  );
}
