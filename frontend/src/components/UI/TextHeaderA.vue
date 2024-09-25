<template>
  <div class="text-header">
    <h2>
      <slot>

      </slot>
    </h2>
  </div>
</template>

<script>
export default {
  name: "text-header-a"
}
</script>

<style lang="sass">

.text-header
    position: relative
    width: auto
    h2
        display: inline-block
        text-align: center
        font-size: 24px
        font-weight: 400
        font-family: 'Roboto Slab', sans-serif
        position: relative
        width: 120px
        &::before
            content: ""
            z-index: -1
            position: absolute
            top: -20px
            right: 0
            background-image: url("@/assets/img/header-holder.svg")
            background-repeat: no-repeat
            height: 100px
            width: 100%

@media (min-width: 768px)
    .text-header
        h2
            font-size: 48px
            width: 190px
            &::before
                height: 170px
                width: 117%
                left: 0
                top: -30px
                background-size: cover
                background-image: url("@/assets/img/header-holder-comp.svg")
</style>