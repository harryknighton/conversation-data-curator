<script setup lang="ts">
  import { ref, type Ref } from 'vue'
  import axios from 'axios'
  import CRUDTable from '../components/CRUDTable.vue'
  import { API_URL } from '@/main';
  import router from '@/router';

  const messages: Ref<Message[]> = ref([]);
  const headers = ref([
    { title: 'ID', key: 'id',  align: 'start', useInForm: false },
    { title: 'Content', key: 'content', align: 'start', useInForm: true },
    { title: 'Actions', key: 'actions', sortable: false, useInForm: false }
  ]);
  const loading = ref(false);
  const title = "All Datasets"
  const sortBy = ref([{key: 'id', order: 'asc'}]);
  const defaultMessage: Message = {  // Default to restore the input message to
    id: -1,
    content: ""
  }


  // Database CRUD operations
  function createMessage(message: Message) : void {
    axios.post(API_URL + 'messages/create/', { content: message.content })
      .then((response: { data: Message }) => {
        messages.value.push(response.data);
      })
      .catch((error: any) => {
        console.error(error);
      })
  }

  async function getMessages(search: string, pageNumber: number, itemsPerPage: number, sortBy: Sorting[]) {
    loading.value = true;
    let params = {
      search: search,
      limit: itemsPerPage,
      offset: itemsPerPage * pageNumber,
      sort_by: sortBy.length > 0 ? sortBy[0].key : 'id',
      sort_asc: sortBy.length > 0 ? sortBy[0].order === 'asc': 'asc',
    }
    axios.get(API_URL + 'messages/', { params })
      .then(
        (response: {data: Message[]}) => {messages.value = response.data},
        () => {messages.value = []}
      )
      .catch((error: any) => {
        console.error(error);
      })
      .finally(() => {loading.value = false;})
  };

  async function deleteMessage(message: Message) {
    axios.post(API_URL + 'messages/delete/', { id: message.id })
      .then(() => {
        messages.value.splice(messages.value.indexOf(message), 1);
      })
      .catch((error: any) => {
        console.error(error);
    })

  }

  async function updateMessage(message: Message) {
    const messageIndex = messages.value.findIndex(item => item.id === message.id);
    messages.value[messageIndex] = message
    axios.post(API_URL + 'messages/update/', { ...message })
      .catch((error: any) => {
        console.error(error);
      })
  }

  function annotateMessage(message: Message) {
    router.push({ name: 'annotations', params: {messageID: message.id}})
  }
</script>


<template>
  <CRUDTable
    @createItem="createMessage"
    @fetchItems="getMessages"
    @editItem="updateMessage"
    @deleteItem="deleteMessage"
    :items="messages"
    :title="title"
    :headers="headers"
    :loading="loading"
    :defaultItem="defaultMessage"
    :sortBy="sortBy"
  >
  <template #actions="actionProps : { input: Message }">
    <v-icon size="small" @click="annotateMessage(actionProps.input)" icon="mdi-clipboard"></v-icon>
  </template>
  </CRUDTable>
</template>
