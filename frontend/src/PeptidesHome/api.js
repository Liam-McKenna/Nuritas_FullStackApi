import { getRequest } from "../core/requests";

export function updateData() {
  return new Promise((resolve) => {
    const models = [
      getRequest("peptides/api/users/"),
      getRequest("peptides/api/assays/"),
      getRequest("peptides/api/peptides/"),
    ];
    Promise.all(models).then((responses) => {
      resolve({
        users: responses[0].reduce((uus, u) => ({ ...uus, [u.id]: u }), {}),
        assays: responses[1],
        peptides: responses[2].reduce((pps, p) => ({ ...pps, [p.id]: p }), {}),
      });
    });
  });
}
