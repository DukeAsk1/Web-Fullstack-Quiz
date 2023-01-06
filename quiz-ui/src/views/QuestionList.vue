<template>
  <ul>
    <div class="row">
      <div class="col">
        <div class="row gy-4">
          <div class="container">
            <div class="row g-5">
              <div
                class="col-4 offset-1"
                v-for="question in list_of_question"
                :key="question"
              >
                <div class="card p-4 rounded-4">
                  <div class="row gy-4">
                    <div class="col-12">
                      <h4>Question : {{ question.text }}</h4>
                    </div>

                    <div class="col-12">
                      <div class="row">
                        <div class="col-6">
                          <img :src="question.image" />
                        </div>
                        <div class="col-6">
                          Position : {{ question.position }} <br />
                          <div
                            class="col-fluid"
                            v-for="answer in question.possibleAnswers"
                            :key="answer"
                          >
                            Answer : {{ answer.text }} Value :
                            {{ answer.isCorrect }}
                          </div>
                        </div>
                      </div>
                    </div>

                    <div class="col text-center">
                      <button
                        @click="$emit('modify', question.position)"
                        class="btn btn-warning"
                      >
                        Modify
                      </button>
                    </div>
                    <div class="col text-center">
                      <button
                        @click="$emit('delete', question.id)"
                        class="btn btn-danger"
                      >
                        Suppress
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- <li v-for="question in list_of_question">
      {{ question.position }} /
      {{ question.text }}
      {{ question.possibleAnswers }} -->

    <!-- </li> -->
  </ul>
</template>

<script>
export default {
  name: "QuestionList",
  data() {
    return {
      questions: Array(),
    };
  },
  props: {
    list_of_question: {
      type: Object,
    },
    emits: ["modify", "delete"],
  },
};
</script>
