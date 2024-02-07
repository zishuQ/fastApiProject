<template>
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

    <!-- 帧间延时滑块和数字输入框 -->
    <el-form ref="formData" :model="formData" label-width="100px" label-position="top">
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
</template>

<script></script>