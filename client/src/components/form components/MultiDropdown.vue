<template>
  <multiselect
    v-model="selected"
    label="name"
    tag-placeholder="Add new tag"
    :placeholder="multiPlaceholder"
    track-by="code"
    :options="items"
    :multiple="multi"
    :taggable="true"
    @tag="addTag"
    class="dev_select"
  ></multiselect>
</template>

<script>
import Multiselect from 'vue-multiselect';

export default {
  name: 'MultiDropdown',
  components: {
    Multiselect,
  },
  props: {
    multiPlaceholder: String,
    items: null,
    multi: Boolean,
  },
  data() {
    return {
      selected: [],
      options: [
        { name: 'Stuff' },
      ],
    };
  },
  methods: {
    addTag(newTag) {
      const tag = {
        name: newTag,
        code: newTag.substring(0, 2) + Math.floor(Math.random() * 10000000),
      };
      this.options.push(tag);
      this.value.push(tag);
    },
  },
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
