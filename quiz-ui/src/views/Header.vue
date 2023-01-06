<template>
  <div class="container-fluid p-0">
    <div class="row">
      <div class="col">
        <nav class="navbar navbar-dark bg-primary text-center">
          <div class="col">
            <a class="navbar-brand rounded p-2" href="#">FullSport Quiz !</a>
          </div>

          <div class="col">
            <ul class="navbar-nav">
              <div class="row">
                <div class="col-2 offset-3">
                  <li class="nav-item">
                    <a class="nav-link text-white rounded" href="/">HomePage</a>
                  </li>
                </div>

                <div class="col-2">
                  <li class="nav-item">
                    <a class="nav-link text-white rounded" href="/admin"
                      >Administration</a
                    >
                  </li>
                </div>
              </div>
            </ul>
          </div>
        </nav>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "Header",
  data() {
    return {};
  },

  async created() {},
};
</script>
