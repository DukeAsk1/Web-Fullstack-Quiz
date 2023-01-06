<template>
  <div class="container">
    <!-- Finduquiz -->
    <div class="row g-4">
      <div class="col-fluid">
        <h2 class="text bg-gradient text-center">End of the quiz !</h2>
      </div>

      <!-- Welcome et Score -->
      <div class="col-fluid text-center">
        <h3>Hi, {{ list_of_result.playerName }}</h3>
        <div>
          Your score is :
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
              <h3>Here are your answers :</h3>
            </div>

            <transition name="slide">
              <div class="col">
                <div class="row gy-4">
                  <div class="col-fluid" v-for="answer in this.list_of_result.answers_list" :key="answer">

                    <p :class="{
                      'text-success': answer[1] === answer[3],
                      'text-danger': answer[1] !== answer[3],
                    }" v-if="answer[4]">
                    <h4 :style="{ color: 'black' }">Question : {{ answer[0] }}</h4>
                    Your answer : {{ answer[1] }} <br />
                    The correct answer : {{ answer[3] }}
                    </p>
                  </div>
                  <button @click="toggleResult">{{ resultText }}</button>
                </div>
              </div>
            </transition>
          </div>
          <!-- Right -->
          <div class="col-6">
            <div align="center">
              <h2>The leaderboard for the quiz:</h2>
              <RankingsVue :table="table" />
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
      table: 'end',
      resultText: 'Show Details',
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
    let quizInfo = await quizApiService.getQuizInfo();
    this.registeredScores = quizInfo.data;
    for (let i = 0; i < this.list_of_result.answers_list.length; i++) {
      if (i < 3) {
        this.list_of_result.answers_list[i][4] = true;
      }
      else {
        this.list_of_result.answers_list[i][4] = false;
      }
    }
    console.log(this.list_of_result);
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

    async toggleResult() {
      this.resultText = this.resultText === 'Show Details' ? 'Hide Details' : 'Show Details'
      if (this.resultText === 'Show Details') {
        for (let i = 3; i < this.list_of_result.answers_list.length; i++) {
          this.list_of_result.answers_list[i][4] = false;
        }
      }
      if (this.resultText === 'Hide Details') {
        for (let i = 3; i < this.list_of_result.answers_list.length; i++) {
          this.list_of_result.answers_list[i][4] = true;
        }
      }
    }
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


/* .slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateX(-100%);
}

.slide-enter-active,
.slide-leave-active {
  transition: 0.3s ease-out;
} */

.slide-enter-active,
.slide-leave-active {
  transition: all .5s;
}

.slide-enter,
.slide-leave-to {
  transform: translateY(-100%);
}
</style>
