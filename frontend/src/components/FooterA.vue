<template>
  <footer class="footer">
    <div class="container">
      <div class="footer__content-wrapper">
        <div class="footer__logo">
          <svg width="31" height="27" viewBox="0 0 31 27" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
                d="M30 6.10949L30 1L1 1L1 19.2482L5.06369 19.2482L5.06369 21.8942L1 21.8942L1 26L30 26L30 9.75912L7.55732 9.75912L7.55732 6.10949L30 6.10949Z"
                stroke="black"/>
          </svg>
          <div class="footer__logo-text">Table of Content</div>
        </div>
        <ul class="list footer__nav">
          <li class="">
             <router-link :to="{name: 'main-page'}" v-scroll-to="{el: '#AboutUs', offset: -105}">О нас</router-link>
          </li>
          <li class="">
            <router-link :to="{name: 'main-page'}" v-scroll-to="{el: '#FAQ', offset: -120}">Вопросы</router-link>
          </li>
          <li class="">
            <a href="#">Поддержка</a>
          </li>
        </ul>
        <ul class="list">
          <li class="">
            <a href="#">+7 (000) 000 - 00 - 00</a>
          </li>
          <li class="">
            <a href="#">tabloc@hello.com</a>
          </li>
        </ul>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "footer-a",
  props: {}
}
</script>

<style lang="sass">
.list
    display: inline-block
    padding: 0
    margin: 0
    list-style-type: none
    li
        a
            color: #000

.footer
    justify-content: space-between
    margin-top: 8rem
    padding: 5rem 0
    background-color: $light-blue
    border-top: var(--border)
    &__content-wrapper
        display: flex
        flex-wrap: wrap
    &__nav
        margin-right: 40px
        margin-bottom: 40px
    &__logo
        width: 100%
        margin-bottom: 40px
        &-text
            margin-left: 10px
            display: inline-block
        svg
            display: inline-block

@media (min-width: 768px)
    .footer
        &__logo
            width: auto
        &__content-wrapper
            justify-content: space-between
</style>