<template>
  <div class="modal fade" id="controlModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">设备控制</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <div v-for="cmd in deviceCommands" :key="cmd.command" class="mb-3">
            <template v-if="cmd.type">
              <label class="form-label">{{ cmd.label }}</label>
              <template v-if="cmd.type === 'select'">
                <select class="form-select" v-model="commandValues[cmd.command]">
                  <option v-for="option in cmd.options" :key="option" :value="option">
                    {{ option }}
                  </option>
                </select>
              </template>
              <template v-else>
                <input
                  :type="cmd.type"
                  class="form-control"
                  v-model.number="commandValues[cmd.command]"
                  :min="cmd.min"
                  :max="cmd.max"
                  :step="cmd.step"
                >
              </template>
              <button class="btn btn-primary mt-2" @click="sendCommand(cmd)">
                应用
              </button>
            </template>
            <template v-else>
              <button
                :class="['btn', cmd.class || 'btn-primary', 'w-100']"
                @click="sendCommand(cmd)"
              >
                {{ cmd.label }}
              </button>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { DeviceControl } from '@/types/device';
import { DEVICE_COMMANDS } from '@/constants/device';
import { useDeviceStore } from '@/stores/device';

const props = defineProps<{
  deviceId: string;
  deviceType: string;
}>();

const deviceStore = useDeviceStore();
const commandValues = ref<Record<string, any>>({});

const deviceCommands = computed(() => {
  return DEVICE_COMMANDS[props.deviceType] || [];
});

async function sendCommand(cmd: DeviceControl) {
  const command: Record<string, any> = { command: cmd.command };
  
  if (cmd.type === 'select') {
    command[cmd.param || cmd.command] = commandValues.value[cmd.command];
  } else if (cmd.type === 'number' || cmd.type === 'range') {
    const value = commandValues.value[cmd.command];
    if (typeof value === 'number') {
      command[cmd.param || cmd.command] = value;
    }
  }
  
  await deviceStore.sendCommand(props.deviceId, command);
}
</script> 