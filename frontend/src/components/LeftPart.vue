<template>
  <!-- 左侧功能区 -->
  <div class="sidebar">
    <!--logo-->
    <!-- <img src="./icons/LogoSDUST.png" alt="Logo" class="logo" /> -->

    <div id="model-select">
      <div style="color: #fff; margin: 5px;">设置</div>
      <el-select v-model="model" placeholder="请选择模型">
        <el-option v-for="model in modelList" :key="model" :label="model" :value="model" @click="selectModel" />
      </el-select>
    </div>

    <el-form ref="formData" :model="formData" label-position="left">
      <el-form-item style="margin-top: 5px; marginbot" class="form-item" label="">
        <text style="color: #fff; margin-right: 10px;">文件上传</text>
        <el-upload class="upload-demo" action="http://localhost:5003/upload" :show-file-list="false"
          :before-upload="beforeUpload" :on-success="handleSuccess" multiple>
          <el-button type="primary" size="small">
            <el-icon>
              <PictureFilled />
            </el-icon>点击上传
          </el-button>
        </el-upload>
      </el-form-item>
      <div style="background-color: #373737">
        <el-row class="row-bg" justify="space-evenly">
          <el-col :span="3">
            <el-button type="primary" size="small" @click="prevImage">
              <el-icon>
                <ArrowLeftBold />
              </el-icon>上一张
            </el-button>
          </el-col>
          <el-col :span="8">
            <el-button type="primary" size="small" @click="nextImage">下一张
              <el-icon>
                <ArrowRightBold />
              </el-icon>
            </el-button>
          </el-col>
        </el-row>
      </div>
    </el-form>
    <!-- IoU滑块和数字输入框 -->
    <label for="iou">
      <div class="IoU-text">
        IoU
      </div>
    </label>
    <div class="center-container">
      <el-slider class="slider" v-model="iouRef" :min="0" :max="1" :step="0.01" />
    </div>
    <div class="center-container">
      <el-input-number class="input-number" v-model="iouRef" :min="0" :max="1" :step="0.01" />
    </div>
    <!-- 置信度滑块和数字输入框 -->
    <label for="confidence">
      <div style="color: #fff;margin-left: 5px;">
        置信度
      </div>
    </label>
    <div class="center-container">
      <el-slider class="slider" v-model="confidenceRef" :min="0" :max="1" :step="0.01" />
    </div>
    <div class="center-container">
      <el-input-number v-model="confidenceRef" :min="0" :max="1" :step="0.01" />
    </div>
    <div>
      <text style="color: #fff; margin-left: 5px;">
        各类病疵统计
      </text>
    </div>
    <div class="bingci">
      <div class="bingci-statistics" v-for="(info, key) in labelCounts" :key="key">
        <div class="statistics">
          <text>{{ key }}:{{ info }}</text>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, watch } from "vue";
import eventBus from '@/EventBus';
import { ArrowLeftBold, ArrowRightBold, CameraFilled, PictureFilled, VideoCamera } from "@element-plus/icons-vue";

