import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getQuestion(position) {
    return this.call("get", "questions?position=" + String(position));
  },
  getNumberOfQuestion() {
    return this.call("get", 'nb_question');
  },
  login(password) {
    return this.call("post", "login", { "password": password });
  },
  updateQuestion(question_id, question, token) {
    return this.call("put", "questions/" + question_id, question, token);
  },
  postQuestion(question, token) {
    return this.call("post", "questions", question, token);
  },
  deleteQuestion(question_id) {
    //console.log("token in API SERVICE", token)
    console.log('ID API SERVICE DELETE', question_id)
    return this.call("delete", "questions/" + question_id);
  },
};