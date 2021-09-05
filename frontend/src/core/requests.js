import { API_ROOT } from "../constants";

import { METHODS, RESPONSE_CODES } from "./constants";

let logRequests = false;
let commonHeaders = {};

export function setLogRequests(v) {
  logRequests = v;
}

if (typeof window !== undefined) window.requestsSetLogRequests = setLogRequests;

export function setCommonHeaders(common) {
  commonHeaders = { ...common };
}

export function getCommonHeaders() {
  return { ...commonHeaders };
}

export function buildRequestUrl(url, qs) {
  const baseUrl =
    url.indexOf("http://") >= 0 || url.indexOf("https://") >= 0
      ? url
      : `${API_ROOT}${url}`;
  return `${baseUrl}${qs ? `?${objectToQueryString(qs)}` : ""}`;
}

export default function request(
  url,
  {
    payload,
    method = METHODS.GET,
    headers = {},
    body,
    extraOptions = {},
    qs,
    fetchParams,
    responseType = "json",
    returnResponse = false,
  } = {}
) {
  const params = fetchParams || {
    method,
    headers: { ...getCommonHeaders(), ...headers },
    ...extraOptions,
  };

  // Set auto header to JSON
  if (
    params.headers &&
    typeof payload === "object" &&
    !params.headers["Content-Type"]
  ) {
    params.headers["Content-Type"] = "application/json";
  }

  if (body) {
    params.body = body;
  } else if (typeof payload === "object") {
    params.body = JSON.stringify(payload);
  }

  const requestUrl = buildRequestUrl(url, qs);

  if (logRequests) console.info(`Request [${params.method}]: `, url, params);
  return fetch(requestUrl, params)
    .then((response) => {
      if (logRequests) console.info("Request: response to ", url, response);
      if (!response.ok) {
        console.error(
          "Request: Invalid!",
          response.status,
          response.statusText
        );
        throw new Error(response);
      }

      if (returnResponse) return response;

      return response.status !== RESPONSE_CODES.NO_CONTENT &&
        responseType === "json"
        ? response.json()
        : response.text();
    })
    .catch((error) => {
      throw new Error(error);
    });
}

export function getRequest(url, options = {}) {
  return request(url, options);
}

export function postRequest(url, payload, options = {}) {
  return request(url, { payload, method: METHODS.POST, ...options });
}

export function deleteRequest(url, payload, options = {}) {
  return request(url, { payload, method: METHODS.DELETE, ...options });
}

export function putRequest(url, payload, options = {}) {
  return request(url, { payload, method: METHODS.PUT, ...options });
}

export function objectToQueryString(obj) {
  return Object.keys(obj)
    .map((key) => key + "=" + obj[key])
    .join("&");
}
