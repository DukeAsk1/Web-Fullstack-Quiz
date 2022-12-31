<template>
  <div class="about">
    <h1>This is the admin page</h1>
  </div>

  <div>
    <p>Enter Admin Password :</p>
    <input type="text" v-model="password" id="name" name="name" size="10">
    <button class="btn btn-success" type="button" @click="loginPlayer">Connexion</button>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";
import quizApiService from "@/services/QuizApiService";
export default {
  name: "Admin",
  data() {
    return {
      password: '',
      token: null,
    };
  },
  components: {

  },
  async created() {
    this.token = participationStorageService.getToken();
    this.updateQuestionList()
  },
  methods: {
    async loginPlayer() {
      let login_info = quizApiService.login(this.password);
      let login_result = await login_info;
      if (login_result) {
        participationStorageService.saveToken(login_result.data.token)
        this.token = login_result.data.token
      }
    },
  }
}
</script>



