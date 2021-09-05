import { useState } from "react";
import { postRequest } from "../core/requests";

export function AssayForm({ data, refreshData }) {
  const [name, setName] = useState("");
  const [operator, setOperator] = useState(null);
  const [peptides, setPeptides] = useState("");
  const [error, setError] = useState("");

  const save = (e) => {
    e.preventDefault();
    const peptidesList = peptides.split("\n");
    const payload = {
      name,
      operator,
      peptides: peptidesList,
    };
    postRequest("peptides/api/assays/", payload)
      .then(() => {
        setName("");
        setOperator(null);
        setPeptides("");
        refreshData();
      })
      .catch(() => {
        setError("Something went wrong!");
      });
  };

  /* Excercise 1 ADD-CODE-HERE */
  const userOptions = Object.values(data.users).map((u) => {
    return (
      <option value={u.id} key={u.id}>
        {u.full_name}
      </option>
    );
  });

  return (
    <div className="assay-form">
      <h2>Add new assay</h2>
      {error && <div className="assay-form__error">{error}</div>}
      <form onSubmit={save}>
        <div className="assay-form__values">
          <Field label="Name">
            <input
              value={name}
              onChange={(e) => setName(e.target.value || "")}
            />
          </Field>
          <Field label="Operator">
            <select
              value={operator || ""}
              onChange={(e) => setOperator(e.target.value)}
            >
              <option />
              {userOptions}
            </select>
          </Field>
          {/* Excercise 5 ADD-CODE-HERE */}
          <Field label="Peptides">
            <textarea
              value={peptides}
              onChange={(e) => setPeptides(e.target.value || "")}
            />
            <span style={{ fontSize: 10, color: "#888" }}>(one per line)</span>
          </Field>
        </div>
        <div className="assay-form__actions">
          <button className="assay-form__save" type="submit">
            Save
          </button>
        </div>
      </form>
    </div>
  );
}

function Field({ label, children }) {
  return (
    <div className="assay-form__field">
      <div className="assay-form__label">{label}</div>
      <div className="assay-form__control">{children}</div>
    </div>
  );
}
