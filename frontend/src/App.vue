<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <nav class="main-nav">
      <div class="nav-content">
        <span class="logo">Intuitive Care - Operadoras</span>
      </div>
    </nav>

    <RouterView />
  </div>
</template>

<style>
:root {
  --primary: #42b883;
  --dark: #2c3e50;
  --gray: #f8f9fa;
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', sans-serif;
  background-color: #f0f2f5;
  color: var(--dark);
}

.main-nav {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-content {
  max-width: 1600px;
  margin: 0 auto;
}

.logo {
  font-weight: bold;
  font-size: 1.2rem;
  color: var(--primary);
}

.app-container {
  min-height: 100vh;
}
</style>