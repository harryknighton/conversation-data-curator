<script setup lang="ts">
  import { defineComponent, ref, type Ref } from 'vue'

  const messages = ref([
    {id:1, content:'hello'},
  ])

  // async function getMessages() {
  //   try {
  //     const response = await axios.get('/user?ID=12345');
  //     messages.value = response;
  //   } catch (error) {
  //     console.error(error);
  //   }
  // }
</script>


<template>
  <h1>Messages</h1>
  <ul>
    <li v-for="message in messages" :key="message.id">
      {{ message.content }}
      <button>X</button>
    </li>
  </ul>
</template>
