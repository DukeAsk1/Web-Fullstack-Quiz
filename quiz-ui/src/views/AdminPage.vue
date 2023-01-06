<template>
  <div v-if="token">
    <div class="row text-center w-50 m-auto mt-5">
      <div class="col">
        <div>
          <button @click="logOut" class="btn btn-danger">Log out</button>
        </div>
      </div>

      <div class="col">
        <div>
          <button @click="addQuestionHandler" class="btn btn-success">
            Add a question
          </button>
        </div>
      </div>

      <div class="col-3">
        <button @click="deleteAllQuestions" class="btn btn-danger">
          Delete all questions
        </button>
      </div>
      <div class="col-4">
        <button @click="deleteAllParticipations" class="btn btn-danger">
          Delete all participations
        </button>
      </div>
    </div>

    <div class="row mt-5">
      <QuestionList
        v-if="action === 'view'"
        :list_of_question="list_of_question"
        @modify="modifyQuestionHandler"
        @delete="deleteQuestionHandler"
      />

      <QuestionModifier
        v-else-if="action === 'modifierQuestion'"
        :question="question"
        @update:question="updateQuestion"
      />
      <QuestionModifier
        v-else-if="action === 'newQuestion'"
        :question="question_form"
        :action="action"
        @update:question="postQuestion"
        @post:json="postQuestion"
      />
    </div>
  </div>

  <div v-else>
    <div class="container mt-5">
      <div class="row">
        <div class="col-6 offset-3 text-center">
          <h2>Enter Admin Password :</h2>
        </div>
      </div>

      <div class="col-6 offset-3 text-center mt-5">
        <div class="row gy-2">
          <div class="col-6 offset-3">
            <div class="form-floating mb-3">
              <input
                type="password"
                class="form-control"
                v-model="password"
                id="name"
                name="name"
                placeholder="yourpassword"
              />
              <label class="text-dark" for="name">Admin password</label>
            </div>
          </div>

          <div class="col-fluid">
            <button class="btn btn-success" type="button" @click="loginPlayer">
              Log in
            </button>
          </div>
        </div>
      </div>

      <div
        class="col-6 offset-3 mt-3 text-center alert alert-danger alert-dismissible fade show"
        role="alert"
        v-if="!password && wrongSubmit"
      >
        <strong>Error !</strong> Please enter a password
      </div>
    </div>
  </div>
</template>

<script>
// Create Vue for modifying the question or add new one
// Cherche condition for the use of button creation and modification
import participationStorageService from "@/services/ParticipationStorageService";
import quizApiService from "@/services/QuizApiService";

import QuestionList from "./QuestionList.vue";
import QuestionModifier from "./QuestionModifier.vue";

export default {
  name: "Admin",
  data() {
    return {
      password: "",
      wrongSubmit: false,
      token: null,
      action: "view",
      question: null,
      list_of_question: Array(),
      question_form: {
        position: null,
        text: null,
        title: null,
        image: null,
        possibleAnswers: null,
      },
    };
  },
  components: {
    QuestionList,
    QuestionModifier,
  },
  async created() {
    // console.log('in admin creation question mode')
    // this.token = participationStorageService.getToken();
    // this.updateQuestionList();
    // console.log(this.list_of_question);
  },
  methods: {
    async loginPlayer() {
      if (this.password.toString() === "") {
        this.wrongSubmit = true;
        return;
      }
      let login_info = quizApiService.login(this.password);
      let login_result = await login_info;
      if (login_result) {
        participationStorageService.saveToken(login_result.data.token);
        this.token = login_result.data.token;
        console.log(this.token);
        this.updateQuestionList();
      }
    },
    async logOut() {
      this.token = null;
      participationStorageService.deleteToken();
    },
    addQuestionHandler() {
      this.action = "newQuestion";
    },
    async updateQuestionList() {
      // this.list_of_question = Array()
      let quiz_info_detail = quizApiService.getQuizInfo();
      let quiz_result = await quiz_info_detail;
      for (let i = 1; i <= quiz_result.data.size; i++) {
        let question_info = quizApiService.getQuestion(i);
        let question_result = await question_info;

        this.list_of_question.push(question_result.data);
      }
      // console.log('all question in db', this.list_of_question)
    },
    async modifyQuestionHandler(questionPosition) {
      let question_info = quizApiService.getQuestion(questionPosition);
      let question_result = await question_info;
      this.action = "modifierQuestion";
      console.log("In modifier");
      this.question = question_result.data;
    },
    async deleteQuestionHandler(question_id) {
      console.log("token", this.token);
      await quizApiService.deleteQuestion(question_id, this.token);
      this.token = participationStorageService.getToken();
      this.updateQuestionList();
      this.action = "view";
    },
    async updateQuestion(new_question) {
      await quizApiService.updateQuestion(
        this.question.id,
        new_question,
        this.token
      );
      this.token = participationStorageService.getToken();
      this.updateQuestionList();
      this.action = "view";
    },
    async postQuestion(new_question) {
      console.log("QUESTION AFTER SAVE", new_question);
      await quizApiService.postQuestion(new_question, this.token);
      this.token = participationStorageService.getToken();
      this.updateQuestionList();
      this.action = "view";
    },
    async deleteAllQuestions() {
      await quizApiService.deleteAllQuestions(this.token);
      this.token = participationStorageService.getToken();
      this.updateQuestionList();
      this.action = "view";
    },
    async deleteAllParticipations() {
      await quizApiService.deleteAllParticipations(this.token);
      this.token = participationStorageService.getToken();
      this.action = "view";
    },
  },
};
</script>
