import api from "./api";

export const askAgent = async (question) => {
  const response = await api.post("ask/", {
    question,
  });

  return response.data;
};