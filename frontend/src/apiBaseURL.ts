import axios from "axios";

export const api = axios.create({
    baseURL: "http://localhost:5000",
    // baseURL: "https://email-classifier-backend-ulrn.onrender.com",
});