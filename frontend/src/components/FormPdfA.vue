<template>
  <header-a class="header_scrolled"></header-a>
    <div class="get-file-page">
        <div class="container">
            <form action="" class="form">
                <div class="form__line">
                    <label for="formFile" class="form-label">PDF файл</label>
                    <input ref="file" class="form-control" type="file" id="formFile" accept=".pdf" v-on:change="handleFileUpload()">
                </div>
                <div class="form__line">
                    <label class="form-label">Язык документа</label>
                    <select ref="lang" class="form-select" aria-label="Type of " id="formPDFLang" v-model="formPDFLang">
                        <option selected value="RUS">Русский</option>
                        <option value="ENG">Английский</option>
                    </select>
                </div>
                <div @click="showPreview">
                    <a class="form__preview-button" :class="{'form__preview-button_active' : isFileExists}" href="#">Посмотреть превью</a>
                </div>
                <div class="form__submit">
                    <button-a class="form__button" @click="submitFile">В работу!</button-a>
                </div>
            </form>
            <img class="get-file-page__flower" src="@/assets/img/Flowers-form.svg" alt="">
            <img class="get-file-page__flower-desk" src="@/assets/img/Flowers-form-desk.svg" alt="">
        </div>
    </div>

  <dialog-a v-model:show="showPdfPreview">
  <vue-pdf-embed
      :source="pdfSource"/>
  </dialog-a>

</template>

<script>
import axios from "axios";
import HeaderA from "@/components/HeaderA";
import VuePdfEmbed from 'vue-pdf-embed'

export default {
  name: "form-pdf-a",
  components: {HeaderA,  VuePdfEmbed},
  data() {
    return {
      file: '',
      fileID: '',

      showPdfPreview: false,
      isFileExists: false,
      formPDFLang: 'RUS',
      pdfSource: '',

      hostname: 'http://localhost:8000', // 'http://45.10.245.207:80'
    }
  },
  methods: {
    handleFileUpload() {
      if (this.$refs.file.files[0]) {
        this.file = this.$refs.file.files[0];
        this.isFileExists = Boolean(this.$refs.file.files[0]);
      }
    },
    checkPdfFile() {
      if (!this.file) return false;
      let filename_type = this.file.name.split('.');
      console.log(this.file.name)
      return !(filename_type[filename_type.length - 1].toLowerCase() !== "pdf" || this.file.size > 200 * 1024 * 1024);
    },
    convertToBase64() {
      let fileReader = new FileReader();
      const w = (str_) => {
        this.pdfSource = str_;
      }

      fileReader.onload = function (fileLoadedEvent) {
        let base64 = fileLoadedEvent.target.result;
        w(base64.toString());
      };
      fileReader.readAsDataURL(this.file);
    },
    showPreview() {
      if (!this.checkPdfFile()) return;
      this.convertToBase64();
      this.showPdfPreview = true;
    },
    async submitFile() {
      if (!this.checkPdfFile()) return;

      let formData = new FormData();
      formData.append('file', this.file);
      
      await axios
          .post(
              this.hostname + '/v1/form/filled/',
              formData,
              {
                params: {
                  lang: this.$refs.lang.value,
                }
              },
              {
                headers: {
                  'Content-Type': 'multipart/form-data'
                }
              }
          )
          .then(({data}) => {
            if (data.validate && data.fileID) {
              this.fileID = data.fileID
            }
          })
      if (this.fileID) {
        this.$router.push({name: 'wait-result-page', params: {fileID: this.fileID}})
      }
    }
  }
}
</script>

<style lang="sass">
.get-file-page
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

.form
    width: 100%
    &__line
        margin-bottom: 2rem
        border: var(--border)
        width: 100%
        display: flex
        align-items: center
        background-color: #fff
        & label
            margin: 0
            background-color: $light-blue
            padding: 0.5rem 1.5rem
            width: 40%
            border-right: var(--border)
        & :last-child
            border: none
            padding: 0 1.5rem
            width: 60%
    &__preview-button
        color: #A7A7A7
        transition: color .5s
        &:not(.form__preview-button_active):hover
            color: #A7A7A7
            text-decoration: none
        &_active
            color: blue
    &__button
        margin-top: 5rem
        background-color: #fff
        padding-left: 4rem
        padding-right: 4rem

@media (min-width: 768px)
    .form
        font-size: 20px
        &__line
            & label
                margin: 0
                padding: 1rem 3rem
            & :last-child
                padding: 0rem 3rem

@media (min-width: 1200px)
    .get-file-page
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
    .form
        min-width: 500px
        position: relative
        &__button
            margin-top: 5rem
            background-color: #fff
            padding-left: 4rem
            padding-right: 4rem
            position: absolute
            bottom: 0
            left: 0


.pdf_previewer__grayscale
  -webkit-filter: grayscale(100%) !important
  -moz-filter: grayscale(100%) !important
  filter: grayscale(100%) !important

</style>