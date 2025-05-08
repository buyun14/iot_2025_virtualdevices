import type { DeviceControl } from '@/types/device';
import type { DeviceState } from '@/types/device';

export type DeviceType = 'light' | 'thermostat' | 'doorlock' | 'blind' | 'ac' | 'smoke_detector' | 'fan' | 'smart_plug';

export const DEVICE_TYPES: DeviceType[] = [
  'light',
  'thermostat',
  'doorlock',
  'blind',
  'ac',
  'smoke_detector',
  'fan',
  'smart_plug',
];

export const DEVICE_ICONS: Record<DeviceType, string> = {
  light: 'bi-lightbulb',
  thermostat: 'bi-thermometer-half',
  doorlock: 'bi-door-closed',
  blind: 'bi-window',
  ac: 'bi-snow',
  smoke_detector: 'bi-shield-exclamation',
  fan: 'bi-fan',
  smart_plug: 'bi-plug'
};

export const DEVICE_COMMANDS: Record<string, DeviceControl[]> = {
  light: [
    { command: 'turn_on', label: '开启' },
    { command: 'turn_off', label: '关闭' },
    { command: 'set_brightness', label: '设置亮度', type: 'range', min: 0, max: 100, step: 1 },
    { command: 'set_color_temp', label: '设置色温', type: 'range', min: 2700, max: 6500, step: 100 },
  ],
  thermostat: [
    { command: 'turn_on', label: '开启' },
    { command: 'turn_off', label: '关闭' },
    { command: 'set_temp', label: '设置温度', type: 'number', min: 16, max: 30, step: 0.5 },
    { command: 'set_mode', label: '设置模式', type: 'select', options: ['cool', 'heat', 'dry', 'fan'] },
  ],
  doorlock: [
    { command: 'lock', label: '锁定' },
    { command: 'unlock', label: '解锁' },
    { command: 'check_battery', label: '检查电池' },
  ],
  blind: [
    { command: 'open', label: '打开' },
    { command: 'close', label: '关闭' },
    { command: 'set_position', label: '设置位置', type: 'range', min: 0, max: 100, step: 1 },
    { command: 'set_tilt', label: '设置倾斜角度', type: 'range', min: 0, max: 180, step: 1 },
  ],
  ac: [
    { command: 'turn_on', label: '开启' },
    { command: 'turn_off', label: '关闭' },
    { command: 'set_temp', label: '设置温度', type: 'number', min: 16, max: 30, step: 0.5 },
    { command: 'set_mode', label: '设置模式', type: 'select', options: ['cool', 'heat', 'dry', 'fan'] },
    { command: 'set_fan_speed', label: '设置风速', type: 'select', options: ['auto', 'low', 'medium', 'high'] },
    { command: 'toggle_swing', label: '切换摇摆' },
  ],
  smoke_detector: [
    { command: 'reset', label: '重置' },
    { command: 'test', label: '测试' },
  ],
  fan: [
    { command: 'turn_on', label: '开启' },
    { command: 'turn_off', label: '关闭' },
    { command: 'set_speed', label: '设置风速', type: 'select', options: ['1', '2', '3'] },
    { command: 'toggle_oscillate', label: '切换摇摆' },
    { command: 'set_timer', label: '设置定时', type: 'number', min: 0, max: 120, step: 1 },
  ],
  smart_plug: [
    { command: 'turn_on', label: '开启' },
    { command: 'turn_off', label: '关闭' },
    { command: 'set_timer', label: '设置定时', type: 'number', min: 0, max: 1440, step: 1 },
  ],
};

export const STATUS_TRANSLATIONS: Partial<Record<keyof DeviceState, string>> = {
  on: '开关状态',
  state: '开关状态',
  brightness: '亮度',
  color_temp: '色温',
  power_consumption: '功率消耗',
  temp: '温度',
  mode: '模式',
  fan_speed: '风速',
  swing: '摇摆',
  locked: '锁定状态',
  battery_level: '电池电量',
  last_lock_time: '最后锁定时间',
  last_unlock_time: '最后解锁时间',
  tamper_alert: '防拆警报',
  position: '位置',
  tilt: '倾斜角度',
  moving: '移动状态',
  last_move_time: '最后移动时间',
  alarm: '警报状态',
  smoke_level: '烟雾浓度',
  last_test_time: '最后测试时间',
  speed: '速度',
  oscillate: '摇摆',
  timer: '定时器',
  voltage: '电压',
  current: '电流',
  schedule: '定时任务',
  error_state: '错误状态',
  online: '在线状态',
  last_update: '最后更新时间'
}; 