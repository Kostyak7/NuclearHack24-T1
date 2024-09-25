<template>
  <header class="header" :class="{ 'header_scrolled': !view.topOfPage}">
    <div class="container">
      <nav>
        <div class="navbar">
          <router-link class="navbar__logo" :to="{name: 'main-page'}" v-scroll-to="'#MainSect'">
            <svg width="29" height="25" viewBox="0 0 57 49" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M56 10.6058V1H1V35.3066H8.70701V40.281H1V48H56V17.4672H13.4363V10.6058H56Z" stroke="black"
                    stroke-width="2"/>
            </svg>
            <div class="navbar__logo-text">Table of Content</div>
          </router-link>
          <button class="navbar__toggle"
                  @click="click_toggle"
                  :class="{'navbar__toggle_active': view.isToggleOpen}">
            <div class="navbar__togline navbar__togline_1"></div>
            <div class="navbar__togline navbar__togline_2"></div>
            <div class="navbar__togline navbar__togline_3"></div>
          </button>
          <ul class="nav" :class="{'nav__active': view.isToggleOpen}">
            <li class="nav__item">
              <router-link :to="{name: 'main-page'}" v-scroll-to="{el: '#AboutUs', offset: -105}">О нас</router-link>
            </li>
            <li class="nav__item">
              <router-link :to="{name: 'main-page'}" v-scroll-to="{el: '#FAQ', offset: -120}">Вопросы</router-link>
            </li>
          </ul>
        </div>
      </nav>
    </div>
  </header>
</template>

<script>
export default {
  name: "header-a",
  data() {
    return {
      view: {
        topOfPage: true,
        isToggleOpen: false,
      }
    }
  },
  props: {},
  beforeMount() {
    window.addEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      if (window.pageYOffset > 0) {
        if (this.view.topOfPage) this.view.topOfPage = false;
      } else {
        if (!this.view.topOfPage && !this.view.isToggleOpen) this.view.topOfPage = true;
      }
    },
    click_toggle() {
      console.log(this.view.isToggleOpen);
      this.view.isToggleOpen = !this.view.isToggleOpen;
      if (this.view.isToggleOpen) {
        this.view.topOfPage = false;
      } else {
        this.handleScroll();
      }
    },
  }
}
</script>


<style lang="sass">
.header
    position: fixed
    z-index: 2000
    width: 100%
    border-bottom: none
    transition: background-color .2s, border-color .2s
    &_scrolled
        background-color: $light-blue
        border-bottom: $main-border

.navbar
    display: flex
    flex-wrap: wrap
    align-items: center
    justify-content: space-between
    a
        text-decoration: none
        color: black
    &__name
        a:hover
            text-decoration: none
            color: black
    &__toggle
        display: none
    &__logo
        display: flex
        align-items: center
        height: $header-height
        &-text
            padding-left: 1rem

.nav
    list-style-type: none
    padding: 0
    margin: 0
    display: flex
    &__item
        padding: 0 2rem
        &:last-child
            padding-right: 0
        a
            padding: 0.5rem

@media (max-width: 768px)
    .navbar
        &__toggle
            display: block
            border: none
            padding: 1rem 0
            background-color: rgba(0, 0, 0, 0)
            outline: 0 !important
            &_active
                .navbar__togline
                    &_1
                        transform: translateY(1.5px) rotate(45deg)
                    &_2
                        background-color: rgba(0, 0, 0, 0)
                    &_3
                        transform: translateY(-1.5px) rotate(-45deg)
        &__togline
            height: 1.5px
            width: 20px
            background-color: black
            &_1
                transform: translateY(-5px)
            &_3
                transform: translateY(5px)

    .nav
        width: 100%
        padding: 0
        flex-wrap: wrap
        overflow: hidden
        height: 0
        //transition: all .2s ease
        &__active
          height: 30%
        &__item
            padding: 0
            width: 100%
            &:last-child
                margin-bottom: 0.5rem
            &:first-child
                margin-top: 0.5rem
            a
                display: block
                padding: 0.5rem 0


</style>