<template>
  <ul>
    Page for question Modifier
  </ul>
  <div v-if="action === 'newQuestion'">
    <label for="name-input">IMPORT QUESTION FROM JSON FILE:</label>
    <input type="file" accept=".json" v-on:change="import_json">
  </div>
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
      <img :src="'data:image/jpeg;base64,' + question.image" ref="image" @change="convertToImage" />
      <input type="file" placeholder="Image" accept="image/*" @change="convertToBase64">
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
              <option selected value=0>False</option>
              <option value=1>True</option>
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
              <option selected value=0>False</option>
              <option value=1>True</option>
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
              <option selected value=0>False</option>
              <option value=1>True</option>
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
              <option selected value=0>False</option>
              <option value=1>True</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </form>
  <button class="btn btn-success" @click="save">Save</button>
</template>

<script>
export default {
  name: "QuestionModifier",
  props: {
    question: {
      type: Object
    },
    action: "",
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
      base64Image: '',
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
          this.question.image = this.base64Image.substring(23);
          console.log('size of base string', this.base64Image.substring(23).length)
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
        image: this.question.image,
        possibleAnswers: this.updatedAnswersArray
      })
      console.log('base 64', this.base64Image);
      console.log("POSSIBLE ANSWERSSSSS", this.updatedAnswersArray);
    },
    import_json(event) {

      const file = event.target.files[0];

      if (!file) {
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        const json = JSON.parse(e.target.result);
        // Do something with the JSON data here
        this.question.position = json.position;
        this.question.image = json.image;
        this.question.text = json.text;
        this.question.title = json.title;
        this.question.possibleAnswers = json.possibleAnswers;

        // console.log(this.question.possibleAnswers)

        for (let i = 0; i < this.question.possibleAnswers.length; i++) {
          console.log("index i in answers", this.question.possibleAnswers[i]);
          if (this.question.possibleAnswers[i].isCorrect === true) {
            this.question.possibleAnswers[i].isCorrect = 1;
          }
          else if (this.question.possibleAnswers[i].isCorrect === false) {
            this.question.possibleAnswers[i].isCorrect = 0;
          }
        }
        const [answer_1, answer_2, answer_3, answer_4] = this.question.possibleAnswers;
        this.answer_1 = answer_1;
        this.answer_2 = answer_2;
        this.answer_3 = answer_3;
        this.answer_4 = answer_4;
        // this.updatedAnswersArray.push(answer_1);
        // this.updatedAnswersArray.push(answer_2);
        // this.updatedAnswersArray.push(answer_3);
        // this.updatedAnswersArray.push(answer_4);


        console.log("Answer Array JSON upload", this.updatedAnswersArray);
        // {
        // "id": 1,
        // "position": 1,
        // "text": "What team won the NBA Championship in 2020?",
        // "title": "NBA",
        // "possibleAnswers": [
        // {"text": "Los Angeles Lakers", "isCorrect": true},
        // {"text": "Golden State Warriors", "isCorrect": false},
        // {"text": "Boston Celtics", "isCorrect": false},
        // {"text": "Houston Rockets", "isCorrect": false}
        // ]
        // }
      };
      reader.readAsText(file);

    }
  }
}
</script>