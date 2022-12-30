import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import QuizPage from '../views/NewQuizPage.vue'
import QuestionDisplay from '../views/QuestionDisplay.vue'
import QuestionsManager from '../views/QuestionsManager.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/new-quiz-page',
      name: 'QuizPage',
      component: QuizPage
    },
    {
      path: '/questions-manager',
      name: 'questions-manager',
      component: QuestionsManager
    },
    {
      path: '/question-display',
      name: 'question-display',
      component: QuestionDisplay
    },
    {
      path: '/result',
      name: 'result',
      component: ResultPage
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
