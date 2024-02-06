<script setup>
import RightPart from "@/components/RightPart.vue";
import LeftPart from './components/LeftPart.vue'

</script>

<template>
  <main>
    <div class="grid-container">
      <div class="left part">
        <LeftPart/>
      </div>>
      <div class="right part">
        <RightPart />
      </div>
    </div>
  </main>
</template>

<style scoped>
.grid-container {
  .left.part {
    grid-row: span;
  }
  .right.part {
    grid-row: span;
  }
}
</style>
