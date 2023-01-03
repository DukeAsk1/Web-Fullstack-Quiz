<template>
  <div class="questions-manager">
    <h1>Questions Manager</h1>
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>

    <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
  </div>

  <button v-if="currentQuestionPosition != totalNumberOfQuestion" @click="next_question">Next</button>

  <button v-if="currentQuestionPosition == totalNumberOfQuestion" @click="next_question">Submit and see results</button>

</template>

<script>
import QuestionDisplay from './QuestionDisplay.vue';
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
        possibleAnswers: {

        }
      },
      selected: Array(),
      currentQuestionPosition: 1,
      totalNumberOfQuestion: 0,
      score: 0,
      answer_current_question: {
        index: 0,
        answer: "...",
        correct: '...',
      },
      list_of_answers: Array(),
    };
  },
  components: {
    QuestionDisplay
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
  },

  methods: {
    async loadQuestionByposition() {
      let current_question = quizApiService.getQuestion(this.currentQuestionPosition);
      let question_data = await current_question;
      return question_data.data
    },
    async getCorrectAnswer() {
      for (let i = 0; i <= this.currentQuestion.possibleAnswers.length - 1; i++) {
        if (this.currentQuestion.possibleAnswers[i].isCorrect === true) {
          this.answer_current_question.correct = this.currentQuestion.possibleAnswers[i].text;
        }
      }
    },
    getNumberOfQuestion() {
      return quizApiService.getNumberOfQuestion()
    },
    async calculateScore() {
      // for (const element of this.currentQuestion) {
      //   console.log(element);
      //   if (element.isCorrect === true) {
      //     console.log(element)
      //     this.answer_current_question.correct = this.element.text;
      //   }
      // }
      if (this.selected.isCorrect === true) {
        this.score++;
      }
      else {
        this.score;
      }
    },
    async next_question() {
      console.log("TYPE DE SELECTED", typeof (this.selected))
      console.log(this.selected)
      this.selected.position = this.currentQuestionPosition
      this.list_of_answers.push(this.selected);
      console.log('list of answers', this.list_of_answers);
      if (this.currentQuestionPosition == this.totalNumberOfQuestion) {
        this.endQuiz()
      }
      else {
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
      this.selected = value;
      console.log('selected answer', this.selected);
    },
    async endQuiz() {
      console.log('list of all answers', this.list_of_answers);
      const listString = JSON.stringify(this.list_of_answers);
      console.log(listString);
      const playerName = participationStorageService.getPlayerName();
      await quizApiService.postParticipation(
        {
          'player_answers': listString,
          'playerName': playerName
        });
      //window.localStorage.setItem("list_of_answers", listString);
      // this.$router.push('/result');
    },
  },

};
</script>