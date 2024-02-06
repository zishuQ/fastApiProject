<template>
  <!-- 右侧部分 -->
  <div class="right-section">
    <!-- 上方标题 -->
    <div class="title">
      <h1>轮胎病疵检测系统</h1>
    </div>

    <el-row :gutter="40"><!-- 下方左侧原始图片展示 -->
      <el-col :span="10" class="upload-container">
        <el-image class="image" v-if="currentImageUrl" :src="currentImageUrl" alt="原始图片" fit="cover">
          原始图片
        </el-image>

      </el-col>

      <el-col :span="10" class="upload-container">
        <el-image class="draw" v-if="currentDrawUrl" :src="currentDrawUrl" alt="预测图片" fit="cover">
          预测图片
        </el-image>

      </el-col>
    </el-row>

    <RouterView>
      <statistic></statistic>
    </RouterView>

  </div>
</template>

<script>

import eventBus from '@/EventBus';
import statistic from '@/components/Statistic.vue';
export default {
  components: {
    statistic
  },
  data() {
    return {
      currentImageUrl: '', // 用于存储上传或摄像头捕获的原始图片路径
      currentDrawUrl: '', // 用于存储深度学习预测的图像路径
    };
  },
  mounted() {
    eventBus.on('imageUploaded', ({ currentImgUrl, currentDrawUrl }) => {

      this.setImage(currentImgUrl, currentDrawUrl);
    });
    eventBus.on('prevImage', ({ currentImgUrl, currentDrawUrl }) => {
      this.setImage(currentImgUrl, currentDrawUrl);
    });
    eventBus.on('nextImage', ({ currentImgUrl, currentDrawUrl }) => {
      this.setImage(currentImgUrl, currentDrawUrl);
    });
  },
  methods: {
    setImage(currentImgUrl, currentDrawUrl) {
      this.currentDrawUrl = currentDrawUrl;
      this.currentImageUrl = currentImgUrl;
    }
  }
};
</script>

<style scoped>
.right-section {
  background-color: #222222;
  display: block;
  position: absolute;
  left: 15%;
  right: 0;
  top: 0;
  bottom: 0;
  overflow: auto;
}

.upload-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 500px;
  width: 500px;
  border: 1px solid #ccc;
  margin-bottom: 20px;
  margin-left: 3%;
  margin-right: 3%;
  overflow: auto;
}

.title {
  background-color: #2c3e50;
  top: 0;
  bottom: 95%;
  left: 15%;
  right: 0;
  text-align: center;
  color: #f2f2f2;
}

.upload-title {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(255, 255, 255, 0.8);
  /* 背景透明度可以根据需要调整 */
  padding: 8px;
  text-align: center;
  font-weight: bold;
}
</style>
