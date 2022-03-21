<template>
     <b-avatar button @click="onClick" :src="profLogo" size="50" ></b-avatar>
</template>

<script>
export default {
  name: 'AvatarButton',
  props: {
    profLogo: String,
  },
  methods: {
    onClick() {
    },
  },
};
</script>

<style scoped>

</style>
