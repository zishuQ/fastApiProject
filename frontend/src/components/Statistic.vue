<template>
  <div class="Statistic">
    <!-- 下拉列表选择生产线 -->
    <el-select v-model="selectedProductionLine" placeholder="选择生产线">
      <el-option v-for="line in productionLines" :key="line.value" :label="line.label" :value="line.value" @click="selectProductionLine"></el-option>
    </el-select>

    <!-- 轮胎信息表格 -->
    <el-table :data="tireList">
      <!-- 表格列配置 -->
      <el-table-column label="轮胎名称" prop="TireName"></el-table-column>
      <el-table-column label="生产日期" prop="ProduceDate"></el-table-column>
      <el-table-column label="检测日期" prop="DefectDate"></el-table-column>
      <el-table-column label="详细信息">
        <template #default="{ row }">
          <div v-if="Object.keys(row.Info).length > 0">
            <el-table :data="getInfoTableData(row.Info)" style="width: 100%" :show-header="false">
              <el-table-column prop="prop"></el-table-column>
              <el-table-column prop="value"></el-table-column>
            </el-table>
          </div>
          <div v-else>无病疵</div>
        </template>
      </el-table-column>
    </el-table>

    <!-- 轮胎详细信息弹窗 -->
    <el-dialog v-if="showDetailDialog" title="轮胎详细信息" :visible.sync="showDetailDialog">
      <!-- 轮胎详细信息内容 -->
      <!-- 可根据需要展示轮胎详细信息的各个属性 -->
    </el-dialog>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedProductionLine: 1,
      productionLines: [
        { label: '生产线1', value: 1 },
        { label: '生产线2', value: 2 },
      ],
      showDetailDialog: false,
      tireList : [],
    };
  },
  mounted() {

  },
  methods: {
    getInfoTableData(info) {
      // 将 Info 转换为表格数据格式
      return Object.keys(info).map(prop => ({ prop, value: info[prop] }));
    },
    selectProductionLine(){
      console.log(this.selectedProductionLine);
      axios.get('http://localhost:5003/tireInfo/'+this.selectedProductionLine).then(
          response=>{
            this.tireList=response.data.data.tireList;
            console.log(this.tireList);
          }
      ).catch(error=>{
        console.error('Error fetching models:',error)
      });
    }
  },
};
</script>
<style>
.Statistic {
  height: 300px;
  width: 100%;
  overflow: auto;
}
</style>

