<template>
    <header-a class="header_scrolled"></header-a>
  <div class="wait-page">
          <div class="container">
            <div class="processing-info-out">
            <div class="processing-info">
            <div class="processing-info-into">
                <p>Идет обработка...</p>
                <p>Прошло времени: {{ seconds }} сек</p>
            </div>
        </div>
    </div>

              <img class="get-file-page__flower" src="@/assets/img/Flowers-form.svg" alt="">
              <img class="get-file-page__flower-desk" src="@/assets/img/Flowers-form-desk.svg" alt="">
          </div>
      </div>  
</template>
  
  <script>
  import axios from "axios";
  import HeaderA from "@/components/HeaderA";
  
  export default {
    name: "wait-a",
    components: {HeaderA},
    data() {
      return {
        seconds: 0, 
        intervalId: null,  
        fileID: null,

        hostname: 'http://localhost:8000', // 'http://45.10.245.207:80'
      }
    },
    components: { HeaderA },
    mounted() {
        this.fileID = this.$route.params.fileID;

        this.intervalId = setInterval(() => {
            this.seconds++;
            this.fetchResult();
        }, 1000);
    },
    methods: {
        async fetchResult() {
            try {
                const response = await axios.get(this.hostname + `/v1/wait/${this.fileID}`);
                console.log(response.data);

                if (response.data.status === "ready") {
                    clearInterval(this.intervalId);
                    this.$router.push(`/v1/result/${this.fileID}`);

                }
            } catch (error) {
                console.error("Ошибка при запросе данных:", error);
            }
        }
    },
    beforeDestroy() {
        clearInterval(this.intervalId);
    }
  }
  </script>
  
<style lang="sass">
  
.wait-page
    height: 100vh
    padding-left: 20%
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

.processing-info-out
    margin-top: 20px

.processing-info 
    text-align: center
    font-size: 22px
    font-weight: bold
    border-radius: 0
    .processing-info-into
        padding: 30px
        border: 2px solid #000
        box-shadow: 0 0 0 5px #FF8D7C
        border-radius: 0
  
@media (min-width: 1200px)
    .wait-page
        padding-left: 10%
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