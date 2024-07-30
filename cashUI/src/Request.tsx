import axios, { AxiosInstance } from "axios";

const instance: AxiosInstance = axios.create({
  baseURL: "http://localhost:8080/",
  timeout: 3000,
  headers: {},
});

export default instance;
