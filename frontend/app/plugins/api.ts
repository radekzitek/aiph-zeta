// plugins/api.ts

import apiService from '~/services/apiService';

export default defineNuxtPlugin(nuxtApp => {
  // The 'provide' helper automatically makes this available
  // throughout your app with a '$' prefix.
  // So you can access it as `$api`
  nuxtApp.provide('api', apiService);
});