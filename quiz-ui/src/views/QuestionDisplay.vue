<template>
  <div class="container">
    <div class="card mb-3 col-10 offset-1">
      <div class="row">
        <div class="col">
          <img v-if="question.image" :src="question.image" />
        </div>

        <div class="col">
          <div class="card-body">
            <div class="row row gy-5">
              <div class="col-fluid">
                <h3 class="card-title">{{ question.title }}</h3>
              </div>

              <div class="col-fluid">
                <h5 class="card-subtitle">{{ question.text }}</h5>
              </div>

              <div class="col">
                <div class="row">
                  <p class="card-text">
                    <small class="text-muted">Choose one of the answers below</small>
                  </p>
                </div>

                <div class="row justify-content-center">
                  <div v-for="(value, index) in question.possibleAnswers" @click="$emit('answer-selected', index)"
                    class="col">
                    <input type="radio" v-model="selected" :value="value" name="radAnswer" />
                    {{ value.text }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuestionDisplay",
  props: {
    question: {
      type: Object,
    },
    emits: ["answer-selected"],
    // created() {
    //   this.$emit('answer-selected', 2);
    // },
  },
};
</script>
