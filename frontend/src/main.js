// Denis Kotnik, May 2021

import Vue from 'vue'
import VueRouter from 'vue-router';
import VueAxios from 'vue-axios';
import axios from 'axios';

import App from './App.vue';
import Book from './components/Book.vue';
import Reservations from './components/Reservations.vue';
import ParkingSpots from './components/ParkingSpots.vue';

Vue.use(VueRouter);
Vue.use(VueAxios, axios);

import '../node_modules/bootstrap/dist/css/bootstrap.min.css';

Vue.config.productionTip = false;

const routes = [
  {
    name: 'Book',
    path: '/book',
    component: Book
  },
  {
    name: 'Reservations',
    path: '/reservations',
    component: Reservations
  },
  {
    name: 'ParkingSpots',
    path: '/parkingspots',
    component: ParkingSpots
  },
  {
    path: '/*',
    redirect: { name: 'ParkingSpots' }
  }
];

const router = new VueRouter({ mode: 'history', routes: routes });

new Vue({
  render: h => h(App),
  router
}).$mount('#app')