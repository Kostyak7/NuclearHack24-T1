<template>
  <section class="about-us" id="AboutUs">
            <div class="about-us__flowers"></div>
            <div class="about-us__grass"></div>
            <div class="about-us__human"></div>
            <div class="about-us__printers">
                <div class="about-us__printer-1"></div>
                <div class="about-us__printer-2"></div>
                <div class="about-us__printer-3"></div>
                <div class="about-us__printer-4"></div>
                <div class="about-us__printer-5"></div>
            </div>
            <div class="container">
                <h2 class="about-us__header">Наш сервис — ваш <span class="about-us__header-hold">лучший друг</span></h2>
                <p class="about-us__story">
                    Мы — сервис по добавлению TOC в PDF файлы.<br>
                    Порой PDF файлы не имеют table of content (TOC), работа с такими файлами требует значительно больше ручного труда. 
                    И гораздо удобнее пользоваться ссылками и сразу переходить к странице с нужной темой.<br><br>

                    Наш сервис предоставляет возможность добавления ссылок и содержания в ваши PDF файлы.
                </p>
            </div>
        </section>
</template>

<script>
export default {
  name: "about-us-a",
}
</script>

<style scoped lang="sass">
.about-us
    height: 750px
    position: relative
    border-bottom: $main-border
    &__header
        font-family: 'Roboto Slab'
        font-style: normal
        font-weight: 400
        font-size: 24px
        line-height: 32px
        width: 220px
        margin: 4rem auto
        &-hold
            padding: 2rem 0
            background-image: url("@/assets/img/holder1.svg")
            background-repeat: no-repeat
            background-position: 75% 105%
    &__story
        padding-top: 4rem
        display: none
    &__grass
        position: absolute
        height: 264px
        bottom: 0
        left: 0
        width: 100%
        background: repeat-x url("@/assets/img/grass.svg")
    &__human
        position: absolute
        bottom: 100px
        left: 0
        height: 580px
        width: 218px
        background: no-repeat url("@/assets/img/human.svg")
    &__flowers
        position: absolute
        bottom: 110px
        right: 0
        height: 512px
        width: 147px
        background: no-repeat url("@/assets/img/flowers.svg")
    &__printers
        position: absolute
        bottom: 20px
        right: 0
        height: 300px
    &__printer
        &-1
            display: none
            position: relative
            background: no-repeat url("@/assets/img/printers/1.svg")
            background-size: contain
            width: 63px
            height: 128px
        &-2
            display: none
            position: relative
            background: no-repeat url("@/assets/img/printers/2.svg")
            background-size: contain
            width: 119px
            height: 87px
        &-3
            display: inline-block
            position: relative
            bottom: -80px
            right: -160px
            background: no-repeat url("@/assets/img/printers/3.svg")
            background-size: contain
            width: 108px
            height: 145px
        &-4
            display: inline-block
            position: relative
            bottom: -160px
            right: 30px
            background: no-repeat url("@/assets/img/printers/4.svg")
            background-size: contain
            width: 198px
            height: 103px
        &-5
            display: none
            position: relative
            background: no-repeat url("@/assets/img/printers/5.svg")
            background-size: contain
            width: 135px
            height: 100px

@media (min-width: 576px)
    .about-us__printer
        &-2
            display: inline-block
            bottom: -70px
            right: -70px



@media (min-width: 768px)
    .about-us
        &__header
            font-size: 38px
            margin: 4rem 0
            width: auto
            text-align: center
            padding-top: 3rem
            &-hold
                padding: 3rem 0
                background-image: url("@/assets/img/holder2.svg")
                background-position: 0
                background-size: 90%
        &__story
            display: block
            padding-right: 10%
            margin-left: 50%
        &__printer
            &-1
                display: inline-block
                bottom: -120px
                right: 40px
            &-2
                bottom: -140px
                right: 25px
            &-3
                right: -30px
            &-4
                right: 10px

@media (min-width: 992px)
    .about-us
        &__header
            font-size: 48px
        &__story
            padding-right: 15%
        &__printer
            &-5
                display: inline-block
                bottom: -120px
                right: 0

@media (min-width: 1200px)
    .about-us__printers
        right: 200px

@media (min-width: 1400px)
    .about-us__printers
        right: 400px
</style>