import { useState } from "react";

export function AssaysList({ data }) {
  const [expanded, setExpanded] = useState({});

  return (
    <div className="assays-list">
      {data.assays.map((assay) => {
        /* Excercise 4 ADD-CODE-HERE: display assay type somewhere here */
        return (
          <div className="assay-item" key={assay.id}>
            <div className="assay-item__header">
              <div className="assay-item__title">{assay.name}</div>
              <div className="assay-item__controls">
                {expanded[assay.id] ? (
                  <span
                    onClick={() =>
                      setExpanded({ ...expanded, [assay.id]: false })
                    }
                  >
                    hide peptides
                  </span>
                ) : (
                  <span
                    onClick={() =>
                      setExpanded({ ...expanded, [assay.id]: true })
                    }
                  >
                    view peptides
                  </span>
                )}
              </div>
            </div>
            <div className="assay-item__details">
              {data.users[assay.operator].full_name}
            </div>
            {expanded[assay.id] && (
              <div className="assay-item__peptides">
                {assay.peptides.map((peptideId, index) => {
                  const peptide = data.peptides[peptideId];
                  return (
                    <div className="assay-item__peptide" key={index}>
                      <div className="assay-item__peptide__name">
                        {peptide.name}
                      </div>
                      <div>{peptide.sequence}</div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
