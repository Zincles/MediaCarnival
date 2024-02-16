<template>
  <div class="text-white">
    {{ libraries }}

    <q-list bordered separator v-for="library in libraries?.libraries" :key="library.id">
      <!-- <q-card class="q-ma-md" style="max-width: 400px"> -->
      <q-item class="text-h6 text-white">{{ library.library_name }}</q-item>
      <!-- </q-card> -->
    </q-list>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import apiUrls from 'src/apiUrls';
import { GetMediaLibraryResponse } from 'src/components/models';

import { ref } from 'vue';

const libraries = ref<GetMediaLibraryResponse>();

//调用API
axios
  .get<GetMediaLibraryResponse>(apiUrls.getMediaLibraries, {})
  .then((response) => {
    libraries.value = response.data;
    console.log(libraries);
  })
  .catch((error) => {
    console.log(error);
  });
</script>
```
