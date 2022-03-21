<template>
  <div>
    <b-avatar
      button
      v-b-toggle.collapse-1
      variant="primary"
      class="mb-3"
      :src="avatarURL"
      size="120"
    >
    </b-avatar>
    <b-collapse id="collapse-1">
      <b-form-input
        id="avatar-input"
        v-model="avatarURL"
        placeholder="Upload an avatar link..."
      ></b-form-input>
    </b-collapse>
  </div>
</template>

<script>
export default {
  name: 'changeAvatar.vue',
  props: {
    value: String,
  },
  computed: {
    avatarURL: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit('input', value);
      },
    },
  },
};
</script>

<style scoped>

#avatar-input {
  background-color: lightblue;
  margin-bottom: 0.5rem;
}

</style>
