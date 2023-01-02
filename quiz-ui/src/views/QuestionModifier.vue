<template>
  <ul>
    Page for question Modifier
  </ul>
  <form>
    <div class="col">
      <label>Position</label>
      <input type="text" placeholder="Title" v-model="question.position">
    </div>
    <div class="col">
      <label>Title</label>
      <input type="text" placeholder="Title" v-model="question.title">
    </div>

    <div class="col">
      <label>Text</label>
      <input type="text" placeholder="Text" v-model="question.text">
    </div>

    <div class="col">
      <label>Image</label>
      <input type="file" placeholder="Image" ref="imageInput" accept="image/*" v-on:change="question.image"
        @change="convertToBase64">
    </div>

    <div class="col">
      <label>Answers</label>
      <div class='col'>
        <div>
          <label>Answer N°1</label>
          <div class="col">
            <label>Text</label>
            <input v-model="answer_1.text">
          </div>
          <div class="col">
            <label>Correct</label>
            <select class="form-select" v-model="answer_1.isCorrect">
              <option selected value=false>False</option>
              <option value=true>True</option>
            </select>
          </div>
        </div>
      </div>
      <div class='col'>
        <div>
          <label>Answer N°2</label>
          <div class="col">
            <label>Text</label>
            <input v-model="answer_2.text">
          </div>
          <div class="col">
            <label>Correct</label>
            <select class="form-select" v-model="answer_2.isCorrect">
              <option selected value=false>False</option>
              <option value=true>True</option>
            </select>
          </div>
        </div>
      </div>
      <div class='col'>
        <div>
          <label>Answer N°3</label>
          <div class="col">
            <label>Text</label>
            <input v-model="answer_3.text">
          </div>
          <div class="col">
            <label>Correct</label>
            <select class="form-select" v-model="answer_3.isCorrect">
              <option selected value=false>False</option>
              <option value=true>True</option>
            </select>
          </div>
        </div>
      </div>
      <div class='col'>
        <div>
          <label>Answer N°4</label>
          <div class="col">
            <label>Text</label>
            <input v-model="answer_4.text">
          </div>
          <div class="col">
            <label>Correct</label>
            <select class="form-select" v-model="answer_4.isCorrect">
              <option selected value=false>False</option>
              <option value=true>True</option>
            </select>
          </div>
        </div>
      </div>
    </div>
    <button class="btn btn-success" @click="save">Save</button>
  </form>
</template>

<script>
export default {
  name: "QuestionModifier",
  props: {
    question: {
      type: Object
    },
    emits: ["update:question"]
  },
  data() {
    console.log('in modifier windows')
    return {
      answer_1: {
        text: null,
        isCorrect: null
      },
      answer_2: {
        text: null,
        isCorrect: null
      },
      answer_3: {
        text: null,
        isCorrect: null
      },
      answer_4: {
        text: null,
        isCorrect: null
      },
      // base64Image: '',
      updatedAnswersArray: Array(),
    }
  },

  mounted() {
    // Destructure the first element from the names prop
    if (this.question.possibleAnswers) {
      const [answer_1, answer_2, answer_3, answer_4] = this.question.possibleAnswers;
      this.answer_1 = answer_1 ? answer_1 : { text: null, isCorrect: null }
      this.answer_2 = answer_2 ? answer_2 : { text: null, isCorrect: null }
      this.answer_3 = answer_3 ? answer_3 : { text: null, isCorrect: null }
      this.answer_4 = answer_4 ? answer_4 : { text: null, isCorrect: null }
    }

  },
  methods: {
    convertToBase64(event) {
      // Reference to the DOM input element
      const input = event.target
      // Ensure that you have a file before attempting to read it
      if (input.files && input.files[0]) {
        // create a new FileReader to read this image and convert to base64 format
        const reader = new FileReader()
        // Define a callback function to run, when FileReader finishes its job
        reader.onload = (e) => {
          // Note: arrow function used here, so that "this.base64Image" refers to the image data in Vue component
          // Read image as base64 and set to base64Image
          this.base64Image = e.target.result
        }
        // Start the reader job - read file as a data url (base64 format)
        reader.readAsDataURL(input.files[0])
      }
    },
    save() {

      if (this.answer_1.text) {
        this.updatedAnswersArray.push({
          text: this.answer_1.text,
          isCorrect: this.answer_1.isCorrect
        })
      }
      if (this.answer_2.text) {
        this.updatedAnswersArray.push({
          text: this.answer_2.text,
          isCorrect: this.answer_2.isCorrect
        })
      }
      if (this.answer_3.text) {
        this.updatedAnswersArray.push({
          text: this.answer_3.text,
          isCorrect: this.answer_3.isCorrect
        })
      }
      if (this.answer_4.text) {
        this.updatedAnswersArray.push({
          text: this.answer_4.text,
          isCorrect: this.answer_4.isCorrect
        })
      }
      this.$emit('update:question', {
        position: this.question.position,
        title: this.question.title,
        text: this.question.text,
        image: this.base64Image,
        possibleAnswers: this.updatedAnswersArray
      })
      console.log("POSSIBLE ANSWERSSSSS", this.updatedAnswersArray)
    },
  }
}

</script>