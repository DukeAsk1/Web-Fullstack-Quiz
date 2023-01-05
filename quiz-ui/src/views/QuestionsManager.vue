<template>
  <div class="container">
    <div class="row">
      <div class="questions-manager">
        <h1 class="text text-center">
          Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}
        </h1>

        <QuestionDisplay
          :question="currentQuestion"
          @answer-selected="answerClickedHandler"
          class="text-center"
        />
      </div>
    </div>

    <div class="row">
      <div class="text-center">
        <button
          v-if="currentQuestionPosition != totalNumberOfQuestion"
          @click="next_question"
          class="btn btn-success"
        >
          Next
        </button>

        <button
          v-if="currentQuestionPosition == totalNumberOfQuestion"
          @click="next_question"
          class="btn btn-success"
        >
          Submit and see results
        </button>
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
    // this.currentQuestion.questionTitle = currentQuestion.data.title;
    // this.currentQuestion.questionText = currentQuestion.data.text;
    // this.currentQuestion.possibleAnswers = currentQuestion.data.possibleAnswers;

    let nb_question = await this.getNumberOfQuestion();
    this.totalNumberOfQuestion = nb_question.data.nb_question;
    // this.value = this.value;
    // console.log(this.selected.isCorrect);
    //this.score = this.calculateScore(value);
    //await this.getCorrectAnswer();
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
    getNumberOfQuestion() {
      return quizApiService.getNumberOfQuestion();
    },
    async next_question() {
      console.log("TYPE DE SELECTED", typeof this.selected);
      console.log(this.selected);
      // this.selected.position = this.currentQuestionPosition
      this.list_of_answers.push(this.selected);
      console.log("list of answers", this.list_of_answers);
      if (this.currentQuestionPosition == this.totalNumberOfQuestion) {
        this.endQuiz();
      } else {
        this.currentQuestionPosition += 1;
        this.currentQuestion = await this.loadQuestionByposition();
        // console.log('current question')
        // console.log(this.currentQuestion);
      }
      // const selectedAnswer = this.selected;
      // // const answer = this.currentQuestion.flatMap(currentQuestion =>
      // //                                     currentQuestion.possibleAnswers).find(possibleAnswers =>
      // //                                     possibleAnswers.id === selectedAnswer);
      // if (selectedAnswer.isCorrect) {
      //   this.score++;
      // }

      // this.answer_current_question.index = this.currentQuestionPosition;
      // this.answer_current_question.answer = this.selected.text;
      // this.getCorrectAnswer();
      // this.list_of_answers.push(this.answer_current_question);
      // this.currentQuestionPosition++;
      // //this.calculateScore();
      // console.log('new position');
      // console.log(this.currentQuestionPosition);
      // this.currentQuestion = this.loadQuestionByposition(this.currentQuestionPosition);
      // console.log(this.currentQuestion);

      // this.currentQuestion.questionTitle = currentQuestion.data.title;
      // this.currentQuestion.questionText = currentQuestion.data.text;
      // this.currentQuestion.possibleAnswers = currentQuestion.data.possibleAnswers;
    },
    async answerClickedHandler(value) {
      this.selected = value + 1;
      console.log("selected answer", this.selected);
    },
    async endQuiz() {
      console.log("list of all answers", this.list_of_answers);
      // const list_index = JSON.stringify(this.list_of_answers);
      // console.log(list_index);
      const playerName = participationStorageService.getPlayerName();
      let result_quiz = await quizApiService.postParticipation({
        answers: this.list_of_answers,
        playerName: playerName,
      });
      console.log("JSON RESULT", result_quiz);
      // const json_result = JSON.stringify(this.result_quiz);
      // console.log('STRINGIFY', json_result)
      window.localStorage.setItem("result_quiz", JSON.stringify(result_quiz));
      this.$router.push("/result");
    },
  },
};
</script>
