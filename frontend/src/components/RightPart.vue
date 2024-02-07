<template>
  <!-- 右侧部分 -->
  <div class="right-section">
    <!-- 上方标题 -->
    <div class="title">
      <h1>轮胎病疵检测平台</h1>
    </div>

    <!-- 下方左侧原始图片展示 -->
    <div class="container">
      <div class="box">
        原始图片
        <div class="image-box">
          <img v-if="currentImageUrl" class="image" :src="currentImageUrl" alt="原始图片" fit="cover" @dblclick="openImg" />
          <div v-else class="empty-image"></div>
        </div>
      </div>
      <div class="separator"></div>
      <div class="box">
        预测图片
        <div class="image-box">
          <img v-if="currentDrawUrl" class="image" :src="currentDrawUrl" alt="预测图片" fit="cover" @dblclick="openDraw">
          <div v-else class="empty-image"></div>
        </div>
      </div>
    </div>
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
    },
    openImg() {
      window.open(this.currentImageUrl);
    },
    openDraw() {
      window.open(this.currentDrawUrl);
    }
  }
};
</script>

<style scoped>
.right-section {
  background-color: #fff;
  display: block;
  position: absolute;
  left: 15%;
  right: 0;
  top: 0;
  bottom: 0;
  overflow: auto;
}

.container {
  height: 90%;
  display: flex;
  justify-content: space-around;
}

.separator {
  border-left: 1px solid #D4D4D4;
  height: 100%;
  margin: auto;
  margin-top: 2%;
}

.box {
  flex: 1;
  color: black;
  text-align: center;
  font-size: large;
}

.image-box {
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image {
  max-width: 100%;
  max-height: 100%;
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
  background-color: #373737;
  border-bottom: 1px solid #ccc;
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
  padding: 8px;
  text-align: center;
  font-weight: bold;
}
</style>
