<template>
  <header-a class="header_scrolled"></header-a>
<div class="result-page">
        <div class="container">
            <img class="get-file-page__flower" src="@/assets/img/Flowers-form.svg" alt="">
            <img class="get-file-page__flower-desk" src="@/assets/img/Flowers-form-desk.svg" alt="">
        </div>
    </div>
</template>

<script>
import HeaderA from "@/components/HeaderA";

export default {
  name: "ResultPage",
  data() {
    return {
    }
  },
  components: { HeaderA },
  beforeMount() {
  }
}
</script>

<style lang="sass">

.result-page
    height: 100vh
    // align-items: center
    &__flower
        position: absolute
        bottom: 0
        right: 1.5rem
        z-index: -1
    &__flower-desk
        display: none
    & .container
        min-height: 100%
        position: relative
        display: flex
        padding-top: 15vh


@media (min-width: 1200px)
    .result-page
        min-height: 650px
        &__flower
            display: none
        &__flower-desk
            display: block
            height: 100%
            position: relative
            bottom: -18px
            margin-left: 10%
        & .container
            min-height: 520px
</style>