<template>
  <div class="container mt-4">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
      <div class="container">
        <a class="navbar-brand" href="#">
          <i class="bi bi-house-door"></i> 智能家居设备模拟器
        </a>
        <div class="d-flex">
          <span class="navbar-text text-light me-3">
            <i class="bi bi-clock"></i> {{ currentTime }}
          </span>
        </div>
      </div>
    </nav>

    <div class="row mb-4">
      <div class="col">
        <AddDeviceForm />
      </div>
    </div>

    <div v-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>

    <div class="row" v-if="!loading">
      <template v-for="(device, id) in devices" :key="id">
        <DeviceCard
          :id="id"
          :device="device"
          @show-control="showControlModal(id, device.type)"
        />
      </template>
    </div>

    <div v-else class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">加载中...</span>
      </div>
    </div>

    <DeviceControlModal
      v-if="selectedDevice"
      :device-id="selectedDevice.id"
      :device-type="selectedDevice.type"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useDeviceStore } from '@/stores/device';
import AddDeviceForm from '@/components/AddDeviceForm.vue';
import DeviceCard from '@/components/DeviceCard.vue';
import DeviceControlModal from '@/components/DeviceControlModal.vue';
import { Modal } from 'bootstrap';

const deviceStore = useDeviceStore();
const currentTime = ref(new Date().toLocaleTimeString());
const selectedDevice = ref<{ id: string; type: string } | null>(null);

let timer: number;
let modal: Modal;

onMounted(() => {
  deviceStore.fetchDevices();
  
  // 更新当前时间
  timer = window.setInterval(() => {
    currentTime.value = new Date().toLocaleTimeString();
  }, 1000);
  
  // 初始化 Bootstrap Modal
  const modalElement = document.getElementById('controlModal');
  if (modalElement) {
    modal = new Modal(modalElement);
  }
});

onUnmounted(() => {
  clearInterval(timer);
});

function showControlModal(id: string, type: string) {
  selectedDevice.value = { id, type };
  modal?.show();
}

const { devices, loading, error } = deviceStore;
</script>

<style>
@import 'bootstrap-icons/font/bootstrap-icons.css';
</style>
