<script setup lang="ts" generic="T extends Object">
  import { ref, nextTick, computed, type Ref } from 'vue'

  type TableHeader = {
    title: string,
    key: keyof T,
    sortable?: boolean,
    useInForm: boolean
  }

  const props = defineProps<{
    title: string,
    loading: boolean,
    items: T[],
    defaultItem: T,
    headers: TableHeader[],
    sortBy: Sorting[]
  }>()

  const emit = defineEmits<{
    createItem: [item: T],
    editItem: [item: T],
    deleteItem: [item: T],
    fetchItems: [search: string, pageNumber: number, itemsPerPage: number, sortBy: Sorting[]],
  }>()

  const numItems = computed(() => {return props.items.length})
  const itemsPerPage = ref(10);
  const pageNumber = ref(0);
  const tempSearch = ref("");  // Contents of search bar
  const search = ref("");  // Final contents of search bar when enter is pressed

  // CRUD
  const inputItem = ref(props.defaultItem) as Ref<T>;  // Holds the message being created/edited/deleted
  const formTitle = computed(() => {return editing ? 'Edit Message' : "New Message"})
  const formEntries = computed(() => {return props.headers.filter(h => h.useInForm)});
  const isCreationDialogueOpen = ref(false);
  const isDeletionDialogueOpen = ref(false);
  const editing = ref(false);


  // Create or edit an item
  function editItem(item: T) {
    editing.value = true;
    inputItem.value = Object.assign({}, item)
    isCreationDialogueOpen.value = true
  }

  async function confirmCreationDialogue() {
    if (editing.value) {
      emit('editItem', inputItem.value);
    } else {
      emit('createItem', inputItem.value);
    }
    closeCreationDialogue();
  }

  function closeCreationDialogue() {
    editing.value = false;
    isCreationDialogueOpen.value = false
    nextTick(() => {
      loadItems();
      inputItem.value = Object.assign({}, props.defaultItem)
    })
  }

  // Delete an item
  function deleteItem(item: T) {
    inputItem.value = Object.assign({}, item)
    isDeletionDialogueOpen.value = true
  }

  function confirmDeletionDialogue() {
    emit('deleteItem', inputItem.value);
    closeDeletionDialogue();
  }

  function closeDeletionDialogue() {
    isDeletionDialogueOpen.value = false;
    nextTick(() => {
      loadItems();
      inputItem.value = Object.assign({}, props.defaultItem)
    })
  }

  // Search
  function updateSearch() {
    search.value = tempSearch.value
  }

  function loadItems() {
    emit('fetchItems', search.value, pageNumber.value, itemsPerPage.value, props.sortBy)
  }
</script>

<template>
  <v-data-table-server
    :items-length="numItems"
    :items="props.items"
    v-model:items-per-page="itemsPerPage"
    v-model:sort-by="props.sortBy"
    :page="pageNumber"
    :headers="headers"
    :loading="props.loading"
    :search="search"
    class="elevation-1"
    item-value="id"
    @update:options="loadItems"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>{{ title }}</v-toolbar-title>
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
        <v-dialog v-model="isCreationDialogueOpen" max-width="500px">
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
                  <v-col v-for="entry in formEntries">
                    <v-text-field
                      v-model="inputItem[entry.key]"
                      :label="entry.title"
                    >
                    </v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue-darken-1" variant="text" @click="closeCreationDialogue">
                Cancel
              </v-btn>
              <v-btn color="blue-darken-1" variant="text" @click="confirmCreationDialogue">
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-dialog v-model="isDeletionDialogueOpen" max-width="500px">
          <v-card>
            <v-card-title class="text-h5"
              >Are you sure you want to delete this item?</v-card-title
            >
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="blue-darken-1"
                variant="text"
                @click="closeDeletionDialogue"
              >
                Cancel
              </v-btn>
              <v-btn
                color="blue-darken-1"
                variant="text"
                @click="confirmDeletionDialogue"
              >
                OK
              </v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon size="small" class="me-2" @click="editItem(item)" icon="mdi-pencil"></v-icon>
      <v-icon size="small" @click="deleteItem(item)" icon="mdi-delete"></v-icon>
      <slot name="actions" :input="item"></slot>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="loadItems"> Load Messages </v-btn>
    </template>
  </v-data-table-server>
</template>