const data = {
  "image_url": "",
  "draw_url": "",
  "image_info": {
    "label_counts": {}
  }
}
export default {
  components: {
    CameraFilled,
    PictureFilled,
    ArrowLeftBold,
    ArrowRightBold,
    VideoCamera,
  },
  computed: {

  },
  setup() {
    // 使用 ref 创建响应式数据
    const iouRef = ref(0.5);
    const confidenceRef = ref(0.5);

    // 使用 watch 监听 ref 数据的变化
    watch([iouRef, confidenceRef], ([newIou, newConfidence]) => {
      sendParametersToBackend(newIou, newConfidence);
    });

    // 发送参数到后端的函数
    const sendParametersToBackend = (newIou, newConfidence) => {
      // 发送参数到后端
      axios.post('http://localhost:5003/updateModel', { iou_thres: newIou, conf_thres: newConfidence })
        .then(response => {
          console.log(response.data.message);
        })
        .catch(error => {
          console.error('Error setting parameters:', error);
        });
    };

    // 返回数据和方法
    return {
      iouRef,
      confidenceRef
    };
  },

  data() {
    return {
      model: null,
      modelList: [],
      autoDetect: false,
      warning: false,
      formData: {
        frameDelay: 1,
        enableFrameDelay: false
      },
      stream: null,
      responseData: null,
      path: [],       // 存储所有上传的图片地址
      currentIndex: 0,  // 当前显示图片的索引
    };
  },

  mounted() {
    axios.get('http://localhost:5003/modelList').then(
      response => {
        this.modelList = response.data.data.modelList
      }
    ).catch(error => {
      console.error('Error fetching models:', error)
    });


  },

  methods: {
    selectModel() {
      axios.post(
        'http://localhost:5003/chooseModel', { model: this.model }).then(response => {
          console.log(response.data.message)
        }).catch(error => {
          console.error('Error selecting model:', error)
        })
    },
    beforeUpload(files) {
      // 将文件添加到 FormData 中
      const formData = new FormData();
      formData.append('images', files);
      // 使用 Axios 发送 POST 请求
      axios.post('http://localhost:5003/upload', formData)
        .then(response => {
          // 处理成功响应
          this.handleSuccess(response.data.data.path);
        })
        .catch(error => {
          // 处理错误
          console.error('上传失败：', error);
        });
      return false; // 阻止 el-upload 默认上传行为
    },
    handleSuccess(path) {
      path.forEach(item => {
        this.path.push(item);
      });
      console.log('http://localhost:5003/imgInfo/' + this.path[this.currentIndex]);

      axios.get('http://localhost:5003/imgInfo/' + this.path[this.currentIndex]).then(response => {
        this.labelCounts = response.data.data.image_info.label_counts;
        const imgUrls = {
          currentImgUrl: response.data.data.image_url,
          currentDrawUrl: response.data.data.draw_url,
        };

        eventBus.emit('imageUploaded', imgUrls);
        console.log(imgUrls);
      }).catch(error => {
        console.error('Error fetching statistics', error)
      })
    },
    prevImage() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
      }
      axios.get('http://localhost:5003/imgInfo/' + this.path[this.currentIndex]).then(response => {
        this.labelCounts = response.data.data?.image_info?.label_counts || {};
        const imgUrls = {
          currentImgUrl: response.data.data.image_url,
          currentDrawUrl: response.data.data.draw_url,
        };
        eventBus.emit('prevImage', imgUrls);
      }).catch(error => {
        console.error('Error fetching statistics', error)
      })

    },
    nextImage() {
      if (this.currentIndex < this.path.length - 1) {
        this.currentIndex++;
      }
      axios.get('http://localhost:5003/imgInfo/' + this.path[this.currentIndex]).then(response => {
        this.labelCounts = response.data.data.image_info.label_counts;
        const imgUrls = {
          currentImgUrl: response.data.data.image_url,
          currentDrawUrl: response.data.data.draw_url,
        };
        eventBus.emit('nextImage', imgUrls);
      }).catch(error => {
        console.error('Error fetching statistics', error)
      })
    },
  }
};

</script>

<style>
.sidebar {
  background-color: #373737;
  display: block;
  position: fixed;
  left: 0;
  top: 0;
  right: 85%;
  bottom: 0;
}

.IoU-text {
  color: #fff;
  margin-left: 5px;
}

.logo {
  max-width: 100%;
  height: auto;
  background-color: #373737;
}

.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.slider {
  width: 90%;
  margin: 5px;
}

.bingci {
  width: 90%;
  height: 58%;
  margin: 8px;
  border: 1px solid #f2f2f2;
}

.bingci-statistics {
  background-color: #373737;
  text-align: center;
  color: #f2f2f2;
}
</style>
