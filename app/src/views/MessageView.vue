<script setup lang="ts">
  import { ref, type Ref, nextTick } from 'vue'
  import axios from 'axios'
  import { VDataTableServer } from 'vuetify/labs/VDataTable'
import { computed } from 'vue';

  declare var require: any

  const messages = ref<{id: number, content: string}[]>([]);
  const messagesPerPage = ref(10);
  const pageNumber = ref(0);
  const headers = ref([
    { title: 'ID', key: 'id',  align: 'start' },
    { title: 'Content', key: 'content', align: 'start' },
    { title: 'Actions', key: 'actions', sortable: false }
  ]);
  const sortBy = ref([{key: 'id', order: 'asc'}]);
  const tempSearch = ref("");  // Contents of search bar
  const search = ref("");  // Final contents of search bar when enter is pressed
  const loading = ref(false);
  const isMessageDialogueOpen = ref(false);
  const isDeleteDialogueOpen = ref(false);
  const editIndex = ref(-1);
  const inputMessage: Ref<Message> = ref({  // Hold the message input through the message dialogue
    id: -1,
    content: ""
  })
  const defaultMessage: Ref<Message> = ref({  // Default to restore the input message to
    id: -1,
    content: ""
  })
  const editing = computed(() => {return editIndex.value !== -1})
  const formTitle = computed(() => {return editing ? 'Edit Message' : "New Message"})

  // Create or edit a message
  function editMessage(message: Message) {
    editIndex.value = messages.value.indexOf(message)
    inputMessage.value = Object.assign({}, message)
    isMessageDialogueOpen.value = true
  }

  async function confirmMessageDialogue() {
    if (editing.value) {
      updateDBMessage(inputMessage.value)
      Object.assign(messages.value[editIndex.value], inputMessage.value)
    } else {
      let createdMessage = await createDBMessage(inputMessage.value);
      messages.value.push(createdMessage);
    }
    closeMessageDialogue();
  }

  function closeMessageDialogue() {
    isMessageDialogueOpen.value = false
    nextTick(() => {
      inputMessage.value = Object.assign({}, defaultMessage.value)
      editIndex.value = -1
    })
  }

  // Delete a message
  function deleteMessage(message: Message) {
    editIndex.value = messages.value.indexOf(message)
    inputMessage.value = Object.assign({}, message)
    isDeleteDialogueOpen.value = true
  }

  function confirmDeleteDialogue() {
    deleteDBMessage(inputMessage.value)
    messages.value.splice(editIndex.value, 1);
    closeDeleteDialogue();
  }

  function closeDeleteDialogue() {
    isDeleteDialogueOpen.value = false;
    nextTick(() => {
      inputMessage.value = Object.assign({}, defaultMessage.value)
      editIndex.value = -1
    })
  }

  // Annotate a message [Not implemented]
  function annotateMessage(item: Message) {

  }

  // Search
  function updateSearch() {
    search.value = tempSearch.value
  }

  // Database CRUD operations
  async function createDBMessage(message: Message) : Promise<Message> {
    const args = { ...message } as Partial<Message>;
    delete args.id;
    let response = await axios.post('http://127.0.0.1:8000/messages/create', { ...args })
      .catch((error: any) => {
        console.error(error);
      })
    if (response && response.status == 200) {
      return response.data as Message;
    } else {
      return {id: -1, content: ""}
    }

  }

  async function getDBMessages() {
    loading.value = true;
    let params = {
      search: search.value,
      limit: messagesPerPage.value,
      offset: messagesPerPage.value * pageNumber.value,
      sort_by: sortBy.value.length > 0 ? sortBy.value[0].key : 'id',
      sort_asc: sortBy.value.length > 0 ? sortBy.value[0].order === 'asc': 'asc',
    }
    axios.get('http://127.0.0.1:8000/messages', { params })
      .then((response: {data: {id: number, content: string}[]}) => {
        messages.value = response.data;
      })
      .catch((error: any) => {
        console.error(error);
      })
      .finally(() => {
        loading.value = false;
      })
  };

  async function deleteDBMessage(message: Message) {
    axios.post('http://127.0.0.1:8000/messages/delete', { id: message.id })
      .catch((error: any) => {
        console.error(error);
    })
  }

  async function updateDBMessage(message: Message) {
    axios.post('http://127.0.0.1:8000/messages/update', { ...message })
      .catch((error: any) => {
        console.error(error);
      })

  }

  function annotateDBMessage(message: Message) {

  }
</script>


<template>
  <v-data-table-server
    v-model:items-per-page="messagesPerPage"
    v-model:sort-by="sortBy"
    :page="pageNumber"
    :headers="headers"
    :items-length="messages.length"
    :items="messages"
    :loading="loading"
    :search="search"
    class="elevation-1"
    item-value="name"
    @update:options="getDBMessages"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>All Datasets</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="tempSearch"
          @keydown.enter="updateSearch"
          append-icon="mdi-magnify"
          label="Press Enter to Search"
          single-line
          hide-details
        ></v-text-field>
        <v-dialog v-model="isMessageDialogueOpen" max-width="500px">
          <template v-slot:activator="{ props }">
            <v-btn color="primary" dark class="mb-2" v-bind="props">
              New Message
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="text-h5">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-text-field
                    v-model="inputMessage.content"
                    label="Content"
                  ></v-text-field>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue-darken-1" variant="text" @click="closeMessageDialogue">
                Cancel
              </v-btn>
              <v-btn color="blue-darken-1" variant="text" @click="confirmMessageDialogue">
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-dialog v-model="isDeleteDialogueOpen" max-width="500px">
          <v-card>
            <v-card-title class="text-h5"
              >Are you sure you want to delete this item?</v-card-title
            >
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue-darken-1" variant="text" @click="closeDeleteDialogue"
                >Cancel</v-btn
              >
              <v-btn
                color="blue-darken-1"
                variant="text"
                @click="confirmDeleteDialogue"
                >OK</v-btn
              >
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon size="small" class="me-2" @click="editMessage(item)" icon="mdi-pencil"></v-icon>
      <v-icon size="small" @click="annotateMessage(item)" icon="mdi-clipboard-edit"></v-icon>
      <v-icon size="small" @click="deleteMessage(item)" icon="mdi-delete"></v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="getDBMessages"> Load Messages </v-btn>
    </template>
  </v-data-table-server>
</template>
