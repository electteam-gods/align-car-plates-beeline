<script setup lang="ts">
import { FileUploadUploadEvent } from "primevue/fileupload";
import Panel from "primevue/panel";
import { ref } from "vue";

const results = ref<
  {
    task_id: string;
    result_url: string;
    status: string;
  }[]
>([]);

const upload = (e: FileUploadUploadEvent) => {
  const data = JSON.parse(e.xhr.responseText);
  results.value.push(...data.list);
};
</script>

<template>
  <div>
    <div class="container mx-auto my-8 flex justify-center">
      <h1 class="text-2xl">Ellecteam</h1>
    </div>

    <div
      class="container mx-auto flex flex-col items-stretch justify-center gap-4 lg:flex-row"
    >
      <div class="flex-1 p-4">
        <FileUpload
          name="files"
          @upload="upload($event)"
          url="/api/process"
          :multiple="true"
          accept="image/*"
          auto
          :maxFileSize="1000000"
        >
          <template #empty>
            <span>Drag and drop files to here to upload.</span>
          </template>
        </FileUpload>
      </div>
      <div class="flex-1 p-4">
        <Panel header="Результаты">
          <div v-for="result in results" class="mb-4">
            <p>{{ result.task_id }}</p>
            <img :src="result.result_url" alt="" />
          </div>
        </Panel>
      </div>
    </div>
  </div>
</template>
