<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">添加新设备</h5>
      <form @submit.prevent="handleSubmit" class="row g-3">
        <div class="col-md-5">
          <select class="form-select" v-model="deviceType" required>
            <option value="">选择设备类型...</option>
            <option v-for="type in DEVICE_TYPES" :key="type" :value="type">
              {{ type }}
            </option>
          </select>
        </div>
        <div class="col-md-5">
          <input
            type="text"
            class="form-control"
            v-model="deviceId"
            placeholder="设备ID (例如: light-001)"
            required
          >
        </div>
        <div class="col-md-2">
          <button type="submit" class="btn btn-primary w-100" :disabled="loading">
            {{ loading ? '添加中...' : '添加' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { DEVICE_TYPES } from '@/constants/device';
import { useDeviceStore } from '@/stores/device';

const deviceStore = useDeviceStore();
const deviceType = ref('');
const deviceId = ref('');
const loading = ref(false);

async function handleSubmit() {
  if (!deviceType.value || !deviceId.value) return;
  
  loading.value = true;
  try {
    await deviceStore.addDevice(deviceType.value, deviceId.value);
    deviceType.value = '';
    deviceId.value = '';
  } finally {
    loading.value = false;
  }
}
</script> 