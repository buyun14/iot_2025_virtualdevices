import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Device } from '@/types/device';
import { api } from '@/services/api';

export const useDeviceStore = defineStore('device', () => {
  const devices = ref<Record<string, Device>>({});
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchDevices() {
    loading.value = true;
    try {
      devices.value = await api.getDevices();
      error.value = null;
    } catch (e) {
      error.value = 'Failed to fetch devices';
      console.error(e);
    } finally {
      loading.value = false;
    }
  }

  async function addDevice(type: string, id: string) {
    loading.value = true;
    try {
      const result = await api.addDevice(type, id);
      if ('error' in result) {
        error.value = result.error;
      } else {
        await fetchDevices();
      }
    } catch (e) {
      error.value = 'Failed to add device';
      console.error(e);
    } finally {
      loading.value = false;
    }
  }

  async function removeDevice(id: string) {
    loading.value = true;
    try {
      const result = await api.removeDevice(id);
      if ('error' in result) {
        error.value = result.error;
      } else {
        await fetchDevices();
      }
    } catch (e) {
      error.value = 'Failed to remove device';
      console.error(e);
    } finally {
      loading.value = false;
    }
  }

  async function sendCommand(id: string, command: any) {
    loading.value = true;
    try {
      const result = await api.sendCommand(id, command);
      if ('error' in result) {
        error.value = result.error;
      } else {
        await fetchDevices();
      }
    } catch (e) {
      error.value = 'Failed to send command';
      console.error(e);
    } finally {
      loading.value = false;
    }
  }

  return {
    devices,
    loading,
    error,
    fetchDevices,
    addDevice,
    removeDevice,
    sendCommand,
  };
}); 