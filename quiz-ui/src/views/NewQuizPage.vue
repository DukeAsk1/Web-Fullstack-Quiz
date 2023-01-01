<template>
  <div class="newQuizPage">
    <h1>This is a new quiz view page</h1>
  </div>
  <h1>New Quiz Page</h1>

  <p> Saisissez votre nom :
    <input type="text" v-model="username" id="name" name="name" size="10">
    <button class="btn btn-success" @click="launchNewQuiz"> GO!</button>
  </p>
  <p>{{ playerName }}</p>
</template>

<style>
@media (min-width: 1024px) {
  .newQuizPage {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>

<script>
import participationStorageService from "@/services/ParticipationStorageService";
export default {
  name: "HomePage",
  data() {
    return {
      username: ''
    };

  },
  methods: {
    buttonClickHandler() {
      console.log('Compute playerName');
      this.username = this.data.username;
    },
    launchNewQuiz() {
      participationStorageService.savePlayerName(this.username.toString());
      const playerName = participationStorageService.getPlayerName();
      console.log("Launch new quiz with " + playerName);
      // this.$router.push('/questions');
    }
  }
}

</script>