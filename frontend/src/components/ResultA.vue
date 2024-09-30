<template>
    <header-a class="header_scrolled"></header-a>
  <div class="result-page">
          <div class="container">

                <div class="form__submit">
                    <button-a class="download__button" @click="downloadFile">Скачать файл</button-a>
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
    name: "result-a",
    components: {HeaderA},
    data() {
      return {
        fileID: null,

        hostname: 'https://yourproject7.ru', // 'http://localhost:8000'
      }
    },
    components: { HeaderA },
    mounted() {
        this.fileID = this.$route.params.fileID;
    },
    methods: {
        async downloadFile() {
            try {
                const response = await axios.get(`${this.hostname}/v1/result/${this.fileID}`, {
                    responseType: 'blob'
                });
                
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', `${this.fileID}}.pdf`); 
                document.body.appendChild(link);
                link.click();
                link.remove();
            } catch (error) {
                console.error("Ошибка при скачивании файла:", error);
            }
        }
    }
  }
  </script>
  
<style lang="sass">
  
.result-page
    height: 100vh
    padding-left: 25%
    // align-items: center
    .download__button
        margin-top: 15vh
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
