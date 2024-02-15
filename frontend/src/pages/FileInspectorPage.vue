<template>
  <div>
    {{ props.path.type }}
    <!-- <img src="" alt="file" /> -->
  </div>
</template>

<script setup lang="ts">
import { SubPath } from 'components/models';

let props = defineProps({
  path: {
    type: Object as () => SubPath,
    required: true,
  },
});
</script>
