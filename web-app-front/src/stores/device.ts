import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Device } from '@/types/device';
import { api } from '@/services/api';

export const useDeviceStore = defineStore('device', () => {
  const devices = ref<Record<string, Device>>({});
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchDevices() {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.getDevices();
      // 将设备数组转换为以ID为键的对象
      devices.value = response.reduce((acc, device) => {
        acc[device.id] = device;
        return acc;
      }, {} as Record<string, Device>);
    } catch (e) {
      error.value = e instanceof Error ? e.message : '获取设备列表失败';
    } finally {
      loading.value = false;
    }
  }

  async function addDevice(type: string, id: string) {
    error.value = null;
    try {
      const response = await api.addDevice(type, id);
      if ('error' in response) {
        error.value = response.error;
        return false;
      }
      await fetchDevices();
      return true;
    } catch (e) {
      error.value = e instanceof Error ? e.message : '添加设备失败';
      return false;
    }
  }

  async function removeDevice(id: string) {
    error.value = null;
    try {
      const response = await api.removeDevice(id);
      if ('error' in response) {
        error.value = response.error;
        return false;
      }
      await fetchDevices();
      return true;
    } catch (e) {
      error.value = e instanceof Error ? e.message : '删除设备失败';
      return false;
    }
  }

  async function sendCommand(id: string, command: any) {
    error.value = null;
    try {
      const response = await api.sendCommand(id, command);
      if ('error' in response) {
        error.value = response.error;
        return false;
      }
      await fetchDevices();
      return true;
    } catch (e) {
      error.value = e instanceof Error ? e.message : '发送命令失败';
      return false;
    }
  }

  return {
    devices,
    loading,
    error,
    fetchDevices,
    addDevice,
    removeDevice,
    sendCommand
  };
}); 