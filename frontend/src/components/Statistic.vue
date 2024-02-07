<template>
  <div class="Statistic">
    <el-select v-model="selectedProductionLine" placeholder="选择生产线">
      <el-option v-for="line in productionLines" :key="line.value" :label="line.label" :value="line.value"
        @click="selectProductionLine">
      </el-option>
    </el-select>
    <div>
      <el-popover placement="right" :width="635" trigger="click">
        <template #reference>
          <el-button style="margin-right: 16px; border-radius: 0%; background-color: #373737; color: #fff;"
            @click="selectProductionLine">查询生产线信息</el-button>
        </template>
        <el-table class="sub-item" :data="tireList">
          <el-table-column width="100" property="TireName" label="轮胎名称" />
          <el-table-column width="100" property="ProduceDate" label="生产日期" />
          <el-table-column width="100" property="DefectDate" label="检测日期" />
          <el-table-column width="310" property="Info" label="详细信息">
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
      </el-popover>
    </div>
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
      tireList: [],
      dialogVisible: false
    };
  },
  mounted() {

  },
  methods: {
    getInfoTableData(info) {
      // 将 Info 转换为表格数据格式
      return Object.keys(info).map(prop => ({ prop, value: info[prop] }));
    },
    selectProductionLine() {
      console.log(this.selectedProductionLine);
      axios.get('http://localhost:5003/tireInfo/' + this.selectedProductionLine).then(
        response => {
          this.tireList = response.data.data.tireList;
          console.log(this.tireList);
        }
      ).catch(error => {
        console.error('Error fetching models:', error)
      });
    }
  },
};
</script>
<style>
.Statistic {
  margin-top: 5px;
  margin-bottom: 5px;
}

.sub-item {
  height: 500px;
  overflow-y: auto;
}
</style>

