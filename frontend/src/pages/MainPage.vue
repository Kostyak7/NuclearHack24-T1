<template>
  <header-a></header-a>
  <main>
    <main-sect-a></main-sect-a>
    <slider-a></slider-a>
    <about-us-a></about-us-a>
    <price-a></price-a>
    <faq-a></faq-a>
  </main>
  <footer-a></footer-a>

</template>


<script>
import HeaderA from "@/components/HeaderA";
import MainSectA from "@/components/MainSectA";
import AboutUsA from "@/components/AboutUsA";
import FaqA from "@/components/FAQA";
import FooterA from "@/components/FooterA";

export default {
  name: "MainPage",
  components: {
    HeaderA,
    MainSectA,
    AboutUsA,
    FaqA,
    FooterA,
  }
}
</script>

<style lang="sass">


</style>
