<template>

  <div class="accordion__item">
    <button class="accordion__item-header" @click="click_accordion">
      <div>{{ $props.faq.title }}</div>
      <div class="accordion__toggle">
        <div class="accordion__line-wrapper" :class="{'accordion__line-wrapper_active': isActive}">
          <div class="accordion__line-1"></div>
          <div class="accordion__line-2"></div>
        </div>
      </div>
    </button>
    <div class="accordion__item-content" :class="{'accordion__item-content_active': isActive}">
      <div class="accordion__text">{{ $props.faq.text }}</div>
    </div>
  </div>

</template>

<script>
export default {
  name: "accordion-item-a",
  props: {
    faq: {
      type: Object,
      required: true,
      default: {
        title: 'Почему мне хочется пиццы?',
        text: 'Она очень вкусная!!!',
      }
    },
  },
  data() {
    return {
      isActive: false,
    }
  },
  methods: {
    click_accordion() {
      this.isActive = !this.isActive;
    }
  }
}
</script>

<style scoped lang="sass">

</style>