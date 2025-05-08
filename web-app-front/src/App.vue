<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <RouterView />
</template>

<style>
@import 'bootstrap/dist/css/bootstrap.min.css';

body {
  background-color: #f8f9fa;
}

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
