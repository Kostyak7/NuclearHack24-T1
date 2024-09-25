<template>
  <button class="button" type="button">
    <slot>

    </slot>
  </button>
</template>

<script>
export default {
  name: "button-a"
}
</script>

<style lang="sass">

.button
    background: $blue
    border-radius: 0px 20px 20px 20px
    padding: 18px 26px
    color: black
    border: var(--border)
    &:focus
        outline: none

@media (min-width: 768px)
    .button
        padding: 22px 40px
        &:hover
            background: $light-blue


</style>