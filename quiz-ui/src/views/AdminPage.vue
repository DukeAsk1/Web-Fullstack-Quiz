<template>
  <div class="about">
    <h1>This is the admin page</h1>
  </div>
  <div v-if="token">
    <button @click="logOut">LOG OUT</button>
    <button @click="addQuestionHandler">
      Add A Question
    </button>
    <QuestionList v-if="action === 'view'" :list_of_question="list_of_question" @modify="modifyQuestionHandler"
      @delete="deleteQuestionHandler" />

    <QuestionModifier v-else-if="action === 'modifierQuestion'" :question="question"
      @update:question="updateQuestion" />
    <QuestionModifier v-else-if="action === 'newQuestion'" :question="question_form" @update:question="postQuestion" />

  </div>


  <div v-else>
    <p>Enter Admin Password :</p>
    <input type="text" v-model="password" id="name" name="name" size="10">
    <button class="btn btn-success" type="button" @click="loginPlayer">Connexion</button>
  </div>
</template>

<script>
// Create Vue for modifying the question or add new one 
// Cherche condition for the use of button creation and modification
import participationStorageService from "@/services/ParticipationStorageService";
import quizApiService from "@/services/QuizApiService";

import QuestionList from './QuestionList.vue';
import QuestionModifier from './QuestionModifier.vue';

export default {
  name: "Admin",
  data() {
    return {
      password: '',
      token: null,
      action: "view",
      question: null,
      list_of_question: Array(),
      question_form: {
        position: null,
        text: null,
        title: null,
        image: null,
        possibleAnswers: null
      }

    };
  },
  components: {
    QuestionList,
    QuestionModifier,

  },
  async created() {
    console.log('in admin creation question mode')
    this.token = participationStorageService.getToken();
    this.updateQuestionList();
    // console.log(this.list_of_question);
  },
  methods: {
    async loginPlayer() {
      let login_info = quizApiService.login(this.password);
      let login_result = await login_info;
      if (login_result) {
        participationStorageService.saveToken(login_result.data.token)
        this.token = login_result.data.token
        console.log(this.token)
      }
    },
    async logOut() {
      this.token = null;
      participationStorageService.deleteToken();
    },
    addQuestionHandler() {
      this.action = 'newQuestion';
    },
    async updateQuestionList() {
      // this.list_of_question = Array()
      let quiz_info_detail = quizApiService.getQuizInfo();
      let quiz_result = await quiz_info_detail;
      for (let i = 1; i <= quiz_result.data.size; i++) {
        let question_info = quizApiService.getQuestion(i);
        let question_result = await question_info;

        this.list_of_question.push(question_result.data)
      }
      // console.log('all question in db', this.list_of_question)
    },
    async modifyQuestionHandler(questionPosition) {
      let question_info = quizApiService.getQuestion(questionPosition);
      let question_result = await question_info;
      this.action = 'modifierQuestion';
      console.log('In modifier')
      this.question = question_result.data;
    },
    async deleteQuestionHandler(question_id) {
      console.log('token', this.token)
      await quizApiService.deleteQuestion(question_id, this.token);
      this.token = participationStorageService.getToken();
      this.updateQuestionList();
      this.action = 'view';
    },
    async updateQuestion(new_question) {
      await quizApiService.updateQuestion(this.question.id, new_question, this.token);
      this.token = participationStorageService.getToken();
      this.updateQuestionList();
      this.action = 'view';

    },
    async postQuestion(new_question) {
      await quizApiService.postQuestion(new_question, this.token);
      this.token = participationStorageService.getToken();
      this.updateQuestionList()
      this.action = 'view'
    },
  },

}

</script>



