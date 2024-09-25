<template>
  <section class="main-sect" id="MainSect">
            <div class="container">
                <h1 class="main-sect__main-thing">Добавляй содержание в свои PDF, <span>быстро <span class="nowrap">и бесплатно!</span></span></h1>
                <button-a class="main-sect__button" @click="$router.push({name: 'form-page-default'})">Начать магию</button-a>
            </div>
            <pets-container-a></pets-container-a>
        </section>
</template>

<script>
import PetsContainerA from "@/components/PetsContainerA";

export default {
  name: "main-sect-a",
  components: {PetsContainerA}
}
</script>

<style lang="sass">

.main-sect
    height: 100vh
    max-height: 900px
    min-height: 684px
    position: relative
    border-bottom: $main-border
    .container
        padding-top: $header-height
    &__main-thing
        margin-top: 2rem
        font-family: 'Roboto Slab', sans-serif
        font-size: 2.25rem
        font-style: normal
        font-weight: 400
        line-height: 1.35em
        padding-bottom: 1rem

.pets-container
    position: absolute
    top: 0
    right: 0
    height: 100%
    width: 100%
    overflow: hidden
    z-index: -1
    svg
        height: 100%
    &__super-huge
        position: absolute
        top: 370px
        right: -201px
        height: 650px
    &__huge-printer
        position: absolute
        display: none
    &__huge-yellow
        position: absolute
        display: none
    &__huge-orange
        position: absolute
        display: none

@media (min-width: 576px)
    .pets-container
        &__super-huge
            top: 300px
            height: 700px
        &__huge-yellow
            display: block
            bottom: -3px
            right: 320px
            height: 150px
            svg
                height: 100%

@media (min-width: 768px)
    .main-sect
        min-height: 1099px
        &__main-thing
            font-size: 3.375rem
            max-width: 700px
            margin-top: 3rem
    .pets-container
        &__super-huge
            height: auto
            right: -150px
        &__huge-yellow
            height: 200px
            right: 350px

@media (min-width: 992px)
    .main-sect
        max-height: 9000px
        min-height: 600px
        height: 100vh 
        &__main-thing
            margin-top: 5rem
    .pets-container
        &__super-huge
            top: auto
            bottom: -100px
            right: -200px
        &__huge-printer
            display: block
            bottom: 160px
            right: 190px
        &__huge-yellow
            right: 380px

@media (min-width: 1200px)
    .pets-container
        &__super-huge
            right: -150px
        &__huge-printer
            right: 240px
        &__huge-yellow
            right: 430px
        &__huge-orange
            display: block
            left: 0
            bottom: -80px

</style>