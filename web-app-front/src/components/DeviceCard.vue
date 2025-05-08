`<template>
    <div class="col-md-4 mb-4">
      <div class="card device-card">
        <div class="card-body">
          <span class="badge bg-secondary device-type-badge">{{ device.type }}</span>
          
          <div class="text-center device-icon">
            <i :class="['bi', DEVICE_ICONS[device.type]]"></i>
          </div>
          
          <h5 class="card-title text-center">
            <span :class="['status-indicator', device.online ? 'status-online' : 'status-offline']"></span>
            {{ id }}
          </h5>
          
          <div class="card-text">
            <template v-for="(value, key) in device" :key="key">
              <template v-if="!['type', 'online', 'last_update', 'error_state'].includes(key as string)">
                <div class="d-flex justify-content-between align-items-center mb-1">
                  <span class="status-label">{{ STATUS_TRANSLATIONS[key as string] || key }}</span>
                  <span class="status-value">{{ formatValue(key as string, value) }}</span>
                </div>
                <div v-if="typeof value === 'number' && (key as string).includes('level')" class="progress mb-2">
                  <div
                    class="progress-bar"
                    role="progressbar"
                    :style="{ width: value + '%' }"
                    :aria-valuenow="value"
                    aria-valuemin="0"
                    aria-valuemax="100"
                  ></div>
                </div>
              </template>
            </template>
          </div>
          
          <div class="last-update mt-2">
            最后更新: {{ new Date(device.last_update).toLocaleString() }}
          </div>
          
          <div v-if="device.error_state" class="error-state mt-2">
            {{ device.error_state }}
          </div>
          
          <div class="mt-3 text-center">
            <button class="btn btn-primary btn-sm" @click="showControlModal">控制</button>
            <button class="btn btn-danger btn-sm ms-2" @click="handleDelete">删除</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { DEVICE_ICONS, STATUS_TRANSLATIONS } from '@/constants/device';
  import type { Device } from '@/types/device';
  import { useDeviceStore } from '@/stores/device';
  
  const props = defineProps<{
    id: string;
    device: Device;
  }>();
  
  const emit = defineEmits<{
    (e: 'show-control'): void;
  }>();
  
  const deviceStore = useDeviceStore();
  
  function formatValue(key: string, value: any): string {
    if (typeof value === 'boolean') {
      return value ? '是' : '否';
    }
    if (key.includes('temp') && typeof value === 'number') {
      return `${value}°C`;
    }
    if (key.includes('humidity') && typeof value === 'number') {
      return `${value}%`;
    }
    if (key.includes('power') && typeof value === 'number') {
      return `${value}W`;
    }
    if (key.includes('voltage') && typeof value === 'number') {
      return `${value}V`;
    }
    if (key.includes('current') && typeof value === 'number') {
      return `${value}A`;
    }
    return String(value);
  }
  
  function showControlModal() {
    emit('show-control');
  }
  
  async function handleDelete() {
    if (confirm('确定要删除这个设备吗？')) {
      await deviceStore.removeDevice(props.id);
    }
  }
  </script>
  
  <style scoped>
  .device-card {
    transition: all 0.3s ease;
  }
  
  .device-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  }
  
  .status-indicator {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 5px;
  }
  
  .status-online {
    background-color: #28a745;
  }
  
  .status-offline {
    background-color: #dc3545;
  }
  
  .device-icon {
    font-size: 2rem;
    margin-bottom: 1rem;
  }
  
  .status-value {
    font-weight: 500;
  }
  
  .status-label {
    color: #6c757d;
    font-size: 0.875rem;
  }
  
  .progress {
    height: 0.5rem;
  }
  
  .device-type-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
  }
  
  .last-update {
    font-size: 0.75rem;
    color: #6c757d;
  }
  
  .error-state {
    color: #dc3545;
    font-size: 0.875rem;
  }
  </style>