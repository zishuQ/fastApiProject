<template>
  <!-- 左侧功能区 -->
  <div class="sidebar">
    <!--logo-->
    <img src="./icons/LogoSDUST.png" alt="Logo" class="logo" />

    <el-select v-model="model" placeholder="请选择模型">
      <el-option v-for="model in modelList" :key="model" :label="model" :value="model" @click="selectModel" />
    </el-select>

    <!-- 参数设置 -->
    <el-form ref="formData" :model="formData" label-position="left">
      <!-- 文件上传 -->
      <el-form-item label="文件上传">
        <el-upload class="upload-demo" action="http://localhost:5003/upload" :show-file-list="false"
          :before-upload="beforeUpload" :on-success="handleSuccess" multiple>
          <el-button type="primary" size="small"><el-icon>
              <PictureFilled />
            </el-icon>点击上传</el-button>
        </el-upload>
      </el-form-item>
      <div style="background-color: black">
        <el-row class="row-bg" justify="space-evenly">
          <el-col :span="3"><el-button type="primary" size="small" @click="prevImage"><el-icon>
                <ArrowLeftBold />
              </el-icon>上一张</el-button></el-col>

          <el-col :span="8"><el-button type="primary" size="small" @click="nextImage">下一张<el-icon>
                <ArrowRightBold />
              </el-icon></el-button></el-col>
        </el-row>
      </div>


      <!-- 视频上传 -->
      <el-form-item label="视频上传">
        <el-upload class="upload-demo" action="/your/upload" :show-file-list="false" :before-upload="beforeUpload">
          <el-button type="primary" size="small"><el-icon>
              <VideoCamera />
            </el-icon>点击上传</el-button>
        </el-upload>
      </el-form-item>
      <!-- 摄像头实时检测 -->
      <el-form-item size="default" label="摄像头实时检测">
        <el-button><el-icon>
            <CameraFilled />
          </el-icon>
        </el-button>
      </el-form-item>
    </el-form>

    <!-- IoU滑块和数字输入框 -->
    <label for="iou">IoU阈值：</label>
    <el-slider v-model="iouRef" :min="0" :max="1" :step="0.01" />
    <el-input-number v-model="iouRef" :min="0" :max="1" :step="0.01" />
    <br>
    <!-- 置信度滑块和数字输入框 -->
    <label for="confidence">置信度阈值：</label>
    <el-slider v-model="confidenceRef" :min="0" :max="1" :step="0.01" />
    <el-input-number v-model="confidenceRef" :min="0" :max="1" :step="0.01" />

    <el-form ref="formData" :model="formData" label-width="100px" label-position="top">
      <!-- 帧间延时滑块和数字输入框 -->
      <el-form-item label="帧间延时">
        <el-switch v-model="formData.enableFrameDelay" active-color="#13ce66" inactive-color="#ff4949" active-text="On"
          inactive-text="Off">
          {{ formData.enableFrameDelay }}
        </el-switch>
        <el-slider v-model="formData.frameDelay" :min="1" :max="20" :step="1" :disabled="!formData.enableFrameDelay" />
        <el-input-number v-model="formData.frameDelay" :min="1" :max="20" :step="1"
          :disabled="!formData.enableFrameDelay" />
      </el-form-item>
    </el-form>


    <div class="el-checkbox">
      <el-checkbox v-model="autoDetect" label="自动检测" size="small" :checked="autoDetect" />
      <el-checkbox v-model="warning" label="预警功能" size="small" :checked="warning" />
    </div>

    <!--病疵统计数据-->
    <div class="bingci-statistics">
      <!-- 使用 v-for 迭代 image_info 中的病疵信息 -->
      <el-statistic v-for="(info, key) in labelCounts" :key="key" :title="key" :value="`${info}`" />
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
    VideoCamera
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
  background-color: #222222;
  display: block;
  position: fixed;
  left: 0;
  top: 0;
  right: 85%;
  bottom: 0;

}

.logo {
  max-width: 100%;
  height: auto;
  background-color: #181818;
}

.bingci-statistics {
  background-color: #181818;
  text-align: center;
  color: #f2f2f2;
}
</style>
