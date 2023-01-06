<template>
  <div class="container">
    <div class="row">
      <div class="questions-manager">
        <h1 class="text text-center">
          Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}
        </h1>

        <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" class="text-center" />
      </div>
    </div>

    <div class="row">
      <div class="text-center">
        <Transition name="slide">
          <button v-if="currentQuestionPosition != totalNumberOfQuestion" @click="next_question"
            class="btn btn-success">
            Next
          </button>
        </Transition>

        <Transition name="fade">
          <!-- <RouterLink to="/result"> -->
          <button v-if="currentQuestionPosition == totalNumberOfQuestion" @click="next_question"
            class="btn btn-success">
            Submit and see results
          </button>
          <!-- </RouterLink> -->
        </Transition>
      </div>
    </div>
  </div>
</template>

<script>
import QuestionDisplay from "./QuestionDisplay.vue";
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

// console.log(selected);
export default {
  name: "Questions Manager",
  data() {
    return {
      currentQuestion: {
        title: "...",
        text: "...",
        possibleAnswers: {},
      },
      selected: 0,
      currentQuestionPosition: 1,
      totalNumberOfQuestion: 0,
      list_of_answers: Array(),
      // result_quiz: {
      //   answers_selected: null,
      //   score: null
      // }
    };
  },
  components: {
    QuestionDisplay,
  },

  async created() {
    this.currentQuestion = await this.loadQuestionByposition();

    let nb_question = await quizApiService.getQuizInfo()
    this.totalNumberOfQuestion = nb_question.data.size;
    this.token = participationStorageService.getToken();

    console.log(this.currentQuestion);
  },

  methods: {
    async loadQuestionByposition() {
      let current_question = await quizApiService.getQuestion(
        this.currentQuestionPosition
      );
      let question_data = await current_question;
      return question_data.data;
    },
    async next_question() {
      console.log("TYPE DE SELECTED", typeof this.selected);
      console.log(this.selected);
      this.list_of_answers.push(this.selected);
      console.log("list of answers", this.list_of_answers);
      if (this.currentQuestionPosition == this.totalNumberOfQuestion) {
        this.endQuiz();
      } else {
        this.currentQuestionPosition += 1;
        this.currentQuestion = await this.loadQuestionByposition();
        this.selected = 0;
      }

    },
    async answerClickedHandler(value) {
      this.selected = value + 1;
      console.log("selected answer", this.selected);
    },
    async endQuiz() {
      console.log("list of all answers", this.list_of_answers);
      const playerName = participationStorageService.getPlayerName();
      let result_quiz = await quizApiService.postParticipation({
        answers: this.list_of_answers,
        playerName: playerName,
      });
      console.log("JSON RESULT", result_quiz);
      window.localStorage.setItem("result_quiz", JSON.stringify(result_quiz));
      this.result_quiz = {};
      this.$router.push("/result");
    },
  },
};
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: all .5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}


.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateX(-100%);
}

.slide-enter-active,
.slide-leave-active {
  transition: 0.3s ease-out;
}
</style>