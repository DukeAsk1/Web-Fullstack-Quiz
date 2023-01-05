<template>
  <div class="container">
    <!-- Finduquiz -->
    <div class="row g-4">
      <div class="col-fluid">
        <h2 class="text bg-gradient text-center">Fin du quiz !</h2>
      </div>

      <!-- Welcome et Score -->
      <div class="col-fluid text-center">
        <h3>Salut, {{ list_of_result.playerName }}</h3>
        <div>
          Ton score est de :
          <strong>
            {{ list_of_result.score }}
            point{{ list_of_result.score > 1 ? "s" : "" }}
          </strong>
        </div>
      </div>
      <!--  -->

      <!-- Affichage des réponses -->
      <div class="col">
        <div class="row">
          <!-- Left -->
          <div class="col-6">
            <div class="col-fluid">
              <h3>Voici tes réponses :</h3>
            </div>

            <div class="col">
              <div class="row gy-4">
                <div class="col-fluid" v-for="answer in list_of_result.answers_list" :key="answer">
                  <h4>Question : {{ answer[0] }}</h4>
                  <p :class="{
                    'text-success': answer[1] === answer[3],
                    'text-danger': answer[1] !== answer[3],
                  }">
                    Your answer : {{ answer[1] }} <br />
                    The correct answer : {{ answer[3] }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          <!-- Right -->
          <div class="col-6">
            <div>
              The leaderboard for the quiz:
              <RankingsVue v-if="action === 'end'" />
            </div>
          </div>
        </div>
      </div>
      <!--  -->

      <!-- boutons -->
      <div class="col-fluid">
        <div class="row justify">
          <div class="col-2 offset-4 text-center">
            <Transition name="slide">
              <RouterLink to="/questions-manager">
                <button class="btn btn-success">
                  <!-- v-on:click="new_attempt" -->
                  TRY AGAIN
                </button>
              </RouterLink>
            </Transition>
          </div>
          <div class="col-2 text-center">
            <Transition name="fade">
              <RouterLink to="/">
                <button class="btn btn-success" v-on:click="home_page">
                  HOME PAGE
                </button>
              </RouterLink>
            </Transition>
          </div>
        </div>
      </div>
      <!--  -->
    </div>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
  }
}

.highlight {
  background-color: yellow;
}
</style>

<script>
import QuestionDisplay from "./QuestionDisplay.vue";
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";
import RankingsVue from "./Rankings.vue";

// console.log(selected);
export default {
  name: "Questions Manager",
  data() {
    return {
      registeredScores: [],
      score: 0,
      answer_current_question: {
        index: 0,
        answer: "...",
        correct: "...",
      },
      list_of_result: Array(),
      action: 'end',
    };
  },

  computed: {
    highlightClass(value) {
      if (
        value.date === this.list_of_result.date_attempt &&
        value.playerName === this.list_of_result.playerName &&
        value.score === this.list_of_result.score
      ) {
        return value //=== value ? "highlight" : "";
      }
    },
  },

  components: {
    QuestionDisplay,
    RankingsVue,
  },

  async created() {
    // parse the list as JSON
    this.list_of_result = JSON.parse(
      window.localStorage.getItem("result_quiz")
    ).data;
    // console.log("Result page quiz", this.list_of_result);
    // console.log(this.list_of_result.playerName)
    let quizInfo = await quizApiService.getQuizInfo();
    this.registeredScores = quizInfo.data;
    // console.log(this.registeredScores);
  },
  methods: {
    new_attempt() {
      this.list_of_result = Array();
      window.localStorage.removeItem('result_quiz');
      this.score = 0;
      // this.$router.push("/questions-manager");
    },
    home_page() {
      this.list_of_result = Array();
      window.localStorage.removeItem('result_quiz');
      participationStorageService.removePlayerName();
      // this.$router.push("/");
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
