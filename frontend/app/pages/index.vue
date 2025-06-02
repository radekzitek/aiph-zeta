<template>
  <div>
    <h1>Users</h1>
    <div v-if="loading">Loading...</div>
    <div v-if="error" style="color: red;">{{ error }}</div>
    <ul v-if="users.length">
      <li v-for="user in users" :key="user.id">{{ user.name }} ({{ user.email }})</li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

// Define reactive state
const users = ref<any[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

// Access the Nuxt application context to get our injected $api service
const { $api } = useNuxtApp();

// Define a function to fetch data
async function fetchUsers() {
  loading.value = true;
  error.value = null;
  try {
    // Use the $api service to make a GET request.
    // This will call: GET /api/v1/users
    const response = await $api.get('/users/');
    users.value = response.data;
  } catch (err: any) {
    console.error('Failed to fetch users:', err);
    error.value = 'Failed to load user data.';
  } finally {
    loading.value = false;
  }
}

// Call the function when the component is mounted
onMounted(() => {
  fetchUsers();
});
</script>